import sqlite3
import os

DB_PATH = "db/memory.db"


def init_db():
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        bot TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    conn.commit()
    conn.close()


def save_chat(user, bot):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("INSERT INTO chat (user, bot) VALUES (?, ?)", (user, bot))

    conn.commit()
    conn.close()


def set_memory(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT OR REPLACE INTO memory (key, value)
    VALUES (?, ?)
    """, (key, value))

    conn.commit()
    conn.close()


def get_memory(key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT value FROM memory WHERE key=?", (key,))
    row = c.fetchone()

    conn.close()

    return row[0] if row else None


# 🧠 auto learn sederhana
def auto_learn(text):
    text = text.lower()

    if "nama saya" in text:
        name = text.split("nama saya")[-1].strip()
        set_memory("name", name)
        return f"oke, aku ingat kamu {name}"

    if "panggil aku" in text:
        name = text.split("panggil aku")[-1].strip()
        set_memory("name", name)
        return f"oke {name}"

    return None
