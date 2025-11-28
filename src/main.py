# src/main.py
"""
Main FastAPI entrypoint — now with full Observability Pack:
- Request logging
- Metrics counters
- Error logging
- Execution time tracking
"""

import time
from typing import Any, Dict
from fastapi import Body
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.orchestrator import orch

# ------------------------------
# Metrics Storage
# ------------------------------

METRICS = {
    "total_calls": 0,
    "intent_calls": {},      # count per intent
    "errors": 0,
    "avg_latency_ms": 0.0,
}

# ------------------------------
# Create App
# ------------------------------

app = FastAPI(
    title="Stocker AI Backend",
    version="2.0",
    description="AI-powered trading assistant with indicators, strategies, backtests, and observability."
)

# ------------------------------
# Helper — update metrics
# ------------------------------

def update_metrics(intent: str, elapsed_ms: float, error: bool):
    METRICS["total_calls"] += 1
    METRICS["avg_latency_ms"] = (
        (METRICS["avg_latency_ms"] * (METRICS["total_calls"] - 1) + elapsed_ms)
        / METRICS["total_calls"]
    )

    if intent not in METRICS["intent_calls"]:
        METRICS["intent_calls"][intent] = 0
    METRICS["intent_calls"][intent] += 1

    if error:
        METRICS["errors"] += 1

# ------------------------------
# Observer Logging
# ------------------------------

def log_request(intent: str, session_id: str, payload: Dict):
    print("\n" + "=" * 60)
    print(f"[REQUEST] intent={intent}, session_id={session_id}")
    print(f"payload: {payload}")
    print("=" * 60 + "\n")

def log_response(intent: str, session_id: str, resp: Dict, elapsed_ms: float):
    print(f"[RESPONSE] intent={intent}, session_id={session_id}")
    print(f"took: {elapsed_ms:.2f} ms")
    print(f"keys returned: {list(resp.keys())}")
    print("-" * 60)

def log_error(intent: str, error_msg: str):
    print(f"[ERROR] {intent}: {error_msg}")

# ------------------------------
# API ENDPOINT — RAW JSON VERSION (RECOMMENDED)
# ------------------------------

@app.post("/api/handle")
async def handle_api(body: Dict = Body(...)):

    message = body.get("message", "")
    session_id = body.get("session_id", "default")
    intent = body.get("intent", "")
    payload = body.get("payload", {}) or {}

    # --- Observability ---
    log_request(intent, session_id, payload)
    start = time.time()

    try:
        resp = orch.handle(session_id, intent, payload, message)
        elapsed_ms = (time.time() - start) * 1000.0

        log_response(intent, session_id, resp, elapsed_ms)
        update_metrics(intent, elapsed_ms, error=False)

        return JSONResponse(content=resp)

    except Exception as e:
        elapsed_ms = (time.time() - start) * 1000.0

        log_error(intent, str(e))
        update_metrics(intent, elapsed_ms, error=True)

        return JSONResponse(
            content={
                "session_id": session_id,
                "response": {
                    "error": "internal_server_error",
                    "details": str(e)
                }
            }
        )

# ------------------------------
# Metrics Endpoint
# ------------------------------

@app.get("/metrics")
def get_metrics():
    return METRICS

# ------------------------------
# Health Check
# ------------------------------

@app.get("/health")
def health():
    return {"status": "ok", "uptime_sec": time.time()}
