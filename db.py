import json
import sqlite3

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            payload TEXT
        )
    """)
    conn.commit()
    conn.close()
    return True

def insert_record(db_path, record):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO records VALUES (?, ?, ?)",
        (record["id"], record["timestamp"], json.dumps(record["payload"]))
    )
    conn.commit()
    conn.close()
    return True