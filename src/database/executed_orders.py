# src/database/executed_orders.py
import sqlite3
from src.database.init_db import get_conn

def init_executed_orders_table():
    from src.database.init_db import init_executed_orders_table as _t; _t()

def log_executed_order(symbol, qty, price, side="buy", session_id=None, recommendation=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO executed_orders (session_id, symbol, qty, price, side, recommendation)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, symbol, qty, price, side, recommendation))
    conn.commit()
    conn.close()

def get_executed_orders(limit=100):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, session_id, symbol, qty, price, side, recommendation, timestamp FROM executed_orders ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    cols = ["id","session_id","symbol","qty","price","side","recommendation","timestamp"]
    return [dict(zip(cols, r)) for r in rows]
