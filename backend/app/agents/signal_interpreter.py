from app.agents.base import BaseAgent
from app.models.agent_schemas import SignalInterpretation
from app.models.signals import HealthSignal


class MockSignalInterpreter(BaseAgent):
    name = "signal-interpreter"

    async def run(self, input_data: dict) -> dict:
        signal = HealthSignal(**input_data["signal"])
        factors = []
        recommendations = []
        risk_level = "low"

        if signal.sleep_hours < 6.0:
            factors.append(f"Low sleep: {signal.sleep_hours}h (below 6h threshold)")
            recommendations.append("Improve sleep hygiene, aim for 7-8 hours")
            risk_level = "high"

        if signal.steps < 3000:
            factors.append(f"Low activity: {signal.steps} steps (below 3000)")
            recommendations.append("Increase daily physical activity")
            if risk_level != "high":
                risk_level = "moderate"

        if signal.stress_score > 70:
            factors.append(f"High stress: {signal.stress_score} (above 70)")
            recommendations.append("Consider stress management techniques")
            risk_level = "high"

        if signal.heart_rate_rest > 90:
            factors.append(f"Elevated resting heart rate: {signal.heart_rate_rest}bpm")
            recommendations.append("Monitor heart rate, consult physician if persistent")
            risk_level = "critical"

        if not factors:
            factors.append("All metrics within normal range")
            recommendations.append("Maintain current health routine")

        summary = f"Health status: {risk_level}. {len(factors)} factor(s) identified."

        result = SignalInterpretation(
            summary=summary,
            risk_level=risk_level,
            contributing_factors=factors,
            recommendations=recommendations,
        )
        return result.model_dump(mode="json")
