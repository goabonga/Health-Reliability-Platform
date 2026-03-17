from pydantic import BaseModel
from datetime import datetime
from typing import Literal


class Incident(BaseModel):
    id: str
    timestamp: datetime
    severity: Literal["low", "medium", "high", "critical"]
    title: str
    description: str
    source: str
    status: Literal["open", "mitigated", "resolved"] = "open"
