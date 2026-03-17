from datetime import datetime, timezone

from app.models.signals import HealthSignal
from app.models.slo import SLOConfig
from app.services.slo_engine import evaluate_slos


def _make_signal(**kwargs) -> HealthSignal:
    defaults = {
        "timestamp": datetime.now(timezone.utc),
        "sleep_hours": 7.0,
        "steps": 8000,
        "stress_score": 30.0,
        "heart_rate_rest": 65,
    }
    defaults.update(kwargs)
    return HealthSignal(**defaults)


def test_all_slos_pass_healthy_signal():
    signal = _make_signal()
    results = evaluate_slos(signal)
    assert all(r.passed for r in results)


def test_sleep_slo_fails():
    signal = _make_signal(sleep_hours=4.0)
    results = evaluate_slos(signal)
    sleep_result = next(r for r in results if r.metric == "sleep_hours")
    assert not sleep_result.passed
    assert sleep_result.current_value == 4.0


def test_stress_slo_fails():
    signal = _make_signal(stress_score=85.0)
    results = evaluate_slos(signal)
    stress_result = next(r for r in results if r.metric == "stress_score")
    assert not stress_result.passed


def test_heart_rate_slo_fails():
    signal = _make_signal(heart_rate_rest=95)
    results = evaluate_slos(signal)
    hr_result = next(r for r in results if r.metric == "heart_rate_rest")
    assert not hr_result.passed


def test_boundary_values():
    signal = _make_signal(sleep_hours=6.0, steps=3000, stress_score=70.0, heart_rate_rest=90)
    results = evaluate_slos(signal)
    assert all(r.passed for r in results)


def test_custom_slos():
    custom = [SLOConfig(name="Custom", metric="sleep_hours", operator=">=", threshold=8.0)]
    signal = _make_signal(sleep_hours=7.0)
    results = evaluate_slos(signal, custom)
    assert len(results) == 1
    assert not results[0].passed
