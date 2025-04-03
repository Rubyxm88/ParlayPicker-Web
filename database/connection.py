# database/connection.py

import sqlite3
from contextlib import contextmanager
import os

DB_PATH = os.getenv("DB_PATH", "parlay_data.db")

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# ✅ This is the alias expected by other files
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute(query, params=None):
    with get_connection() as conn:
        cursor = conn.execute(query, params or [])
        return cursor.fetchall()

def insert(query, params=None):
    with get_connection() as conn:
        cursor = conn.execute(query, params or [])
        return cursor.lastrowid

def bulk_insert(query, data):
    with get_connection() as conn:
        conn.executemany(query, data)

def table_exists(table_name):
    query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
    result = execute(query, [table_name])
    return bool(result)
