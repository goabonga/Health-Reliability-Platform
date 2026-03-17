from datetime import datetime, timezone

from app.models.signals import HealthSignal
from app.models.incident import Incident
from app.services.state_store import StateStore


def _make_signal():
    return HealthSignal(
        timestamp=datetime.now(timezone.utc),
        sleep_hours=7.0,
        steps=8000,
        stress_score=30.0,
        heart_rate_rest=65,
    )


def _make_incident(title="Test incident", status="open"):
    return Incident(
        id="test-001",
        timestamp=datetime.now(timezone.utc),
        severity="high",
        title=title,
        description="test",
        source="test",
        status=status,
    )


def test_add_signal():
    s = StateStore()
    s.add_signal(_make_signal())
    assert len(s.signals) == 1
    assert s.get_latest_signal() is not None


def test_signal_limit():
    s = StateStore()
    for _ in range(150):
        s.add_signal(_make_signal())
    assert len(s.signals) == 100


def test_add_incident():
    s = StateStore()
    s.add_incident(_make_incident())
    assert len(s.incidents) == 1


def test_has_open_incident():
    s = StateStore()
    s.add_incident(_make_incident(title="Sleep SLO violation"))
    assert s.has_open_incident("Sleep SLO violation")
    assert not s.has_open_incident("Activity SLO violation")


def test_resolve_incident():
    s = StateStore()
    s.add_incident(_make_incident())
    resolved = s.resolve_incident("test-001")
    assert resolved is not None
    assert resolved.status == "resolved"
    assert not s.has_open_incident("Test incident")


def test_clear():
    s = StateStore()
    s.add_signal(_make_signal())
    s.add_incident(_make_incident())
    s.clear()
    assert len(s.signals) == 0
    assert len(s.incidents) == 0


def test_get_state():
    s = StateStore()
    s.add_signal(_make_signal())
    state = s.get_state()
    assert "latest_signal" in state
    assert "total_signals" in state
    assert state["total_signals"] == 1
