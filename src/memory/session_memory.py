# src/memory/session_memory.py

from typing import Any, Dict, List, Optional
from threading import Lock
import time

# In-memory store: { session_id: { messages: [...], last_strategy: {...}, ... } }
_SESSIONS: Dict[str, Dict[str, Any]] = {}
_LOCK = Lock()


def _get_or_create(session_id: str) -> Dict[str, Any]:
    """Get or create the per-session state dict."""
    with _LOCK:
        if session_id not in _SESSIONS:
            _SESSIONS[session_id] = {
                "messages": [],
                "last_strategy": None,
                "created_at": time.time(),
                "updated_at": time.time(),
            }
        return _SESSIONS[session_id]


def append_message(
    session_id: str,
    role: str,
    content: Any,
    meta: Optional[Dict[str, Any]] = None,
) -> None:
    """Append a message (user/assistant) to the session log."""
    s = _get_or_create(session_id)
    msg = {
        "role": role,
        "content": str(content),
        "meta": meta or {},
        "ts": time.time(),
    }
    s["messages"].append(msg)
    # keep it bounded (last 20 messages)
    if len(s["messages"]) > 20:
        s["messages"] = s["messages"][-20:]
    s["updated_at"] = time.time()


def get_recent_messages(session_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Return last N messages for a session (not used by UI yet, but handy)."""
    s = _SESSIONS.get(session_id)
    if not s:
        return []
    return s["messages"][-limit:]


def set_last_strategy(session_id: str, strategy: Dict[str, Any]) -> None:
    """Store the last generated strategy for this session."""
    s = _get_or_create(session_id)
    s["last_strategy"] = strategy
    s["updated_at"] = time.time()


def get_last_strategy(session_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve last generated strategy for this session."""
    s = _SESSIONS.get(session_id)
    if not s:
        return None
    return s.get("last_strategy")


def get_session_summary(session_id: str) -> Dict[str, Any]:
    """
    Lightweight summary for meta:
      { "messages": N, "has_last_strategy": bool }
    """
    s = _SESSIONS.get(session_id)
    if not s:
        return {"messages": 0, "has_last_strategy": False}
    return {
        "messages": len(s["messages"]),
        "has_last_strategy": s.get("last_strategy") is not None,
    }
