from pydantic import BaseModel
from typing import Literal


class SLOConfig(BaseModel):
    name: str
    metric: str
    operator: Literal[">=", "<=", ">", "<"]
    threshold: float


class SLOResult(BaseModel):
    slo_name: str
    metric: str
    current_value: float
    threshold: float
    operator: str
    passed: bool
