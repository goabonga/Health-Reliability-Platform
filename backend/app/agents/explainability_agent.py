from app.agents.base import BaseAgent
from app.models.agent_schemas import Explanation
from app.models.incident import Incident


EXPLANATIONS = {
    "Sleep SLO violation": {
        "what_happened": "Sleep duration dropped below the minimum healthy threshold of 6 hours.",
        "why_it_matters": "Chronic sleep deprivation increases risk of cardiovascular disease, weakens immune function, and impairs cognitive performance.",
        "what_to_do": "Prioritize sleep by setting a consistent bedtime, reducing evening screen time, and creating a restful environment.",
        "plain_language_summary": "You're not getting enough sleep. This can affect your health and daily performance. Try going to bed earlier tonight.",
    },
    "Activity SLO violation": {
        "what_happened": "Daily step count fell below the minimum threshold of 3,000 steps.",
        "why_it_matters": "Sedentary behavior is linked to increased risk of obesity, diabetes, and cardiovascular issues.",
        "what_to_do": "Take a 30-minute walk, use stairs instead of elevators, and set hourly movement reminders.",
        "plain_language_summary": "You've been too sedentary today. Even a short walk can help improve your health metrics.",
    },
    "Stress SLO violation": {
        "what_happened": "Stress score exceeded the healthy threshold of 70.",
        "why_it_matters": "Elevated stress increases cortisol levels, disrupts sleep, and can lead to burnout and health complications.",
        "what_to_do": "Practice breathing exercises, take breaks, and consider what's driving your stress levels.",
        "plain_language_summary": "Your stress levels are too high. Take a moment to breathe and consider reducing your current workload.",
    },
    "Heart Rate SLO violation": {
        "what_happened": "Resting heart rate exceeded the safe threshold of 90bpm.",
        "why_it_matters": "Persistently elevated resting heart rate can indicate cardiovascular strain, dehydration, or underlying health conditions.",
        "what_to_do": "Rest, hydrate, avoid stimulants, and consult a physician if this persists.",
        "plain_language_summary": "Your resting heart rate is elevated. Stay calm, drink water, and monitor it. See a doctor if it stays high.",
    },
}

DEFAULT_EXPLANATION = {
    "what_happened": "A health metric violated its defined threshold.",
    "why_it_matters": "Health metric violations can indicate declining wellbeing.",
    "what_to_do": "Review your recent habits and consult the recommendations provided.",
    "plain_language_summary": "One of your health indicators needs attention. Check the details for specific guidance.",
}


class MockExplainabilityAgent(BaseAgent):
    name = "explainability-agent"

    async def run(self, input_data: dict) -> dict:
        incident = Incident(**input_data["incident"])
        template = EXPLANATIONS.get(incident.title, DEFAULT_EXPLANATION)

        result = Explanation(
            incident_id=incident.id,
            what_happened=template["what_happened"],
            why_it_matters=template["why_it_matters"],
            what_to_do=template["what_to_do"],
            plain_language_summary=template["plain_language_summary"],
        )
        return result.model_dump(mode="json")
