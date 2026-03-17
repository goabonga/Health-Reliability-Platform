from datetime import datetime, timezone

from app.models.signals import HealthSignal
from app.services.slo_engine import evaluate_slos
from app.services.incident_detector import detect_incidents


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


def test_no_incidents_healthy_signal():
    signal = _make_signal()
    slos = evaluate_slos(signal)
    incidents = detect_incidents(slos)
    assert len(incidents) == 0


def test_incident_created_for_slo_violation():
    signal = _make_signal(sleep_hours=3.0)
    slos = evaluate_slos(signal)
    incidents = detect_incidents(slos)
    assert len(incidents) == 1
    assert incidents[0].title == "Sleep SLO violation"
    assert incidents[0].severity == "high"


def test_multiple_incidents():
    signal = _make_signal(sleep_hours=3.0, heart_rate_rest=100, stress_score=90.0, steps=500)
    slos = evaluate_slos(signal)
    incidents = detect_incidents(slos)
    assert len(incidents) == 4


def test_incident_has_valid_fields():
    signal = _make_signal(heart_rate_rest=100)
    slos = evaluate_slos(signal)
    incidents = detect_incidents(slos)
    inc = incidents[0]
    assert inc.id
    assert inc.timestamp
    assert inc.status == "open"
    assert inc.source == "slo-engine"
