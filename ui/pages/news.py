# ui/pages/news.py
from services.api_client import call_backend
import streamlit as st


def render():
    st.title("📰 Stock News")
    st.info("Will integrate news API later.")

    trace, response, error = call_backend(message="show news", intent="market_news")
    if not error and isinstance(response, list):
        for item in response:
            st.markdown(f"**{item.get('headline')}** — {item.get('source')}")
    else:
        st.info("No news available.")
