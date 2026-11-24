import sqlite3
import os
from pathlib import Path
from contextlib import contextmanager

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "musiq_ai.db"

def get_db_path():
    return os.getenv("MUSIQ_DB_PATH", str(DEFAULT_DB_PATH))

def _create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            pref_key TEXT PRIMARY KEY,
            pref_value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_preferences (
            activity TEXT PRIMARY KEY,
            genre TEXT,
            mood TEXT,
            language TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS track_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            track_title TEXT NOT NULL,
            artist_name TEXT,
            video_id TEXT,
            is_liked INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(track_title, artist_name)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlist_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playlist_name TEXT NOT NULL,
            description TEXT,
            duration_seconds INTEGER,
            track_count INTEGER,
            video_ids_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

@contextmanager
def get_db_connection():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    _create_tables(conn)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        _create_tables(conn)

init_db()
