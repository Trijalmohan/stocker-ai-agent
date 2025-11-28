from google import genai
import os

from src.database.conversation import get_history, save_message
from src.tools.market_api import get_price   # keep your stub

class ExpertAgent:
    def __init__(self, memory=None):
        self.memory = memory
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "models/gemini-2.5-pro"

    def explain_advanced(self, session_id: str, topic: str, level: str = "advanced") -> str:

        history = get_history(session_id)
        context = "\n".join(
            [f"{h['role']}: {h['message']}" for h in history[-8:]]
        )

        system_prompt = (
            "You are STOCKER-EXPERT, a technical finance analyst.\n"
            "Provide formulas, edge cases, and deep logic.\n"
            f"Conversation history:\n{context}\n"
        )

        user_prompt = f"Explain '{topic}' at an '{level}' depth."

        contents = [
            {"role": "model", "parts": [{"text": system_prompt}]},
            {"role": "user", "parts": [{"text": user_prompt}]}
        ]

        result = self.client.models.generate_content(
            model=self.model,
            contents=contents
        )

        save_message(session_id, "assistant", result.text)
        return result.text
