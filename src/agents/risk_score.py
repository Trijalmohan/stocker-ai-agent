def calculate_risk(indicators: dict):
    """
    Returns a 0–100 risk score + verbal label.
    Higher = more risky.
    """

    if not indicators or not isinstance(indicators, dict):
        return {
            "score": None,
            "rating": "unknown",
            "reason": "Missing indicators"
        }

    score = 50  # baseline neutral

    rsi = indicators.get("rsi")
    sma20 = indicators.get("sma20")
    sma50 = indicators.get("sma50")
    macd = indicators.get("macd")

    # --- RSI Logic ---
    if rsi:
        if rsi > 70:
            score += 25
        elif rsi > 60:
            score += 10
        elif rsi < 30:
            score -= 20
        elif rsi < 40:
            score -= 10

    # --- Trend Logic (SMA crossover) ---
    if sma20 and sma50:
        if sma20 < sma50:   # bearish
            score += 20
        else:               # bullish
            score -= 10

    # --- MACD Momentum ---
    if macd:
        if macd < 0:
            score += 10
        else:
            score -= 5

    score = max(0, min(100, score))  # clamp range

    # Label the score
    if score >= 70:
        rating = "HIGH RISK"
    elif score >= 50:
        rating = "MODERATE RISK"
    else:
        rating = "LOW RISK"

    return {
        "score": score,
        "rating": rating,
        "reason": "Calculated from RSI, SMA, MACD."
    }
