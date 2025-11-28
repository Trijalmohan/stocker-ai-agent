# src/database/pending_orders.py
import sqlite3
from src.database.init_db import get_conn

def init_pending_orders_table():
    # wrapper in case not called
    from src.database.init_db import init_pending_orders_table as _t; _t()

def save_pending_order(session_id, symbol, qty, price, side, recommendation=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO pending_orders (session_id, symbol, qty, price, side, recommendation)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, symbol, qty, price, side, recommendation))
    conn.commit()
    conn.close()

def get_pending_orders(session_id=None):
    conn = get_conn()
    c = conn.cursor()
    if session_id:
        c.execute("SELECT id, session_id, symbol, qty, price, side, recommendation, created_at FROM pending_orders WHERE session_id = ?", (session_id,))
    else:
        c.execute("SELECT id, session_id, symbol, qty, price, side, recommendation, created_at FROM pending_orders")
    rows = c.fetchall()
    conn.close()
    cols = ["id","session_id","symbol","qty","price","side","recommendation","created_at"]
    return [dict(zip(cols, r)) for r in rows]

def delete_pending_order(order_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM pending_orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
