from datetime import datetime, timezone

from app.agents.base import BaseAgent
from app.models.agent_schemas import Postmortem
from app.models.incident import Incident


class MockPostmortemAgent(BaseAgent):
    name = "postmortem-agent"

    async def run(self, input_data: dict) -> dict:
        incident = Incident(**input_data["incident"])

        result = Postmortem(
            incident_id=incident.id,
            title=f"Postmortem: {incident.title}",
            summary=(
                f"Incident '{incident.title}' was detected at {incident.timestamp.isoformat()}. "
                f"Severity: {incident.severity}. The issue was identified by the SLO engine "
                f"and processed through the agent pipeline."
            ),
            root_cause=f"Health metric degradation detected via {incident.source}: {incident.description}",
            impact=(
                f"A {incident.severity}-severity health reliability incident was raised. "
                f"Automated remediation actions were triggered."
            ),
            lessons_learned=[
                "Early detection via SLO monitoring enabled fast response",
                "Automated triage reduced time to action",
                "Agent pipeline provided consistent analysis",
            ],
            action_items=[
                "Continue monitoring affected metrics",
                "Review threshold configuration for sensitivity",
                "Track recovery trajectory over next 24-48 hours",
            ],
            timestamp=datetime.now(timezone.utc),
        )
        return result.model_dump(mode="json")
