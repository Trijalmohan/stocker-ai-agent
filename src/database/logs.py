# src/database/logs.py
from src.database.connection import get_db

def save_log(trace_id, level, message):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO logs (trace_id, level, message) VALUES (?, ?, ?)", (trace_id, level, message))
    conn.commit()
    conn.close()
