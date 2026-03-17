from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.signals import HealthSignal
from app.models.slo import SLOResult
from app.models.incident import Incident
from app.models.timeline import TimelineEvent
from app.models.action import Action
from app.services.simulator import generate_signal
from app.services.slo_engine import evaluate_slos
from app.services.incident_detector import detect_incidents
from app.services.state_store import store
from app.services.orchestrator import orchestrator

app = FastAPI(title="Health Reliability Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    orchestrator.start()


@app.on_event("shutdown")
async def shutdown():
    orchestrator.stop()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/signals", response_model=HealthSignal)
async def get_signals():
    return generate_signal()


@app.get("/slo/evaluate", response_model=List[SLOResult])
async def slo_evaluate():
    signal = generate_signal()
    return evaluate_slos(signal)


@app.get("/incidents", response_model=List[Incident])
async def get_incidents():
    return store.incidents


@app.get("/actions", response_model=List[Action])
async def get_actions():
    return store.actions


@app.get("/state")
async def get_state():
    return store.get_state()


@app.get("/timeline", response_model=List[TimelineEvent])
async def get_timeline():
    return list(reversed(store.timeline))


@app.post("/orchestrator/start")
async def start_orchestrator():
    orchestrator.start()
    return {"status": "started"}


@app.post("/orchestrator/stop")
async def stop_orchestrator():
    orchestrator.stop()
    return {"status": "stopped"}


@app.get("/orchestrator/status")
async def orchestrator_status():
    return {"running": orchestrator.is_running}
