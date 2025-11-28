# src/database/positions.py
from src.database.connection import get_db


def init_positions_table():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            symbol TEXT NOT NULL,
            quantity REAL NOT NULL,
            avg_price REAL NOT NULL,
            market_price REAL DEFAULT 0,
            unrealized_pnl REAL DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_positions(session_id: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM positions WHERE session_id = ?", (session_id,))
    rows = cursor.fetchall()

    conn.close()
    return rows
