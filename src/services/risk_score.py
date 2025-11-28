# src/services/risk_score.py
def calculate_risk(price, volatility):
    return {
        "risk_score": None,
        "level": "unknown",
        "reason": "Risk module disabled in simple mode."
    }
