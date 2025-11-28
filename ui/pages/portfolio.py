# ui/pages/portfolio.py
import streamlit as st
import pandas as pd
from ui.services.api_client import call_backend

def render():
    st.title("💼 Portfolio")
    st.write("Your current holdings and quick actions.")

    trace, resp, err = call_backend("show portfolio", intent="portfolio")
    if err:
        st.error(err)
        return

    positions = resp.get("portfolio", [])
    if not positions:
        st.info("No positions to show.")
        return

    df = pd.DataFrame(positions)
    # show friendly table
    st.dataframe(df, width="stretch")

    # quick action: close first position (demo)
    if st.button("Simulate close-first-position"):
        first = positions[0]
        st.write("Simulating close:", first)
        st.success("Simulation done (no real trade executed).")
