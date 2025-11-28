# src/database/connection.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "stocker.db")

def get_db():
    """Return a sqlite3 connection (caller must close)."""
    # ensure folder exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
