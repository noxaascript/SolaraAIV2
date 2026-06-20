import sqlite3
import os
import re

DB_PATH = "db/memory.db"


# ======================
# INIT DB
# ======================
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


# ======================
# CHAT SAVE
# ======================
def save_chat(user, bot):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("INSERT INTO chat (user, bot) VALUES (?, ?)", (user, bot))

    conn.commit()
    conn.close()


# ======================
# MEMORY CORE
# ======================
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


# ======================
# NORMALIZER (slang fix)
# ======================
def normalize(text):
    t = text.lower()

    slang = {
        "gw": "saya",
        "gue": "saya",
        "aku": "saya",
    }

    for k, v in slang.items():
        t = t.replace(k, v)

    return t


# ======================
# AUTO LEARN (smart)
# ======================
def auto_learn(text):
    text = normalize(text)

    patterns = [
        r"nama (saya)\s*[:\-]?\s*(.+)",
        r"panggil aku\s+(.+)"
    ]

    for p in patterns:
        match = re.search(p, text)
        if match:
            name = match.group(len(match.groups())).strip()
            set_memory("name", name)
            return f"oke, aku ingat nama kamu {name}"

    return None
