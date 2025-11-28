# ui/pages/backtest.py
import streamlit as st
from ui.services.api_client import call_backend

def render():
    st.title("📉 Backtesting Engine")

    symbol = st.text_input("Symbol", "AAPL").upper()

    if st.button("Run Backtest"):
        resp = call_backend(
            message="run backtest",
            intent="backtest",
            payload={"symbol": symbol}
        )

        data = resp.get("response", {})

        if "error" in data:
            st.error(data["error"])
            return

        st.success("Backtest Completed")

        st.json(data)
