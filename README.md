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
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Tech Stack

- **Backend**: Python, FastAPI, Pydantic
- **Frontend**: React, TailwindCSS
- **AI Agents**: Mistral (with mock fallback)

## Project Structure

```
backend/           # FastAPI application
  app/
    agents/        # AI agent implementations
    models/        # Pydantic schemas
    services/      # Business logic
    main.py        # App entry point
frontend/          # React dashboard
docs/              # Documentation
```
