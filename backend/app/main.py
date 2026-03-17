from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.models.signals import HealthSignal
from app.models.slo import SLOResult, SLOConfig
from app.models.incident import Incident
from app.models.timeline import TimelineEvent
from app.models.action import Action
from app.services.simulator import generate_signal
from app.services.slo_engine import evaluate_slos, DEFAULT_SLOS
from app.services.incident_detector import detect_incidents
from app.services.state_store import store
from app.services.orchestrator import orchestrator
from app.services.scenarios import scenario_runner

app = FastAPI(title="Health Reliability Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "internal_server_error", "message": str(exc)},
    )


@app.on_event("startup")
async def startup():
    orchestrator.start()


@app.on_event("shutdown")
async def shutdown():
    orchestrator.stop()


@app.get("/health")
async def health():
    return {"status": "ok", "orchestrator_running": orchestrator.is_running}


@app.get("/signals", response_model=HealthSignal)
async def get_signals():
    latest = store.get_latest_signal()
    if latest:
        return latest
    return generate_signal()


@app.get("/signals/history", response_model=List[HealthSignal])
async def get_signals_history():
    return store.signals


@app.get("/slo/evaluate", response_model=List[SLOResult])
async def slo_evaluate():
    latest = store.get_latest_signal()
    signal = latest if latest else generate_signal()
    return evaluate_slos(signal)


@app.get("/slo/config", response_model=List[SLOConfig])
async def get_slo_config():
    return DEFAULT_SLOS


@app.get("/incidents", response_model=List[Incident])
async def get_incidents():
    return store.incidents


@app.get("/incidents/open", response_model=List[Incident])
async def get_open_incidents():
    return store.get_open_incidents()


@app.get("/actions", response_model=List[Action])
async def get_actions():
    return store.actions


@app.get("/postmortems")
async def get_postmortems():
    return store.postmortems


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


@app.get("/scenarios")
async def get_scenarios():
    return scenario_runner.status


@app.post("/scenarios/{name}")
async def set_scenario(name: str):
    store.clear()
    if scenario_runner.set_scenario(name):
        return {"status": "active", "scenario": name}
    return JSONResponse(status_code=404, content={"error": f"Unknown scenario: {name}"})


@app.post("/scenarios/stop")
async def stop_scenario():
    scenario_runner.clear_scenario()
    return {"status": "stopped"}
