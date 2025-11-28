# ui/pages/charts.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from ui.services.api_client import call_backend

def render():
    st.title("📈 Technical Chart Viewer")

    symbol = st.text_input("Symbol", "AAPL").upper()
    period = st.selectbox("Period", ["1mo", "3mo", "6mo", "1y"], index=2)

    st.subheader("Indicators")
    col1, col2, col3 = st.columns(3)

    with col1:
        show_sma = st.checkbox("SMA (50/200)", True)
    with col2:
        show_ema = st.checkbox("EMA (20)", True)
    with col3:
        show_rsi = st.checkbox("RSI", True)

    show_volume = st.checkbox("Show Volume", True)

    if st.button("Load Chart"):
        resp = call_backend(
            message="get chart",
            intent="candles",
            payload={"symbol": symbol, "period": period}
        )

        data = resp.get("response", {})

        if "error" in data:
            st.error(data["error"])
            return

        candles = data.get("data")
        indicators = data.get("indicators", {})

        df = pd.DataFrame(candles)
        df["time"] = pd.to_datetime(df["time"])

        fig = go.Figure()

        # candles
        fig.add_trace(go.Candlestick(
            x=df["time"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Price"
        ))

        # SMA
        if show_sma and "sma" in indicators:
            sma = indicators["sma"]
            fig.add_trace(go.Scatter(
                x=df["time"], y=sma["sma50"], mode="lines", name="SMA50", line=dict(color="orange")
            ))
            fig.add_trace(go.Scatter(
                x=df["time"], y=sma["sma200"], mode="lines", name="SMA200", line=dict(color="brown")
            ))

        # EMA
        if show_ema and "ema" in indicators:
            ema = indicators["ema"]
            fig.add_trace(go.Scatter(
                x=df["time"], y=ema["ema20"], mode="lines", name="EMA20", line=dict(color="blue")
            ))

        # Volume
        if show_volume:
            fig.add_trace(go.Bar(
                x=df["time"], y=df["volume"],
                name="Volume",
                marker_color="gray",
                yaxis="y2",
                opacity=0.4
            ))

        # layout
        fig.update_layout(
            height=600,
            xaxis=dict(title="Time"),
            yaxis=dict(title="Price"),
            yaxis2=dict(overlaying="y", side="right", position=1.0)
        )

        st.plotly_chart(fig, use_container_width=True)

        # RSI lower chart
        if show_rsi and "momentum" in indicators:
            st.subheader("RSI (14)")

            rsi_fig = go.Figure()
            rsi_fig.add_trace(go.Scatter(
                x=df["time"],
                y=indicators["momentum"]["rsi"],
                mode="lines",
                name="RSI",
                line=dict(color="purple")
            ))

            rsi_fig.add_hline(y=70, line_color="red")
            rsi_fig.add_hline(y=30, line_color="green")

            st.plotly_chart(rsi_fig, use_container_width=True)
