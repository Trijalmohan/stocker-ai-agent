# app.py
import streamlit as st
from ui.pages.dashboard import render as dashboard_page
from ui.pages.charts import render as chart_page
from ui.pages.backtest import render as backtest_page

st.set_page_config(
    page_title="Stocker AI",
    layout="wide",
    page_icon="📈"
)

PAGES = {
    "📊 Dashboard": dashboard_page,
    "📈 Charts": chart_page,
    "📉 Backtest": backtest_page,
}

page = st.sidebar.selectbox("Navigation", list(PAGES.keys()))
PAGES[page]()
