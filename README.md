# Health Reliability Platform

A multi-agent AI platform that treats health like a production system — with SLO-based monitoring, incident detection, AI-driven remediation, and SRE-style observability.

## Architecture

```
┌─────────────┐    ┌──────────────┐    ┌───────────────────┐
│  Frontend    │◄──►│  FastAPI      │◄──►│  Agent System     │
│  Dashboard   │    │  Backend      │    │                   │
│  (React)     │    │              │    │  signal-interpreter│
│              │    │  /signals    │    │  incident-triage   │
│              │    │  /incidents  │    │  remediation-planner│
│              │    │  /timeline   │    │  explainability    │
│              │    │  /state      │    │  postmortem        │
└─────────────┘    └──────────────┘    └───────────────────┘
                          │
                   ┌──────┴──────┐
                   │  SLO Engine │
                   │  Simulator  │
                   │  State Store│
                   └─────────────┘
```

## Quick Start

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend proxies API requests to the backend on port 8000.

### With AI Agents (optional)

```bash
export MISTRAL_API_KEY=your_key_here
export USE_AI_AGENTS=true
uvicorn app.main:app --reload --port 8000
```

Without the API key, the system uses deterministic mock agents.

## Demo Scenarios

Use the scenario selector in the dashboard or the API:

| Scenario | Description |
|---|---|
| `sleep_degradation` | Health degrades then recovers (sleep focus) |
| `recovery` | Start in critical state, gradual recovery |
| `low_activity` | Activity drops triggering cascading alerts |

```bash
# Activate a scenario
curl -X POST http://localhost:8000/scenarios/sleep_degradation

# Stop scenario (return to random)
curl -X POST http://localhost:8000/scenarios/stop
```

## Demo Flow

1. Dashboard shows healthy state (all SLOs green)
2. Signals degrade over time
3. SLO violations trigger incidents
4. AI agents triage, plan remediation, explain
5. Actions are displayed in real-time
6. System recovers, incidents resolve
7. Postmortem is automatically generated

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/signals` | Latest health signal |
| GET | `/signals/history` | Signal history |
| GET | `/slo/evaluate` | Current SLO status |
| GET | `/slo/config` | SLO configuration |
| GET | `/incidents` | All incidents |
| GET | `/incidents/open` | Open incidents only |
| GET | `/actions` | Remediation actions |
| GET | `/postmortems` | Generated postmortems |
| GET | `/state` | Full system state |
| GET | `/timeline` | Event timeline |
| POST | `/orchestrator/start` | Start monitoring |
| POST | `/orchestrator/stop` | Stop monitoring |
| GET | `/orchestrator/status` | Orchestrator status |
| GET | `/scenarios` | Available scenarios |
| POST | `/scenarios/{name}` | Activate scenario |
| POST | `/scenarios/stop` | Stop scenario |

## Tech Stack

- **Backend**: Python 3.12+, FastAPI, Pydantic v2
- **Frontend**: React 19, TypeScript, TailwindCSS, Vite
- **AI Agents**: Mistral AI (with deterministic mock fallback)
- **Testing**: pytest, pytest-asyncio

## Project Structure

```
backend/
  app/
    agents/          # AI agent implementations (mock + Mistral)
      prompts/       # Prompt templates for Mistral
    models/          # Pydantic schemas (signals, SLO, incidents, etc.)
    services/        # Business logic (simulator, SLO engine, orchestrator)
    main.py          # FastAPI app entry point
  tests/             # Test suite
frontend/
  src/
    components/      # React dashboard panels
    hooks/           # API polling hooks
    types.ts         # TypeScript interfaces
```

## Running Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```
