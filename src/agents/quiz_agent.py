# src/agents/quiz_agent.py

from google import genai
import os

class QuizAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "models/gemini-2.5-flash"

    def generate_question(self, topic: str, difficulty: str = "easy"):
        """
        Generate a single quiz question on a financial topic.
        """
        prompt = f"""
Create a {difficulty} multiple-choice quiz question on: **{topic}**

Format strictly as valid JSON:
{{
  "question": "...",
  "options": ["A", "B", "C", "D"],
  "answer": "A",
  "explanation": "..."
}}
"""

        result = self.client.models.generate_text(
            model=self.model,
            prompt=prompt
        )

        return result.text
