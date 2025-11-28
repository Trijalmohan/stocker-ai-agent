# src/services/indicators.py
import pandas as pd
import numpy as np
from typing import Dict, Any
from src.services.market_data import get_stock_candles

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Add only SMA50, SMA200, EMA20, RSI14."""
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()
    df = df.sort_values("time")

    close = df["close"].astype(float)

    df["SMA50"] = close.rolling(50, min_periods=1).mean()
    df["SMA200"] = close.rolling(200, min_periods=1).mean()
    df["EMA20"] = close.ewm(span=20, adjust=False).mean()

    # RSI
    delta = close.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    roll_up = up.rolling(14, min_periods=1).mean()
    roll_down = down.rolling(14, min_periods=1).mean()
    rs = roll_up / (roll_down.replace(0, np.nan))
    df["RSI"] = (100 - (100 / (1 + rs))).fillna(50)

    return df

def get_indicators(symbol: str, period="6mo") -> Dict[str, Any]:
    """Return indicator summary for agents."""
    df = get_stock_candles(symbol, period)
    if df.empty:
        return {"error": "no data"}

    df = add_indicators(df)
    last = df.iloc[-1]

    return {
        "symbol": symbol.upper(),
        "period": period,
        "sma": {
            "sma50": float(last["SMA50"]),
            "sma200": float(last["SMA200"]),
        },
        "ema": {
            "ema20": float(last["EMA20"]),
        },
        "momentum": {
            "rsi": float(last["RSI"]),
        }
    }

__all__ = ["add_indicators", "get_indicators"]
