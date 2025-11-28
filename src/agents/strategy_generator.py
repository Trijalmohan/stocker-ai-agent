# src/agents/strategy_generator.py

import os
from google import genai


class StrategyGenerator:

    def __init__(self):
        key = os.getenv("GOOGLE_API_KEY")
        try:
            self.client = genai.Client(api_key=key) if key else None
        except Exception:
            self.client = None

        self.model = "models/gemini-2.5-flash"

    def generate(self, prompt: str, risk: str = "medium", timeframe: str = "6mo"):
        """
        Generate a natural-language trading strategy.
        Does NOT return JSON — returns clean English instructions.
        """

        instruction = f"""
You are a professional quantitative trading strategist.

Write a very clear, concise NATURAL-LANGUAGE TRADING STRATEGY.
Do NOT use JSON. Do NOT use code blocks.
The user will read this directly.

DETAILS:
- User request: "{prompt}"
- Risk level: {risk}
- Timeframe: {timeframe}

FORMAT:
Write 5 short sections:
1. Strategy Name  
2. Objective  
3. Entry Rules  
4. Exit Rules  
5. Risk Considerations  

Write naturally, like you're explaining to a trader.
Avoid technical clutter unless relevant.
"""

        # ============ GEMINI OUTPUT ============
        if self.client:
            try:
                result = self.client.models.generate_content(
                    model=self.model, contents=instruction
                )
                text = result.text.strip()
                return {
                    "status": "ok",
                    "content": text
                }
            except Exception as e:
                print("Gemini error:", e)

        # ============ FALLBACK STRATEGY ============
        fallback = f"""
Strategy Name: Simple RSI Swing Plan

Objective:
Capture quick reversals by buying dips and selling rallies.

Entry Rules:
- Enter long when RSI falls below 30 (oversold).
- Increase confidence if the price forms a higher low.

Exit Rules:
- Sell when RSI rises above 70 (overbought).
- Exit early if price closes below the previous swing low.

Risk Considerations:
This is a {risk}-risk strategy. Works best for short-term swings.
Timeframe: {timeframe}.
"""

        return {
            "status": "fallback",
            "content": fallback,
            "warning": "Gemini unavailable — fallback strategy used."
        }
