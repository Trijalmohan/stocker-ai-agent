# src/services/market_data.py
import yfinance as yf
import pandas as pd
from typing import Dict, Any

def get_stock_price(symbol: str) -> Dict[str, Any]:
    """Get latest stock price using yfinance."""
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        if data.empty:
            return {"error": f"No price data for {symbol}"}
        return {"price": float(data["Close"].iloc[-1])}
    except Exception as e:
        return {"error": str(e)}

def get_crypto_price(symbol: str) -> Dict[str, Any]:
    """Crypto fallback: SYMBOL-USD."""
    try:
        ticker = yf.Ticker(symbol + "-USD")
        data = ticker.history(period="1d")
        if data.empty:
            return {"error": f"No price data for {symbol}"}
        return {"price": float(data["Close"].iloc[-1])}
    except Exception as e:
        return {"error": str(e)}

def get_stock_candles(symbol: str, period="6mo") -> pd.DataFrame:
    """Return OHLCV candles."""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        if df.empty:
            return pd.DataFrame()

        df = df.reset_index()
        df.rename(columns={
            "Date": "time",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume"
        }, inplace=True)
        return df
    except Exception:
        return pd.DataFrame()

__all__ = ["get_stock_price", "get_crypto_price", "get_stock_candles"]
