import json
import os
import time

FILE = "memory.json"


def load_memory():
    if not os.path.exists(FILE):
        return {}
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_memory_db(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_memory(user_id, prompt, result):
    db = load_memory()
    if user_id not in db:
        db[user_id] = []
    db[user_id].append({
        "timestamp": time.time(),
        "prompt":    prompt,
        "result":    str(result),
    })
    if len(db[user_id]) > 50:
        db[user_id] = db[user_id][-50:]
    save_memory_db(db)


def get_memory(user_id):
    db = load_memory()
    return db.get(user_id, [])


def get_context(user_id, limit=5):
    memory = get_memory(user_id)
    if not memory:
        return "No previous memory."
    recent = memory[-limit:]
    context = ""
    for item in recent:
        context += f"\nUser: {item['prompt']}\nAI: {item['result']}\n"
    return context.strip()


def clear_memory(user_id=None):
    db = load_memory()
    if user_id:
        db[user_id] = []
    else:
        db = {}
    save_memory_db(db)
    return "Memory cleared"


# ── Aliases used by main.py ──────────────────────────────

def get_history(user_id="user", limit=10):
    """Return the last N memory entries as plain strings."""
    entries = get_memory(user_id)[-limit:]
    return [
        f"[{time.strftime('%H:%M', time.localtime(e['timestamp']))}] "
        f"You: {e['prompt'][:60]}  |  AI: {e['result'][:60]}"
        for e in entries
    ]


def save_chat(prompt, response, user_id="user"):
    """Save a chat turn. Called as save_chat(prompt, response) from main.py."""
    add_memory(user_id, prompt, response)
