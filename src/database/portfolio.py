# src/database/portfolio.py
from src.database.init_db import get_conn
import sqlite3

def add_or_update_position(symbol: str, qty: float, price: float):
    conn = get_conn()
    c = conn.cursor()
    # If exists, add to quantity and recompute avg price (simple weighted avg)
    c.execute("SELECT id, quantity, avg_price FROM positions WHERE symbol = ?", (symbol,))
    row = c.fetchone()
    if row:
        id_, existing_qty, existing_avg = row
        existing_qty = existing_qty or 0.0
        existing_avg = existing_avg or 0.0
        total_qty = existing_qty + qty
        if total_qty == 0:
            new_avg = 0.0
        else:
            new_avg = (existing_avg * existing_qty + price * qty) / total_qty
        c.execute("UPDATE positions SET quantity = ?, avg_price = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (total_qty, new_avg, id_))
    else:
        c.execute("INSERT INTO positions (symbol, quantity, avg_price, market_price, unrealized_pnl) VALUES (?, ?, ?, ?, ?)",
                  (symbol, qty, price, price, 0.0))
    conn.commit()
    conn.close()

def get_positions():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT symbol, quantity, avg_price, market_price, unrealized_pnl, updated_at FROM positions")
    rows = c.fetchall()
    conn.close()
    cols = ["symbol", "quantity", "avg_price", "market_price", "unrealized_pnl", "updated_at"]
    return [dict(zip(cols, r)) for r in rows]

def sell_position(symbol: str, qty: float, price: float):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, quantity, avg_price FROM positions WHERE symbol = ?", (symbol,))
    row = c.fetchone()
    if not row:
        conn.close()
        raise ValueError("No position")
    id_, existing_qty, avg_price = row
    remaining = existing_qty - qty
    if remaining <= 0:
        c.execute("DELETE FROM positions WHERE id = ?", (id_,))
    else:
        c.execute("UPDATE positions SET quantity = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (remaining, id_))
    conn.commit()
    conn.close()

def get_realized_pnl():
    # For now a simple stub: 0.0
    return 0.0

def get_unrealized_pnl():
    # calculate sum of (market_price - avg_price) * quantity
    positions = get_positions()
    total = 0.0
    for p in positions:
        qty = p.get("quantity", 0) or 0
        avg = p.get("avg_price", 0) or 0
        mkt = p.get("market_price", avg) or avg
        total += (mkt - avg) * qty
    return total
