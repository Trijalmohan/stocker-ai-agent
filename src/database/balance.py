# src/database/balance.py
from src.database.init_db import get_conn

def get_balance():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT total FROM balance WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return float(row[0]) if row else 0.0

def update_balance(new_balance: float):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE balance SET total = ? WHERE id = 1", (new_balance,))
    conn.commit()
    conn.close()

def deposit(amount: float):
    balance = get_balance()
    new_balance = balance + amount
    update_balance(new_balance)
    return new_balance
