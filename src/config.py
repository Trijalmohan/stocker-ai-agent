import os
from dotenv import load_dotenv

load_dotenv()

FINNHUB_API_KEY = os.getenv("STOCKER_FINNHUB_KEY")
