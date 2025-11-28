# src/services/strategy_generator.py
import uuid

def generate_strategy(prompt=None, risk=None, timeframe=None):
    text = (prompt or "").lower()

    if "rsi" in text or "momentum" in text:
        strat = {
            "id": str(uuid.uuid4())[:8],
            "type": "rsi",
            "params": {"oversold": 30, "overbought": 70},
            "content": "RSI strategy: Buy when RSI < 30, sell when RSI > 70."
        }
        return strat

    # DEFAULT → MA crossover
    strat = {
        "id": str(uuid.uuid4())[:8],
        "type": "ma_crossover",
        "params": {"short": 50, "long": 200},
        "content": "Moving-average crossover strategy: Buy when SMA50 rises above SMA200."
    }
    return strat

class StrategyGenerator:
    def generate(self, prompt=None, risk=None, timeframe=None):
        return generate_strategy(prompt, risk, timeframe)
