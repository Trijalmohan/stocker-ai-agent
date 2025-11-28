import requests
import os

API_KEY = os.getenv("NEWSDATA_API_KEY", "YOUR_KEY_HERE")
BASE_URL = "https://newsdata.io/api/1/news"

def get_market_news(limit=10):
    params = {
        "apikey": API_KEY,
        "q": "stocks OR investing OR crypto OR markets",
        "language": "en",
    }
    
    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        data = resp.json()

        articles = data.get("results", [])[:limit]

        return [
            {
                "title": a.get("title"),
                "source": a.get("source_id"),
                "link": a.get("link"),
                "pubDate": a.get("pubDate")
            }
            for a in articles
        ]
    except Exception as e:
        return {"error": str(e)}
