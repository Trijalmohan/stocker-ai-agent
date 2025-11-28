# ui/pages/history.py
import pandas as pd
from ui.services.api_client import call_backend
import streamlit as st


def render():
    st.title("📜 History")
    st.info("History tracking not implemented yet.")

    trace, resp, err = call_backend("show trade history", intent="executed_orders")
    if err:
        st.error(err)
        return

    orders = resp.get("orders", [])
    if not orders:
        st.info("No executed trades yet.")
        return

    df = pd.DataFrame(orders)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    st.dataframe(df, width="stretch")

    st.write("Select a trade to inspect:")
    sel = st.selectbox("Trade", orders, format_func=lambda o: f"{o.get('side','').upper()} {o.get('qty')} {o.get('symbol')} @ {o.get('price')}")
    if sel:
        st.json(sel)
