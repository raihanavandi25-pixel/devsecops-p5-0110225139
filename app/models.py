"""Lapisan akses data (SQLite). Semua query memakai parameterized statement."""
import sqlite3

_connection = None


def get_connection(db_path):
    global _connection
    if db_path == ":memory:":
        if _connection is None:
            _connection = sqlite3.connect(":memory:", check_same_thread=False)
            _connection.row_factory = sqlite3.Row
        return _connection
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def reset_memory_db():
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None


def init_db(db_path):
    conn = get_connection(db_path)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title TEXT NOT NULL,
               status TEXT NOT NULL DEFAULT 'todo'
           )"""
    )
    conn.commit()


def add_task(db_path, title):
    conn = get_connection(db_path)
    cur = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    conn.commit()
    return cur.lastrowid


def list_tasks(db_path, status=None):
    conn = get_connection(db_path)
    if status:
        rows = conn.execute("SELECT * FROM tasks WHERE status = ?", (status,))
    else:
        rows = conn.execute("SELECT * FROM tasks")
    return [dict(r) for r in rows.fetchall()]


def update_status(db_path, task_id, status):
    conn = get_connection(db_path)
    cur = conn.execute(
        "UPDATE tasks SET status = ? WHERE id = ?", (status, task_id)
    )
    conn.commit()
    return cur.rowcount > 0


def delete_task(db_path, task_id):
    conn = get_connection(db_path)
    cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return cur.rowcount > 0
