from fastapi import FastAPI

app = FastAPI(title="Health Reliability Platform", version="0.1.0")


@app.get("/health")
async def health():
    return {"status": "ok"}
