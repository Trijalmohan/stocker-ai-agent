# src/database/conversation.py

from src.database.init_db import get_conn

def save_message(session_id, role, message):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO conversation (session_id, role, message) VALUES (?, ?, ?)",
        (session_id, role, message),
    )
    conn.commit()
    conn.close()

def get_history(session_id, limit=50):
    """
    Returns the last N messages from the conversation table for a given session.
    This is required by teacher_agent, expert_agent, etc.
    """
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        SELECT role, message, created_at
        FROM conversation
        WHERE session_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (session_id, limit),
    )

    rows = c.fetchall()
    conn.close()

    history = []
    for role, message, created_at in rows:
        history.append(
            {"role": role, "message": message, "timestamp": created_at}
        )

    # reverse chronological → oldest first
    return list(reversed(history))
