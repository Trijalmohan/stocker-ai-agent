# src/services/backtest.py
import pandas as pd
from src.services.market_data import get_stock_candles
from src.services.indicators import add_indicators

def backtest(symbol="AAPL", strategy=None):
    df = get_stock_candles(symbol)
    if df.empty:
        return {"error": "No candle data"}

    df = add_indicators(df)

    if strategy is None:
        strategy = {
            "type": "ma_crossover",
            "params": {"short": 50, "long": 200}
        }

    stype = strategy["type"]
    params = strategy["params"]

    df["position"] = 0
    df["signal"] = 0

    # MA CROSSOVER
    if stype == "ma_crossover":
        short = params["short"]
        long = params["long"]

        df["SMA_short"] = df["close"].rolling(short).mean()
        df["SMA_long"] = df["close"].rolling(long).mean()
        df["position"] = (df["SMA_short"] > df["SMA_long"]).astype(int)
        df["signal"] = df["position"].diff().fillna(0)

    # RSI REVERSAL
    elif stype == "rsi":
        oversold = params["oversold"]
        overbought = params["overbought"]

        in_pos = False
        signals = []

        for r in df["RSI"]:
            if not in_pos and r < oversold:
                signals.append(1)
                in_pos = True
            elif in_pos and r > overbought:
                signals.append(-1)
                in_pos = False
            else:
                signals.append(0)

        df["signal"] = signals
        df["position"] = pd.Series(signals).cumsum().clip(lower=0).apply(lambda x: 1 if x > 0 else 0)

    # simulate trades
    balance = 10000
    shares = 0
    trades = []

    for _, row in df.iterrows():
        price = row["close"]

        if row["signal"] == 1 and balance > 0:
            shares = balance / price
            balance = 0
            trades.append({"type": "BUY", "price": float(price)})

        elif row["signal"] == -1 and shares > 0:
            balance = shares * price
            shares = 0
            trades.append({"type": "SELL", "price": float(price)})

    if shares > 0:
        balance = shares * df["close"].iloc[-1]

    return {
        "symbol": symbol,
        "final_balance": round(balance, 2),
        "profit": round(balance - 10000, 2),
        "trades": trades
    }
