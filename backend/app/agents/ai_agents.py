import logging
from typing import Type

from pydantic import BaseModel, ValidationError

from app.agents.base import BaseAgent
from app.agents.mistral_client import call_mistral, load_prompt
from app.agents.signal_interpreter import MockSignalInterpreter
from app.agents.incident_triage import MockIncidentTriage
from app.agents.remediation_planner import MockRemediationPlanner
from app.agents.explainability_agent import MockExplainabilityAgent
from app.agents.postmortem_agent import MockPostmortemAgent
from app.models.agent_schemas import (
    SignalInterpretation,
    TriageResult,
    RemediationPlan,
    Explanation,
    Postmortem,
)
from app.models.signals import HealthSignal
from app.models.incident import Incident

logger = logging.getLogger(__name__)


class AIAgent(BaseAgent):
    name: str = ""
    prompt_name: str = ""
    schema: Type[BaseModel] = BaseModel
    fallback: BaseAgent

    def __init__(self, name: str, prompt_name: str, schema: Type[BaseModel], fallback: BaseAgent):
        self.name = name
        self.prompt_name = prompt_name
        self.schema = schema
        self.fallback = fallback

    def _build_prompt_kwargs(self, input_data: dict) -> dict:
        kwargs = {}
        if "signal" in input_data:
            sig = input_data["signal"]
            kwargs.update(sig)
        if "incident" in input_data:
            inc = input_data["incident"]
            kwargs.update(inc)
        return kwargs

    async def run(self, input_data: dict) -> dict:
        try:
            kwargs = self._build_prompt_kwargs(input_data)
            prompt = load_prompt(self.prompt_name, **kwargs)
            result = await call_mistral(prompt)

            if result is None:
                logger.info(f"[{self.name}] Falling back to mock agent")
                return await self.fallback.run(input_data)

            validated = self.schema.model_validate(result)
            logger.info(f"[{self.name}] AI response validated successfully")
            return validated.model_dump(mode="json")

        except ValidationError as e:
            logger.warning(f"[{self.name}] AI response validation failed: {e}")
            return await self.fallback.run(input_data)
        except Exception as e:
            logger.error(f"[{self.name}] Unexpected error: {e}")
            return await self.fallback.run(input_data)


def create_ai_signal_interpreter() -> BaseAgent:
    return AIAgent(
        name="signal-interpreter",
        prompt_name="signal_interpreter",
        schema=SignalInterpretation,
        fallback=MockSignalInterpreter(),
    )


def create_ai_incident_triage() -> BaseAgent:
    return AIAgent(
        name="incident-triage",
        prompt_name="incident_triage",
        schema=TriageResult,
        fallback=MockIncidentTriage(),
    )


def create_ai_remediation_planner() -> BaseAgent:
    return AIAgent(
        name="remediation-planner",
        prompt_name="remediation_planner",
        schema=RemediationPlan,
        fallback=MockRemediationPlanner(),
    )


def create_ai_explainability_agent() -> BaseAgent:
    return AIAgent(
        name="explainability-agent",
        prompt_name="explainability",
        schema=Explanation,
        fallback=MockExplainabilityAgent(),
    )


def create_ai_postmortem_agent() -> BaseAgent:
    return AIAgent(
        name="postmortem-agent",
        prompt_name="postmortem",
        schema=Postmortem,
        fallback=MockPostmortemAgent(),
    )
