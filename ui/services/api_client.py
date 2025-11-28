# ui/services/api_client.py
import requests

BACKEND_URL = "http://127.0.0.1:8000/api/handle"

def call_backend(message=None, intent=None, payload=None, session_id="ui-session"):
    body = {
        "message": message,
        "session_id": session_id,
        "intent": intent,
        "payload": payload or {}
    }

    try:
        r = requests.post(BACKEND_URL, json=body, timeout=30)
        return r.json()
    except Exception as e:
        return {"response": {"error": str(e)}}
