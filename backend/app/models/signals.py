from pydantic import BaseModel
from datetime import datetime


class HealthSignal(BaseModel):
    timestamp: datetime
    sleep_hours: float
    steps: int
    stress_score: float
    heart_rate_rest: int
