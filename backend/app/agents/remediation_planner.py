from app.agents.base import BaseAgent
from app.models.agent_schemas import RemediationPlan
from app.models.incident import Incident


REMEDIATION_TEMPLATES = {
    "Sleep SLO violation": {
        "actions": [
            "Set bedtime reminder for 10:00 PM",
            "Reduce screen time 1 hour before sleep",
            "Enable sleep tracking notifications",
        ],
        "timeline": "Improvement expected within 2-3 days",
        "expected_outcome": "Sleep hours return above 6h threshold",
        "confidence": 0.85,
    },
    "Activity SLO violation": {
        "actions": [
            "Schedule 30-minute walk",
            "Set hourly movement reminders",
            "Track step count actively",
        ],
        "timeline": "Improvement expected within 1-2 days",
        "expected_outcome": "Step count returns above 3000 threshold",
        "confidence": 0.90,
    },
    "Stress SLO violation": {
        "actions": [
            "Schedule 15-minute meditation session",
            "Practice deep breathing exercises",
            "Review and reduce workload if possible",
        ],
        "timeline": "Improvement expected within 1-2 days",
        "expected_outcome": "Stress score drops below 70 threshold",
        "confidence": 0.75,
    },
    "Heart Rate SLO violation": {
        "actions": [
            "Schedule physician consultation",
            "Reduce caffeine intake",
            "Monitor heart rate every 2 hours",
            "Practice relaxation techniques",
        ],
        "timeline": "Monitor closely over next 24 hours",
        "expected_outcome": "Resting heart rate returns below 90bpm",
        "confidence": 0.70,
    },
}

DEFAULT_REMEDIATION = {
    "actions": ["Investigate root cause", "Monitor metrics closely"],
    "timeline": "Review within 24 hours",
    "expected_outcome": "Metrics return to normal range",
    "confidence": 0.60,
}


class MockRemediationPlanner(BaseAgent):
    name = "remediation-planner"

    async def run(self, input_data: dict) -> dict:
        incident = Incident(**input_data["incident"])
        template = REMEDIATION_TEMPLATES.get(incident.title, DEFAULT_REMEDIATION)

        result = RemediationPlan(
            incident_id=incident.id,
            actions=template["actions"],
            timeline=template["timeline"],
            expected_outcome=template["expected_outcome"],
            confidence=template["confidence"],
        )
        return result.model_dump(mode="json")
