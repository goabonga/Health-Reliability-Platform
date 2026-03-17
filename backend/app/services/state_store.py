from datetime import datetime, timezone
from typing import List

from app.models.signals import HealthSignal
from app.models.incident import Incident
from app.models.action import Action
from app.models.timeline import TimelineEvent


class StateStore:
    def __init__(self) -> None:
        self.signals: List[HealthSignal] = []
        self.incidents: List[Incident] = []
        self.actions: List[Action] = []
        self.timeline: List[TimelineEvent] = []
        self.postmortems: List[dict] = []

    def add_signal(self, signal: HealthSignal) -> None:
        self.signals.append(signal)
        if len(self.signals) > 100:
            self.signals = self.signals[-100:]

    def add_incident(self, incident: Incident) -> None:
        self.incidents.append(incident)

    def has_open_incident(self, title: str) -> bool:
        return any(
            i.title == title and i.status == "open"
            for i in self.incidents
        )

    def get_open_incidents(self) -> List[Incident]:
        return [i for i in self.incidents if i.status == "open"]

    def mitigate_incident(self, incident_id: str) -> Incident | None:
        for i, inc in enumerate(self.incidents):
            if inc.id == incident_id and inc.status == "open":
                updated = inc.model_copy(update={"status": "mitigated"})
                self.incidents[i] = updated
                return updated
        return None

    def resolve_incident(self, incident_id: str) -> Incident | None:
        for i, inc in enumerate(self.incidents):
            if inc.id == incident_id and inc.status in ("open", "mitigated"):
                updated = inc.model_copy(update={"status": "resolved"})
                self.incidents[i] = updated
                return updated
        return None

    def add_action(self, action: Action) -> None:
        self.actions.append(action)

    def add_timeline_event(self, event: TimelineEvent) -> None:
        self.timeline.append(event)
        if len(self.timeline) > 500:
            self.timeline = self.timeline[-500:]

    def add_postmortem(self, postmortem: dict) -> None:
        self.postmortems.append(postmortem)

    def get_latest_signal(self) -> HealthSignal | None:
        return self.signals[-1] if self.signals else None

    def get_state(self) -> dict:
        return {
            "latest_signal": self.get_latest_signal(),
            "total_signals": len(self.signals),
            "open_incidents": [i for i in self.incidents if i.status == "open"],
            "total_incidents": len(self.incidents),
            "recent_actions": self.actions[-10:],
            "total_actions": len(self.actions),
            "postmortems": self.postmortems[-5:],
        }

    def clear(self) -> None:
        self.signals.clear()
        self.incidents.clear()
        self.actions.clear()
        self.timeline.clear()
        self.postmortems.clear()


store = StateStore()
