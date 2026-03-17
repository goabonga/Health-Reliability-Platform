from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class TimelineEvent(BaseModel):
    timestamp: datetime
    event_type: Literal["signal", "slo", "agent", "action", "incident", "system"]
    message: str
    details: dict | None = None
