from datetime import datetime, timezone
from typing import List

from app.models.timeline import TimelineEvent
from app.models.signals import HealthSignal
from app.models.slo import SLOResult
from app.models.incident import Incident
from app.models.action import Action


def signal_event(signal: HealthSignal) -> TimelineEvent:
    return TimelineEvent(
        timestamp=signal.timestamp,
        event_type="signal",
        message=f"Signal received: sleep={signal.sleep_hours}h, steps={signal.steps}, stress={signal.stress_score}, hr={signal.heart_rate_rest}",
        details=signal.model_dump(mode="json"),
    )


def slo_event(results: List[SLOResult]) -> TimelineEvent:
    violations = [r for r in results if not r.passed]
    if violations:
        names = ", ".join(r.slo_name for r in violations)
        message = f"SLO violations detected: {names}"
    else:
        message = "All SLOs passing"
    return TimelineEvent(
        timestamp=datetime.now(timezone.utc),
        event_type="slo",
        message=message,
        details={"results": [r.model_dump(mode="json") for r in results]},
    )


def incident_event(incident: Incident) -> TimelineEvent:
    return TimelineEvent(
        timestamp=incident.timestamp,
        event_type="incident",
        message=f"[{incident.severity.upper()}] {incident.title}",
        details=incident.model_dump(mode="json"),
    )


def action_event(action: Action) -> TimelineEvent:
    return TimelineEvent(
        timestamp=action.timestamp,
        event_type="action",
        message=f"Action by {action.agent}: {action.description}",
        details=action.model_dump(mode="json"),
    )


def agent_event(agent_name: str, message: str, details: dict | None = None) -> TimelineEvent:
    return TimelineEvent(
        timestamp=datetime.now(timezone.utc),
        event_type="agent",
        message=f"[{agent_name}] {message}",
        details=details,
    )
