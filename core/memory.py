import json
import os
import time

FILE = "memory.json"


# =========================
# LOAD MEMORY DATABASE
# =========================
def load_memory():

    if not os.path.exists(FILE):
        return {}

    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {}


# =========================
# SAVE MEMORY DATABASE
# =========================
def save_memory_db(data):

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


# =========================
# ADD MEMORY (USER CONTEXT)
# =========================
def add_memory(user_id, prompt, result):

    db = load_memory()

    if user_id not in db:
        db[user_id] = []

    db[user_id].append({
        "timestamp": time.time(),
        "prompt": prompt,
        "result": str(result)
    })

    # limit memory biar gak berat
    if len(db[user_id]) > 50:
        db[user_id] = db[user_id][-50:]

    save_memory_db(db)


# =========================
# GET USER MEMORY
# =========================
def get_memory(user_id):

    db = load_memory()
    return db.get(user_id, [])


# =========================
# GET CONTEXT STRING (FOR AI)
# =========================
def get_context(user_id, limit=5):

    memory = get_memory(user_id)

    if not memory:
        return "No previous memory."

    recent = memory[-limit:]

    context = ""

    for item in recent:
        context += f"""
User: {item['prompt']}
AI: {item['result']}
"""

    return context.strip()


# =========================
# CLEAR MEMORY (OPTIONAL TOOL)
# =========================
def clear_memory(user_id=None):

    db = load_memory()

    if user_id:
        db[user_id] = []
    else:
        db = {}

    save_memory_db(db)

    return "Memory cleared"
