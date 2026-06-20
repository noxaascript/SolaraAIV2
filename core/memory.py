import sqlite3
from config import DB_PATH

# 🔥 init db
def init_db():
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


# 💾 save chat
def save_chat(user, bot):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("INSERT INTO chat (user, bot) VALUES (?, ?)", (user, bot))

    conn.commit()
    conn.close()


# 🧠 store memory (key-value)
def set_memory(key, value):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    INSERT OR REPLACE INTO memory (key, value)
    VALUES (?, ?)
    """, (key, value))

    conn.commit()
    conn.close()


# 🧠 get memory
def get_memory(key):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT value FROM memory WHERE key=?", (key,))
    row = c.fetchone()

    conn.close()

    return row[0] if row else None
