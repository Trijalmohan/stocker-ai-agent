# ui/pages/dashboard.py
import streamlit as st
from ui.services.api_client import call_backend

def render():
    st.title("📊 Stocker AI Dashboard")

    st.subheader("Generate Strategy")

    prompt = st.text_input("Describe your strategy goal", "RSI momentum strategy")
    risk = st.selectbox("Risk Level", ["low", "medium", "high"], index=1)
    timeframe = st.selectbox("Timeframe", ["1mo", "3mo", "6mo", "1y"], index=2)
    symbol = st.text_input("Symbol (optional)", "AAPL")

    if st.button("Generate"):
        resp = call_backend(
            message=prompt,
            intent="generate_strategy",
            payload={
                "prompt": prompt,
                "risk": risk,
                "timeframe": timeframe,
                "symbol": symbol
            }
        )

        data = resp.get("response", {})

        if "error" in data:
            st.error(data["error"])
            return

        st.success("Strategy Generated")
        st.write("### Summary")
        st.write(data.get("summary", ""))

        st.write("### Strategy Text")
        st.write(data.get("strategy_text", ""))

        st.write("### Strategy JSON")
        st.json(data.get("strategy", {}))

        st.write("### Indicators")
        st.json(data.get("indicators", {}))
