from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.signals import HealthSignal
from app.models.slo import SLOResult
from app.models.incident import Incident
from app.services.simulator import generate_signal
from app.services.slo_engine import evaluate_slos
from app.services.incident_detector import detect_incidents

app = FastAPI(title="Health Reliability Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    signal = generate_signal()
    slo_results = evaluate_slos(signal)
    return detect_incidents(slo_results)
