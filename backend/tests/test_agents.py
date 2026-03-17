import pytest
from datetime import datetime, timezone

from app.agents.signal_interpreter import MockSignalInterpreter
from app.agents.incident_triage import MockIncidentTriage
from app.agents.remediation_planner import MockRemediationPlanner
from app.agents.explainability_agent import MockExplainabilityAgent
from app.agents.postmortem_agent import MockPostmortemAgent
from app.models.agent_schemas import (
    SignalInterpretation,
    TriageResult,
    RemediationPlan,
    Explanation,
    Postmortem,
)


def _signal_data(**kwargs):
    defaults = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sleep_hours": 7.0,
        "steps": 8000,
        "stress_score": 30.0,
        "heart_rate_rest": 65,
    }
    defaults.update(kwargs)
    return defaults


def _incident_data(**kwargs):
    defaults = {
        "id": "test-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "severity": "high",
        "title": "Sleep SLO violation",
        "description": "sleep_hours = 3.0 (threshold: >= 6.0)",
        "source": "slo-engine",
        "status": "open",
    }
    defaults.update(kwargs)
    return defaults


@pytest.mark.asyncio
async def test_signal_interpreter_healthy():
    agent = MockSignalInterpreter()
    result = await agent.run({"signal": _signal_data()})
    parsed = SignalInterpretation.model_validate(result)
    assert parsed.risk_level == "low"


@pytest.mark.asyncio
async def test_signal_interpreter_unhealthy():
    agent = MockSignalInterpreter()
    result = await agent.run({"signal": _signal_data(sleep_hours=3.0, stress_score=80.0)})
    parsed = SignalInterpretation.model_validate(result)
    assert parsed.risk_level == "high"
    assert len(parsed.contributing_factors) >= 2


@pytest.mark.asyncio
async def test_incident_triage():
    agent = MockIncidentTriage()
    result = await agent.run({"incident": _incident_data()})
    parsed = TriageResult.model_validate(result)
    assert parsed.priority == "P2"
    assert parsed.requires_immediate_action is True


@pytest.mark.asyncio
async def test_remediation_planner():
    agent = MockRemediationPlanner()
    result = await agent.run({"incident": _incident_data()})
    parsed = RemediationPlan.model_validate(result)
    assert len(parsed.actions) >= 2
    assert 0 < parsed.confidence <= 1.0


@pytest.mark.asyncio
async def test_explainability():
    agent = MockExplainabilityAgent()
    result = await agent.run({"incident": _incident_data()})
    parsed = Explanation.model_validate(result)
    assert parsed.plain_language_summary
    assert parsed.what_to_do


@pytest.mark.asyncio
async def test_postmortem():
    agent = MockPostmortemAgent()
    result = await agent.run({"incident": _incident_data(status="resolved")})
    parsed = Postmortem.model_validate(result)
    assert "Postmortem" in parsed.title
    assert len(parsed.lessons_learned) >= 1


@pytest.mark.asyncio
async def test_unknown_incident_uses_defaults():
    agent = MockRemediationPlanner()
    result = await agent.run({"incident": _incident_data(title="Unknown SLO violation")})
    parsed = RemediationPlan.model_validate(result)
    assert len(parsed.actions) >= 1
