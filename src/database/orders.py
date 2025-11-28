# src/database/orders.py

import sqlite3
from typing import List, Dict, Any

from src.database.connection import get_db


def _rows_to_dicts(rows, columns) -> List[Dict[str, Any]]:
    return [dict(zip(columns, row)) for row in rows]


def log_order(
    session_id: str,
    symbol: str,
    side: str,
    qty: float,
    price: float,
    status: str = "executed",
    source: str = "api",
    meta: str | None = None,
) -> int:
    """
    Insert a single trade/order into the orders table.

    Returns the inserted row id.
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO orders (session_id, symbol, side, qty, price, status, source, meta)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (session_id, symbol, side.upper(), float(qty), float(price), status, source, meta),
    )

    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    return order_id


def get_orders(limit: int = 50) -> list[dict]:
    """
    Fetch most recent orders across all sessions.
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, created_at, session_id, symbol, side, qty, price, status, source, meta
        FROM orders
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()
    conn.close()

    columns = [
        "id",
        "created_at",
        "session_id",
        "symbol",
        "side",
        "qty",
        "price",
        "status",
        "source",
        "meta",
    ]
    return _rows_to_dicts(rows, columns)


def get_orders_for_session(session_id: str, limit: int = 50) -> list[dict]:
    """
    Fetch most recent orders for a single conversation/session.
    """
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, created_at, session_id, symbol, side, qty, price, status, source, meta
        FROM orders
        WHERE session_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT ?
        """,
        (session_id, limit),
    )

    rows = cursor.fetchall()
    conn.close()

    columns = [
        "id",
        "created_at",
        "session_id",
        "symbol",
        "side",
        "qty",
        "price",
        "status",
        "source",
        "meta",
    ]
    return _rows_to_dicts(rows, columns)
