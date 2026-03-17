from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime


class SignalInterpretation(BaseModel):
    summary: str
    risk_level: Literal["low", "moderate", "high", "critical"]
    contributing_factors: List[str]
    recommendations: List[str]


class TriageResult(BaseModel):
    incident_id: str
    priority: Literal["P1", "P2", "P3", "P4"]
    category: str
    requires_immediate_action: bool
    reasoning: str


class RemediationPlan(BaseModel):
    incident_id: str
    actions: List[str]
    timeline: str
    expected_outcome: str
    confidence: float


class Explanation(BaseModel):
    incident_id: str
    what_happened: str
    why_it_matters: str
    what_to_do: str
    plain_language_summary: str


class Postmortem(BaseModel):
    incident_id: str
    title: str
    summary: str
    root_cause: str
    impact: str
    lessons_learned: List[str]
    action_items: List[str]
    timestamp: datetime
