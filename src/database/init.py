# src/database/init.py
"""
Create required tables if they don't exist.
Importing this module will create the DB schema.
"""
from .connection import get_db

def init_db():
    conn = get_db()
    c = conn.cursor()

    # balance table (single row id=1)
    c.execute("""
    CREATE TABLE IF NOT EXISTS balance (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        total REAL DEFAULT 10000.0
    )
    """)
    # ensure a single row exists
    c.execute("INSERT OR IGNORE INTO balance (id, total) VALUES (1, 10000.0)")

    # positions table
    c.execute("""
    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT,
        quantity REAL,
        avg_price REAL,
        market_price REAL,
        unrealized_pnl REAL,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # pending orders
    c.execute("""
    CREATE TABLE IF NOT EXISTS pending_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        symbol TEXT,
        qty REAL,
        price REAL,
        side TEXT,
        recommendation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # executed orders
    c.execute("""
    CREATE TABLE IF NOT EXISTS executed_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        symbol TEXT,
        qty REAL,
        price REAL,
        side TEXT,
        recommendation TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # logs table (simple)
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        level TEXT,
        trace_id TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

# run on import if desired
try:
    init_db()
except Exception:
    # if import-time DB creation should be suppressed, modify accordingly
    pass
