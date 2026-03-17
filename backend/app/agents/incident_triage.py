from app.agents.base import BaseAgent
from app.models.agent_schemas import TriageResult
from app.models.incident import Incident


SEVERITY_PRIORITY = {
    "critical": "P1",
    "high": "P2",
    "medium": "P3",
    "low": "P4",
}

SEVERITY_CATEGORY = {
    "critical": "cardiovascular",
    "high": "lifestyle-degradation",
    "medium": "activity-deficit",
    "low": "minor-variance",
}


class MockIncidentTriage(BaseAgent):
    name = "incident-triage"

    async def run(self, input_data: dict) -> dict:
        incident = Incident(**input_data["incident"])

        priority = SEVERITY_PRIORITY.get(incident.severity, "P3")
        category = SEVERITY_CATEGORY.get(incident.severity, "general")
        requires_immediate = incident.severity in ("critical", "high")

        reasoning = (
            f"Incident '{incident.title}' classified as {priority} based on "
            f"{incident.severity} severity. Category: {category}. "
            f"{'Immediate action required.' if requires_immediate else 'Monitor and review.'}"
        )

        result = TriageResult(
            incident_id=incident.id,
            priority=priority,
            category=category,
            requires_immediate_action=requires_immediate,
            reasoning=reasoning,
        )
        return result.model_dump(mode="json")
