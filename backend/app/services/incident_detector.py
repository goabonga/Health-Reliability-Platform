import uuid
from datetime import datetime, timezone
from typing import List

from app.models.incident import Incident
from app.models.slo import SLOResult

SEVERITY_MAP = {
    "Sleep SLO": "high",
    "Activity SLO": "medium",
    "Stress SLO": "high",
    "Heart Rate SLO": "critical",
}


def detect_incidents(slo_results: List[SLOResult]) -> List[Incident]:
    incidents = []
    for result in slo_results:
        if not result.passed:
            severity = SEVERITY_MAP.get(result.slo_name, "medium")
            incidents.append(
                Incident(
                    id=str(uuid.uuid4())[:8],
                    timestamp=datetime.now(timezone.utc),
                    severity=severity,
                    title=f"{result.slo_name} violation",
                    description=(
                        f"{result.metric} = {result.current_value} "
                        f"(threshold: {result.operator} {result.threshold})"
                    ),
                    source="slo-engine",
                )
            )
    return incidents
