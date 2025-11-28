# src/memory/memory_service.py
from typing import Dict, Any
import uuid
import time

class MemoryService:
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.longterm: Dict[str, Dict[str, Any]] = {}

    def create_session(self, user_id: str) -> str:
        sid = str(uuid.uuid4())
        self.sessions[sid] = {
            "user_id": user_id,
            "created_at": time.time(),
            "history": [],
            "profile": {     # NEW
                "level": "basic",
                "style": "simple",
                "last_topic": None
            }
        }
        return sid

    def append_history(self, session_id: str, entry: str):
        if session_id in self.sessions:
            self.sessions[session_id]["history"].append({
                "ts": time.time(),
                "text": entry
            })

    def get_history(self, session_id: str):
        return self.sessions.get(session_id, {}).get("history", [])

    def update_profile(self, session_id: str, updates: dict):
        if session_id in self.sessions:
            self.sessions[session_id]["profile"].update(updates)

    def get_profile(self, session_id: str):
        return self.sessions.get(session_id, {}).get("profile", {})
