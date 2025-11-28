# src/utils/logger.py
"""
Lightweight console-only observability utilities.

- new_trace_id(): produce short trace ids for request correlation
- log_event(): structured info-level events (prints JSON-ish lines)
- log_error(): structured error-level events (with stack trace)
- timed(): context manager to measure duration for a block

Console-only (no file writes) — ideal for Kaggle/Notebook and dev machines.
"""

import logging
import time
import uuid
import json
import traceback
from typing import Any, Dict, Optional, Callable, ContextManager
from contextlib import contextmanager

# Configure root logger for console-only JSON like output
_logger = logging.getLogger("stocker")
if not _logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    # simple formatter — we will output JSON ourselves
    ch.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(ch)
_logger.setLevel(logging.INFO)


def new_trace_id(prefix: str = "t") -> str:
    """Return a short trace id (convenient for console logs)."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def _safe_serialize(payload: Any) -> Any:
    """Try to serialize; fall back to string representation when needed."""
    try:
        json.dumps(payload)
        return payload
    except Exception:
        try:
            return str(payload)
        except Exception:
            return "<unserializable>"


def log_event(
    trace: Optional[str],
    event: str,
    level: str = "info",
    details: Optional[Dict[str, Any]] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> None:
    """Log a structured event to console."""
    payload = {
        "ts": int(time.time()),
        "trace": trace,
        "event": event,
        "level": level,
        "details": _safe_serialize(details or {}),
    }
    if extra:
        payload["extra"] = _safe_serialize(extra)

    # print JSON-ish one-liner for easy grepping and parsing
    line = json.dumps(payload, default=str, ensure_ascii=False)
    if level in ("warn", "warning"):
        _logger.warning(line)
    elif level in ("error", "err"):
        _logger.error(line)
    else:
        _logger.info(line)


def log_error(trace: Optional[str], message: str, exc: Optional[Exception] = None) -> None:
    """Log an error-level event with traceback (if provided)."""
    tb = None
    if exc:
        tb = traceback.format_exc()
    payload = {
        "ts": int(time.time()),
        "trace": trace,
        "event": "error",
        "message": message,
        "exception": str(exc) if exc else None,
        "traceback": tb,
    }
    _logger.error(json.dumps(payload, default=str, ensure_ascii=False))


@contextmanager
def timed(trace: Optional[str], name: str):
    """Context manager to measure duration; logs start/end automatically."""
    start = time.time()
    log_event(trace, f"{name}.start", details={"name": name})
    try:
        yield
    except Exception as e:
        log_error(trace, f"Exception in timed block {name}", e)
        raise
    finally:
        duration = time.time() - start
        log_event(trace, f"{name}.end", details={"name": name, "duration_s": round(duration, 4)})
