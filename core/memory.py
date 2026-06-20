import sqlite3
import os
import re

DB_PATH = "db/memory.db"


# =========================
# DATABASE INIT
# =========================

def init_db():
    os.makedirs("db", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memory (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        bot TEXT
    )
    """)

    conn.commit()
    conn.close()


# =========================
# CHAT HISTORY
# =========================

def save_chat(user, bot):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO chat (user, bot) VALUES (?, ?)",
        (user, bot)
    )

    conn.commit()
    conn.close()


# =========================
# MEMORY SYSTEM
# =========================

def set_memory(key, value):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR REPLACE INTO memory
        (key, value)
        VALUES (?, ?)
        """,
        (key, value)
    )

    conn.commit()
    conn.close()


def get_memory(key):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "SELECT value FROM memory WHERE key=?",
        (key,)
    )

    data = cur.fetchone()

    conn.close()

    if data:
        return data[0]

    return None


def get_all_memory():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("SELECT key, value FROM memory")

    data = cur.fetchall()

    conn.close()

    return data


def delete_memory(key):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM memory WHERE key=?",
        (key,)
    )

    conn.commit()
    conn.close()


# =========================
# TEXT NORMALIZER
# =========================

def normalize(text):
    text = text.lower()

    slang = {
        "gw": "saya",
        "gue": "saya",
        "aku": "saya"
    }

    for old, new in slang.items():
        text = text.replace(old, new)

    return text


# =========================
# AUTO LEARN V2
# =========================

def auto_learn(text):
    text = normalize(text)

    patterns = [
        (
            r"nama saya (.+)",
            "name",
            "Nama kamu aku ingat 👍"
        ),
        (
            r"saya suka (.+)",
            "favorite",
            "Oke, kamu suka {}"
        ),
        (
            r"saya pakai (.+)",
            "device",
            "Sip, perangkat kamu {}"
        ),
        (
            r"proyek saya (.+)",
            "project",
            "Aku catat proyek kamu {}"
        )
    ]

    for pattern, key, message in patterns:
        match = re.search(pattern, text)

        if match:
            value = match.group(1).strip()

            set_memory(key, value)

            if "{}" in message:
                return message.format(value)

            return message

    return None


# =========================
# BUILD AI CONTEXT
# =========================

def build_memory_context():
    memories = get_all_memory()

    if not memories:
        return ""

    result = "User profile:\n"

    for key, value in memories:
        result += f"- {key}: {value}\n"

    return result
