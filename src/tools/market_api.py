# src/tools/market_api.py

def get_price(symbol: str) -> float:
    """
    TEMPORARY PRICE FETCHER (Stub)
    Replace with real API later (Yahoo Finance, Alpha Vantage, Finnhub).
    """
    sample = {
        "AAPL": 175.0,
        "TSLA": 240.0,
        "MSFT": 360.0,
        "NVDA": 900.0,
        "GOOG": 150.0
    }

    return sample.get(symbol.upper(), None)
