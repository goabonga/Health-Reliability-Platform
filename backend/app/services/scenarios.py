from dataclasses import dataclass, field
from typing import List
from datetime import datetime, timezone

from app.models.signals import HealthSignal


@dataclass
class ScenarioStep:
    sleep_hours: float
    steps: int
    stress_score: float
    heart_rate_rest: int


SCENARIOS: dict[str, List[ScenarioStep]] = {
    "sleep_degradation": [
        ScenarioStep(sleep_hours=7.5, steps=8000, stress_score=30, heart_rate_rest=65),
        ScenarioStep(sleep_hours=7.0, steps=7500, stress_score=35, heart_rate_rest=68),
        ScenarioStep(sleep_hours=6.5, steps=6000, stress_score=45, heart_rate_rest=70),
        ScenarioStep(sleep_hours=5.5, steps=5000, stress_score=55, heart_rate_rest=75),
        ScenarioStep(sleep_hours=4.5, steps=4000, stress_score=65, heart_rate_rest=80),
        ScenarioStep(sleep_hours=3.5, steps=3500, stress_score=75, heart_rate_rest=85),
        ScenarioStep(sleep_hours=3.0, steps=2500, stress_score=80, heart_rate_rest=92),
        ScenarioStep(sleep_hours=4.0, steps=3000, stress_score=72, heart_rate_rest=88),
        ScenarioStep(sleep_hours=5.0, steps=4500, stress_score=60, heart_rate_rest=78),
        ScenarioStep(sleep_hours=6.5, steps=6000, stress_score=45, heart_rate_rest=70),
        ScenarioStep(sleep_hours=7.0, steps=8000, stress_score=35, heart_rate_rest=65),
        ScenarioStep(sleep_hours=7.5, steps=9000, stress_score=25, heart_rate_rest=62),
    ],
    "recovery": [
        ScenarioStep(sleep_hours=3.0, steps=1500, stress_score=85, heart_rate_rest=95),
        ScenarioStep(sleep_hours=3.5, steps=2000, stress_score=80, heart_rate_rest=90),
        ScenarioStep(sleep_hours=4.5, steps=3000, stress_score=70, heart_rate_rest=85),
        ScenarioStep(sleep_hours=5.5, steps=4500, stress_score=60, heart_rate_rest=78),
        ScenarioStep(sleep_hours=6.0, steps=5500, stress_score=50, heart_rate_rest=72),
        ScenarioStep(sleep_hours=6.5, steps=7000, stress_score=40, heart_rate_rest=68),
        ScenarioStep(sleep_hours=7.0, steps=8500, stress_score=30, heart_rate_rest=65),
        ScenarioStep(sleep_hours=7.5, steps=10000, stress_score=25, heart_rate_rest=62),
        ScenarioStep(sleep_hours=8.0, steps=11000, stress_score=20, heart_rate_rest=60),
        ScenarioStep(sleep_hours=8.0, steps=12000, stress_score=18, heart_rate_rest=58),
    ],
    "low_activity": [
        ScenarioStep(sleep_hours=7.0, steps=8000, stress_score=30, heart_rate_rest=65),
        ScenarioStep(sleep_hours=7.0, steps=5000, stress_score=35, heart_rate_rest=68),
        ScenarioStep(sleep_hours=6.5, steps=3000, stress_score=40, heart_rate_rest=70),
        ScenarioStep(sleep_hours=6.0, steps=2000, stress_score=50, heart_rate_rest=72),
        ScenarioStep(sleep_hours=6.0, steps=1500, stress_score=55, heart_rate_rest=75),
        ScenarioStep(sleep_hours=5.5, steps=1000, stress_score=65, heart_rate_rest=78),
        ScenarioStep(sleep_hours=5.0, steps=800, stress_score=72, heart_rate_rest=82),
        ScenarioStep(sleep_hours=5.5, steps=2000, stress_score=60, heart_rate_rest=76),
        ScenarioStep(sleep_hours=6.0, steps=4000, stress_score=45, heart_rate_rest=70),
        ScenarioStep(sleep_hours=7.0, steps=7000, stress_score=30, heart_rate_rest=65),
        ScenarioStep(sleep_hours=7.5, steps=9000, stress_score=25, heart_rate_rest=62),
    ],
}


class ScenarioRunner:
    def __init__(self) -> None:
        self.active_scenario: str | None = None
        self._step_index: int = 0
        self._steps: List[ScenarioStep] = []

    def set_scenario(self, name: str) -> bool:
        if name not in SCENARIOS:
            return False
        self.active_scenario = name
        self._steps = SCENARIOS[name]
        self._step_index = 0
        return True

    def clear_scenario(self) -> None:
        self.active_scenario = None
        self._steps = []
        self._step_index = 0

    def get_signal(self) -> HealthSignal | None:
        if not self._steps:
            return None
        step = self._steps[self._step_index % len(self._steps)]
        self._step_index += 1
        return HealthSignal(
            timestamp=datetime.now(timezone.utc),
            sleep_hours=step.sleep_hours,
            steps=step.steps,
            stress_score=step.stress_score,
            heart_rate_rest=step.heart_rate_rest,
        )

    @property
    def available_scenarios(self) -> List[str]:
        return list(SCENARIOS.keys())

    @property
    def status(self) -> dict:
        return {
            "active_scenario": self.active_scenario,
            "step": self._step_index,
            "total_steps": len(self._steps),
            "available": self.available_scenarios,
        }


scenario_runner = ScenarioRunner()
