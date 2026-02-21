import json
import logging
import os
import sqlite3


def init_db(db_path):
    """Create tables if needed. Returns True if tables exist/created, False on failure."""
    try:
        parent = os.path.dirname(db_path)
        if parent:
            os.makedirs(parent, exist_ok=True)
        conn = sqlite3.connect(os.path.abspath(db_path))
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS records (
                id TEXT PRIMARY KEY,
                timestamp TEXT,
                payload TEXT
            )
        """
        )

        conn.commit()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='records'"
        )
        exists = cursor.fetchone() is not None
        conn.close()

        return exists
    except sqlite3.Error as e:
        logging.error(f"init_db failed: {e}")

        return False


def insert_record(db_path, record):
    try:
        path = os.path.abspath(db_path)
        with sqlite3.connect(path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO records (id, timestamp, payload) VALUES (?, ?, ?)",
                (record["id"], record["timestamp"], json.dumps(record["payload"])),
            )
            conn.commit()

        return True
    except (KeyError, TypeError) as e:
        logging.error(f"Invalid record structure: {e}")

        return False
    except sqlite3.Error as e:
        logging.error(f"Insert failed: {e}")

        return False
