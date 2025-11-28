# ui/pages/indicators.py
import streamlit as st
from services.api_client import call_backend


def render():
    st.title("📊 Technical Indicators")

    symbol = st.text_input("Symbol", "AAPL").upper()

    if st.button("Get Indicators"):
        payload = {"symbol": symbol, "period": "6mo"}
        response = call_backend("indicators", payload)

        if "error" in response:
            st.error(response["error"])
        else:
            st.success("Indicators Fetched")
            st.json(response)
