# src/agents/strategy_engine.py

import os
from google import genai
import pandas as pd

from src.services.market_data import get_stock_candles, get_crypto_price
from src.services.indicators import add_indicators

try:
    from src.services.risk_score import calculate_risk
except ImportError:
    calculate_risk = None   # fallback if module missing


# ---------------------------------------------
# Fallback simple risk calculator
# ---------------------------------------------
def _calc_risk(volatility):
    if volatility is None or pd.isna(volatility):
        return {
            "risk_score": 50.0,
            "level": "Medium",
            "reason": "No volatility data"
        }
    score = min(100, max(0, float(volatility) * 10))
    level = (
        "Low" if score < 30
        else "Medium" if score < 70
        else "High"
    )
    return {
        "risk_score": round(score, 2),
        "level": level,
        "reason": f"Derived from volatility={volatility}"
    }


# ---------------------------------------------
# Strategy Engine
# ---------------------------------------------
class StrategyEngine:
    def __init__(self):
        self.client = None
        key = os.getenv("GOOGLE_API_KEY")
        if key:
            try:
                self.client = genai.Client(api_key=key)
            except Exception:
                self.client = None

        self.model = "models/gemini-2.5-flash"

    # --------------------------------------------------------
    # MAIN ANALYSIS FUNCTION
    # --------------------------------------------------------
    def analyze(self, symbol: str, user_message: str | None = None):

        symbol = symbol.upper()

        # --------------------------------------------------------
        # 1) Load 6 months candles
        # --------------------------------------------------------
        candles = get_stock_candles(symbol, period="6mo")

        if isinstance(candles, dict) and candles.get("error"):
            # fallback to crypto
            candles = get_crypto_price(symbol)

        if not isinstance(candles, pd.DataFrame):
            return {
                "status": "error",
                "message": "Could not load market data",
                "raw": candles
            }

        # --------------------------------------------------------
        # 2) Add indicators into the DataFrame
        # --------------------------------------------------------
        candles = add_indicators(
            candles,
            indicators=["rsi", "macd", "sma20", "ema20", "volatility"]
        )

        last = candles.iloc[-1]

        price = float(last.get("close"))
        rsi = last.get("rsi")
        macd = last.get("macd")
        volatility = last.get("volatility")

        # --------------------------------------------------------
        # 3) Risk score
        # --------------------------------------------------------
        if calculate_risk:
            try:
                risk = calculate_risk(price, volatility)
            except Exception:
                risk = _calc_risk(volatility)
        else:
            risk = _calc_risk(volatility)

        # --------------------------------------------------------
        # 4) Gemini / fallback analysis
        # --------------------------------------------------------
        prompt = f"""
You are a concise financial analyst.
Symbol: {symbol}
Price: {price}
RSI: {rsi}
MACD: {macd}
Volatility: {volatility}
User context: {user_message}

Return a JSON object ONLY with:
summary
recommendation (Buy/Sell/Hold)
confidence (0-100)
price_target (number)
"""

        ai_output = None

        if self.client:
            try:
                result = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                ai_output = result.text.strip()

            except Exception:
                ai_output = None

        # --------------------------------------------------------
        # 5) No LLM available → heuristic fallback
        # --------------------------------------------------------
        if ai_output is None:

            rec = "HOLD"
            conf = 50

            if rsi is not None:
                if rsi < 30:
                    rec = "BUY"; conf = 65
                elif rsi > 70:
                    rec = "SELL"; conf = 65

            ai_output = {
                "summary": f"Heuristic analysis for {symbol}.",
                "recommendation": rec,
                "confidence": conf,
                "price_target": price * 1.05 if price else None
            }

        # --------------------------------------------------------
        # 6) Final output
        # --------------------------------------------------------
        return {
            "status": "ok",
            "symbol": symbol,
            "price": price,
            "rsi": rsi,
            "macd": macd,
            "volatility": volatility,
            "risk": risk,
            "analysis": ai_output,
            "action": "To execute: say 'approve trade'"
        }
