import asyncio
import logging
import os
import uuid
from datetime import datetime, timezone

from app.services.simulator import generate_signal
from app.services.scenarios import scenario_runner
from app.services.slo_engine import evaluate_slos
from app.services.incident_detector import detect_incidents
from app.services.state_store import store
from app.services import timeline_builder as tb
from app.models.action import Action
from app.agents.signal_interpreter import MockSignalInterpreter
from app.agents.incident_triage import MockIncidentTriage
from app.agents.remediation_planner import MockRemediationPlanner
from app.agents.explainability_agent import MockExplainabilityAgent
from app.agents.postmortem_agent import MockPostmortemAgent

logger = logging.getLogger(__name__)


def _create_agents():
    use_ai = os.environ.get("MISTRAL_API_KEY") and os.environ.get("USE_AI_AGENTS", "").lower() in ("1", "true", "yes")

    if use_ai:
        from app.agents.ai_agents import (
            create_ai_signal_interpreter,
            create_ai_incident_triage,
            create_ai_remediation_planner,
            create_ai_explainability_agent,
            create_ai_postmortem_agent,
        )
        logger.info("Using AI-powered agents (Mistral)")
        return {
            "signal_interpreter": create_ai_signal_interpreter(),
            "incident_triage": create_ai_incident_triage(),
            "remediation_planner": create_ai_remediation_planner(),
            "explainability_agent": create_ai_explainability_agent(),
            "postmortem_agent": create_ai_postmortem_agent(),
        }

    logger.info("Using mock agents")
    return {
        "signal_interpreter": MockSignalInterpreter(),
        "incident_triage": MockIncidentTriage(),
        "remediation_planner": MockRemediationPlanner(),
        "explainability_agent": MockExplainabilityAgent(),
        "postmortem_agent": MockPostmortemAgent(),
    }


class Orchestrator:
    def __init__(self, interval: float = 5.0) -> None:
        self.interval = interval
        self._running = False
        self._task: asyncio.Task | None = None
        agents = _create_agents()
        self.signal_interpreter = agents["signal_interpreter"]
        self.incident_triage = agents["incident_triage"]
        self.remediation_planner = agents["remediation_planner"]
        self.explainability_agent = agents["explainability_agent"]
        self.postmortem_agent = agents["postmortem_agent"]

    @property
    def is_running(self) -> bool:
        return self._running

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._loop())

    def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None

    async def _loop(self) -> None:
        while self._running:
            try:
                await self._tick()
            except Exception as e:
                store.add_timeline_event(tb.agent_event("orchestrator", f"Error: {e}"))
            await asyncio.sleep(self.interval)

    async def _tick(self) -> None:
        signal = scenario_runner.get_signal() or generate_signal()
        store.add_signal(signal)
        store.add_timeline_event(tb.signal_event(signal))

        slo_results = evaluate_slos(signal)
        store.add_timeline_event(tb.slo_event(slo_results))

        interpretation = await self.signal_interpreter.run(
            {"signal": signal.model_dump(mode="json")}
        )
        store.add_timeline_event(
            tb.agent_event("signal-interpreter", interpretation["summary"], interpretation)
        )

        # Check for incident resolution — if current SLOs pass, resolve open incidents for that SLO
        passing_slos = {r.slo_name for r in slo_results if r.passed}
        for incident in store.get_open_incidents():
            slo_name = incident.title.replace(" violation", "")
            if slo_name in passing_slos:
                resolved = store.resolve_incident(incident.id)
                if resolved:
                    store.add_timeline_event(
                        tb.agent_event("orchestrator", f"Incident resolved: {resolved.title}", resolved.model_dump(mode="json"))
                    )
                    # Generate postmortem
                    postmortem = await self.postmortem_agent.run(
                        {"incident": resolved.model_dump(mode="json")}
                    )
                    store.add_postmortem(postmortem)
                    store.add_timeline_event(
                        tb.agent_event("postmortem-agent", f"Postmortem generated for {resolved.title}", postmortem)
                    )

        # Detect new incidents — skip duplicates
        incidents = detect_incidents(slo_results)

        for incident in incidents:
            if store.has_open_incident(incident.title):
                continue

            store.add_incident(incident)
            store.add_timeline_event(tb.incident_event(incident))

            triage = await self.incident_triage.run(
                {"incident": incident.model_dump(mode="json")}
            )
            store.add_timeline_event(
                tb.agent_event("incident-triage", triage["reasoning"], triage)
            )

            remediation = await self.remediation_planner.run(
                {"incident": incident.model_dump(mode="json")}
            )
            for action_desc in remediation["actions"]:
                action = Action(
                    id=str(uuid.uuid4())[:8],
                    timestamp=datetime.now(timezone.utc),
                    incident_id=incident.id,
                    action_type="remediation",
                    description=action_desc,
                    agent="remediation-planner",
                )
                store.add_action(action)
                store.add_timeline_event(tb.action_event(action))

            explanation = await self.explainability_agent.run(
                {"incident": incident.model_dump(mode="json")}
            )
            store.add_timeline_event(
                tb.agent_event(
                    "explainability-agent",
                    explanation["plain_language_summary"],
                    explanation,
                )
            )


orchestrator = Orchestrator()
