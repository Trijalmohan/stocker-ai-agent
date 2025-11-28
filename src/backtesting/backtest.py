# src/backtesting/backtest.py
from typing import List, Dict, Any
import pandas as pd


def run_ma_backtest(series: List[Dict[str, Any]], short_window: int = 20, long_window: int = 50):
    """
    Simple moving-average crossover backtest.
    series: list of {date, open, high, low, close, volume}
    Returns summary metrics and trades
    """
    if not isinstance(series, list) or len(series) < long_window + 2:
        return {"error": "Not enough data to backtest", "trades": [], "metrics": {}}

    df = pd.DataFrame(series)
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    df = df.dropna(subset=["close"]).reset_index(drop=True)

    df["short_ma"] = df["close"].rolling(window=short_window).mean()
    df["long_ma"] = df["close"].rolling(window=long_window).mean()

    position = 0  # 0 = cash, 1 = long
    entry_price = 0.0
    trades = []

    for i in range(1, len(df)):
        # ensure both MAs exist
        if pd.isna(df.loc[i - 1, "short_ma"]) or pd.isna(df.loc[i - 1, "long_ma"]):
            continue
        prev_short = df.loc[i - 1, "short_ma"]
        prev_long = df.loc[i - 1, "long_ma"]
        cur_short = df.loc[i, "short_ma"]
        cur_long = df.loc[i, "long_ma"]

        # signal: short crosses above long -> buy
        if position == 0 and prev_short <= prev_long and cur_short > cur_long:
            position = 1
            entry_price = df.loc[i, "close"]
            trades.append({"type": "buy", "date": df.loc[i, "date"], "price": float(entry_price)})

        # signal: short crosses below long -> sell
        if position == 1 and prev_short >= prev_long and cur_short < cur_long:
            exit_price = df.loc[i, "close"]
            pnl = float(exit_price - entry_price)
            trades.append({"type": "sell", "date": df.loc[i, "date"], "price": float(exit_price), "pnl": pnl})
            position = 0
            entry_price = 0.0

    # If still long at the end, close at last price
    if position == 1:
        last_price = df.loc[len(df) - 1, "close"]
        trades.append({"type": "sell", "date": df.loc[len(df) - 1, "date"], "price": float(last_price), "pnl": float(last_price - entry_price)})

    # compute basic metrics
    total_pnl = sum([t.get("pnl", 0) for t in trades if t.get("type") == "sell"])
    num_trades = len([t for t in trades if t["type"] in ("buy", "sell")])
    wins = len([t for t in trades if t.get("pnl", 0) > 0])
    losses = len([t for t in trades if t.get("pnl", 0) <= 0])

    metrics = {"total_pnl": float(total_pnl), "num_trades": num_trades, "wins": wins, "losses": losses}

    return {"trades": trades, "metrics": metrics, "short_window": short_window, "long_window": long_window}
