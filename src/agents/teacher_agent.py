from google import genai
import os
from src.database.conversation import get_history

class TeacherAgent:
    def __init__(self, memory=None):
        self.memory = memory
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "models/gemini-2.5-flash"

    def explain(self, session_id: str, topic: str, level: str = "basic"):
        # ---- Get conversation history ----
        history = get_history(session_id)

        formatted_history = "\n".join(
            f"{h['role'].upper()}: {h['message']}" for h in history
        )

        system_prompt = f"""
You are a concise financial tutor.
Keep answers short (5-7 sentences). Use bullet points when helpful.
Use previous conversation context when relevant.

Conversation so far:
{formatted_history}

Only provide long detailed answers if user explicitly asks (e.g. "go deeper", "full explanation").
"""

        query = f"Explain {topic} at a {level} level."

        result = self.client.models.generate_content(
            model=self.model,
            contents=f"{system_prompt}\nUser: {query}"
        )

        return result.text.strip()
