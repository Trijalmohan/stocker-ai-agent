# ui/components/navbar.py
import streamlit as st

def navbar(title="📈 Stocker AI"):
    st.markdown(
        f"""
        <div style="background:#0E1117;padding:1rem;border-radius:8px;margin-bottom:10px;">
            <h2 style="color:white;margin:0;">{title}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
