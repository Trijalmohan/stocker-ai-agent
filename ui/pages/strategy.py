# ui/pages/strategies.py
import streamlit as st
from services.api_client import call_backend


def render():
    st.title("🤖 AI Strategy Generator")

    prompt = st.text_area("Describe your strategy idea", "RSI momentum quick trades")
    risk = st.selectbox("Risk Level", ["low", "medium", "high"])
    timeframe = st.selectbox("Timeframe", ["1mo", "3mo", "6mo", "1y"])

    if st.button("Generate Strategy"):
        payload = {
            "prompt": prompt,
            "risk": risk,
            "timeframe": timeframe,
        }
        response = call_backend("generate_strategy", payload)

        if "error" in response:
            st.error(response["error"])
        else:
            st.success("AI Strategy Generated")
            st.json(response)
