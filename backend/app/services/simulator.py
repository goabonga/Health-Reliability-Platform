import random
from datetime import datetime, timezone

from app.models.signals import HealthSignal


def generate_signal() -> HealthSignal:
    return HealthSignal(
        timestamp=datetime.now(timezone.utc),
        sleep_hours=round(random.uniform(3.0, 9.0), 1),
        steps=random.randint(500, 15000),
        stress_score=round(random.uniform(10.0, 95.0), 1),
        heart_rate_rest=random.randint(55, 110),
    )
