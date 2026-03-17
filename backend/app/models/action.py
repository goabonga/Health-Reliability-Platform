from pydantic import BaseModel
from datetime import datetime


class Action(BaseModel):
    id: str
    timestamp: datetime
    incident_id: str
    action_type: str
    description: str
    agent: str
