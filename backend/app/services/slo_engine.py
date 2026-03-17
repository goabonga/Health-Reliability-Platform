import operator as op
from typing import List

from app.models.signals import HealthSignal
from app.models.slo import SLOConfig, SLOResult

OPERATORS = {
    ">=": op.ge,
    "<=": op.le,
    ">": op.gt,
    "<": op.lt,
}

DEFAULT_SLOS: List[SLOConfig] = [
    SLOConfig(name="Sleep SLO", metric="sleep_hours", operator=">=", threshold=6.0),
    SLOConfig(name="Activity SLO", metric="steps", operator=">=", threshold=3000),
    SLOConfig(name="Stress SLO", metric="stress_score", operator="<=", threshold=70.0),
    SLOConfig(name="Heart Rate SLO", metric="heart_rate_rest", operator="<=", threshold=90),
]


def evaluate_slos(signal: HealthSignal, slos: List[SLOConfig] | None = None) -> List[SLOResult]:
    slos = slos or DEFAULT_SLOS
    results = []
    for slo in slos:
        current_value = getattr(signal, slo.metric)
        comparator = OPERATORS[slo.operator]
        passed = comparator(float(current_value), float(slo.threshold))
        results.append(
            SLOResult(
                slo_name=slo.name,
                metric=slo.metric,
                current_value=float(current_value),
                threshold=slo.threshold,
                operator=slo.operator,
                passed=passed,
            )
        )
    return results
