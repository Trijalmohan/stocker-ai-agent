# src/utils/metrics.py
"""
Very small in-memory metrics collector.

- increment(counter_name)
- gauge(metric_name, value)
- timing(metric_name, seconds)
- snapshot() -> returns a POJO of metrics

Console-only; safe to use in notebooks and unit tests.
"""

import time
from threading import Lock
from typing import Dict, Any

_lock = Lock()
_counters: Dict[str, int] = {}
_gauges: Dict[str, float] = {}
_timings: Dict[str, list] = {}


def increment(name: str, by: int = 1) -> None:
    with _lock:
        _counters[name] = _counters.get(name, 0) + by


def gauge(name: str, value: float) -> None:
    with _lock:
        _gauges[name] = float(value)


def timing(name: str, value: float) -> None:
    with _lock:
        arr = _timings.setdefault(name, [])
        arr.append(float(value))


def snapshot() -> Dict[str, Any]:
    """Return a copy of the current metrics for reporting."""
    with _lock:
        return {
            "counters": dict(_counters),
            "gauges": dict(_gauges),
            "timings": {k: list(v) for k, v in _timings.items()},
            "ts": int(time.time())
        }


def reset_all() -> None:
    """Reset metrics (useful in tests)."""
    with _lock:
        _counters.clear()
        _gauges.clear()
        _timings.clear()
