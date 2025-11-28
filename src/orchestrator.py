"""
FINAL ORCHESTRATOR — stable, JSON-safe, fully compatible with FastAPI + UI.

Supports intents:
- candles          → chart data + indicators
- generate_strategy → natural-language strategy generation
- backtest         → (backend ready, UI can call)
"""

from typing import Any, Dict, Optional
import traceback
import time
import pandas as pd

from src.agents.strategy_generator import StrategyGenerator
from src.services.indicators import get_indicators, add_indicators
from src.services.market_data import get_stock_candles, get_stock_price
from src.services.backtest import backtest


# -------------------------------------------------------
# Helper: Shorten long strategy text for UI summary
# -------------------------------------------------------

def _short_summary(text: str, max_len: int = 160) -> str:
    if not text:
        return ""
    p = [p.strip() for p in text.split("\n\n") if p.strip()]
    first = p[0] if p else text
    return first[: max_len] + "..." if len(first) > max_len else first


# -------------------------------------------------------
# Main Orchestrator
# -------------------------------------------------------

class Orchestrator:
    def __init__(self):
        try:
            self.strategy_gen = StrategyGenerator()
        except Exception:
            self.strategy_gen = None

    # =====================================================
    # ROUTER METHOD (FastAPI calls this)
    # =====================================================

    def handle(
        self,
        session_id: str,
        intent: str,
        payload: Optional[Dict[str, Any]] = None,
        message: Optional[str] = None,
    ) -> Dict[str, Any]:

        payload = payload or {}

        try:

            # ========== CANDLES (Charts) ==========
            if intent == "candles":
                return self._handle_candles(session_id, payload)

            # ========== STRATEGY GENERATION ==========
            if intent == "generate_strategy":
                return self._handle_strategy(session_id, payload, message)

            # ========== BACKTEST ==========
            if intent == "backtest":
                return self._handle_backtest(session_id, payload)

            # Unknown intent
            return {
                "session_id": session_id,
                "response": {"error": f"Unknown intent '{intent}'"}
            }

        except Exception as e:
            return {
                "session_id": session_id,
                "response": {
                    "error": "internal_error",
                    "details": str(e),
                    "trace": traceback.format_exc()
                }
            }

    # =====================================================
    # 1) CANDLES HANDLER (Charts require JSON-safe output)
    # =====================================================

    def _handle_candles(self, session_id: str, payload: Dict[str, Any]):
        symbol = payload.get("symbol", "AAPL").upper()
        period = payload.get("period", "6mo")

        try:
            df = get_stock_candles(symbol, period=period)

            if df is None or df.empty:
                return {
                    "session_id": session_id,
                    "response": {"error": f"No candle data for {symbol}."}
                }

            # Add indicators (SMA/EMA/RSI)
            df = add_indicators(df)

            # --------- Build indicator arrays ----------
            indicators = {}

            if "SMA50" in df and "SMA200" in df:
                indicators["sma"] = {
                    "sma50": df["SMA50"].astype(float).tolist(),
                    "sma200": df["SMA200"].astype(float).tolist()
                }

            if "EMA20" in df:
                indicators["ema"] = {
                    "ema20": df["EMA20"].astype(float).tolist()
                }

            if "RSI" in df:
                indicators["momentum"] = {
                    "rsi": df["RSI"].astype(float).tolist()
                }

            # --------- SAFE CANDLES (important!) ----------
            candles = []
            for row in df.to_dict(orient="records"):
                t = row.get("time")
                if isinstance(t, (pd.Timestamp,)):
                    row["time"] = t.isoformat()
                candles.append(row)

            return {
                "session_id": session_id,
                "response": {
                    "data": candles,
                    "indicators": indicators
                }
            }

        except Exception as e:
            return {
                "session_id": session_id,
                "response": {
                    "error": str(e),
                    "trace": traceback.format_exc()
                }
            }

    # =====================================================
    # 2) STRATEGY GENERATION
    # =====================================================

    def _handle_strategy(self, session_id, payload, message):
        prompt = (
            payload.get("prompt")
            or payload.get("message")
            or message
            or "Generate a trading strategy"
        )

        risk = payload.get("risk", "medium")
        timeframe = payload.get("timeframe", "6mo")
        symbol = payload.get("symbol")

        # --------- ENRICH: Indicators for context ---------
        indicators = {}
        try:
            if symbol:
                indicators = get_indicators(symbol, timeframe)
        except Exception:
            indicators = {}

        # --------- CALL STRATEGY GENERATOR ---------
        gen_status = "ok"
        warning = None

        if self.strategy_gen:
            try:
                out = self.strategy_gen.generate(prompt=prompt, risk=risk, timeframe=timeframe)
                strategy_text = out.get("content", "")
                if "warning" in out:
                    warning = out["warning"]
            except Exception as e:
                gen_status = "error"
                strategy_text = f"Fallback: Strategy generation failed. {e}"
        else:
            gen_status = "missing_generator"
            strategy_text = "Fallback: Strategy generator not available."

        summary = _short_summary(strategy_text)

        # --------- PRICE SNAPSHOT ---------
        price_snapshot = None
        if symbol:
            try:
                sp = get_stock_price(symbol)
                price_snapshot = sp
            except:
                price_snapshot = {"error": "price_failed"}

        return {
            "session_id": session_id,
            "response": {
                "status": gen_status,
                "strategy_text": strategy_text,
                "summary": summary,
                "indicators": indicators,
                "price_snapshot": price_snapshot,
                "meta": {
                    "symbol": symbol,
                    "risk": risk,
                    "timeframe": timeframe,
                    "warnings": [w for w in [warning] if w],
                    "timestamp": int(time.time())
                }
            }
        }

    # =====================================================
    # 3) BACKTEST HANDLER
    # =====================================================

    def _handle_backtest(self, session_id, payload):
        symbol = payload.get("symbol", "AAPL")
        strategy = payload.get("strategy")

        try:
            result = backtest(symbol, strategy)
            return {
                "session_id": session_id,
                "response": result
            }
        except Exception as e:
            return {
                "session_id": session_id,
                "response": {
                    "error": "backtest_failed",
                    "details": str(e),
                    "trace": traceback.format_exc()
                }
            }


# Singleton instance
orch = Orchestrator()
