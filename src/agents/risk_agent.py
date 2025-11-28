from google import genai
import os

class RiskAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "models/gemini-2.5-flash"

    def assess(self, symbol: str, price: float, vol: float = None):
        prompt = f"""
You are a risk analyst. Analyze risk of buying {symbol} at price {price}.

Output JSON only:
{{
  "risk_level": "low | medium | high",
  "factors": ["...", "..."],
  "score": <number between 0 and 1>
}}
"""

        res = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        
        # Clean JSON
        text = res.text.replace("```json", "").replace("```", "").strip()
        
        import json
        try:
            return json.loads(text)
        except:
            return {"risk_level": "unknown", "score": 0.0}
