# ui/components/chart.py
import streamlit as st
import pandas as pd

try:
    import plotly.graph_objects as go
    PLOTLY_AVAILABLE = True
except Exception:
    PLOTLY_AVAILABLE = False


def render_price_chart(df: pd.DataFrame, overlays=None):
    """
    df: pandas DataFrame indexed by datetime. Prefer columns: ['open','high','low','close','volume']
    overlays: list of indicator names to optionally draw (SMA20, SMA50, RSI...).
    """
    overlays = overlays or []

    # ensure datetime index
    if not hasattr(df.index, "tz"):
        df.index = pd.to_datetime(df.index)

    # If OHLC present and Plotly available -> candlestick
    has_ohlc = set(["open", "high", "low", "close"]).issubset(df.columns)
    if has_ohlc and PLOTLY_AVAILABLE:
        fig = go.Figure(data=[go.Candlestick(
            x=df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="OHLC"
        )])

        # overlays: simple SMA lines if present in df
        for name in overlays:
            key = name.lower()
            if key in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df[key], mode="lines", name=name))

        fig.update_layout(
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            margin=dict(l=10, r=10, t=30, b=20),
            height=520
        )
        st.plotly_chart(fig, use_container_width=True)
        return

    # Otherwise: fallback to line chart with close or first numeric column
    ycol = None
    for c in ["close", "price", "adj_close", "adjclose", "last"]:
        if c in df.columns:
            ycol = c
            break
    if ycol is None:
        # pick first numeric column
        numeric_cols = df.select_dtypes("number").columns.tolist()
        if numeric_cols:
            ycol = numeric_cols[0]
        else:
            st.warning("No numeric column to chart.")
            st.dataframe(df.head())
            return

    # simple streamlit line chart (Plotly if available)
    if PLOTLY_AVAILABLE:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df[ycol], mode="lines", name=ycol))
        # overlays if present in df
        for name in overlays:
            key = name.lower()
            if key in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df[key], mode="lines", name=name))
        fig.update_layout(template="plotly_dark", height=460, margin=dict(l=10, r=10, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.line_chart(df[ycol])
