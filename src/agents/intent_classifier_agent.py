from google import genai
import os
import json
import logging

logger = logging.getLogger(__name__)


class IntentClassifierAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "models/gemini-2.5-flash"

    def classify(self, message: str) -> dict:
        system_prompt = """
You are an intent classifier for a trading tutor agent.

Very important rules:
- Output ONLY valid JSON. No backticks, no markdown, no explanations.
- DO NOT execute any trades yourself.
- NEVER use 'buy' or 'sell' as the intent. For trade-type questions,
  use intent 'analyze' and include the symbol in payload.

Valid intents:
- "explain"           → explain a concept
- "quiz"              → quiz the user
- "portfolio"         → show current portfolio
- "balance"           → show cash balance
- "deposit"           → add funds
- "stock_price"       → ask for a stock price
- "crypto_price"      → ask for a crypto price
- "market_news"       → latest market news
- "pnl"               → realized + unrealized PnL
- "analyze"           → ask if a user should buy/sell/hold something

JSON schema:
{
  "intent": "<one of the above>",
  "payload": {
    // optional fields, for example:
    "symbol": "TSLA",
    "topic": "options",
    "amount": 1000
  }
}

Examples:

User: "Should I buy Tesla now?"
→ { "intent": "analyze", "payload": { "symbol": "TSLA" } }

User: "What's the price of bitcoin?"
→ { "intent": "crypto_price", "payload": { "symbol": "BTC" } }

User: "Show my portfolio"
→ { "intent": "portfolio", "payload": {} }
"""

        full_prompt = f"{system_prompt}\n\nUser: {message}\n\nReturn ONLY JSON."

        result = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
        )

        text = (result.text or "").strip()
        logger.info("[RAW_INTENT_OUTPUT] %s", text)

        # Strip accidental markdown fences
        text = text.replace("```json", "").replace("```", "").strip()

        # Try to isolate first {...} block
        if "{" in text and "}" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            text = text[start:end]

        try:
            data = json.loads(text)
            intent = data.get("intent")
            payload = data.get("payload") or {}
            return {"intent": intent, "payload": payload}
        except Exception as e:
            logger.error("Failed to parse intent JSON: %s | raw=%s", e, text)
            return {"intent": None, "payload": {}}
