import json
import os
import time

FILE = "global_memory.json"

MAX_ITEMS = 500


# =========================
# LOAD DATABASE
# =========================

def load_global():

    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as f:
            return json.load(f)

    except Exception:
        return []


# =========================
# SAVE DATABASE
# =========================

def save_global(data):

    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


# =========================
# ADD GLOBAL KNOWLEDGE
# =========================

def learn(task, answer, category="general"):

    database = load_global()


    memory = {
        "time": time.time(),
        "category": category,
        "task": str(task),
        "answer": str(answer)
    }


    database.append(memory)


    # batasi ukuran database
    if len(database) > MAX_ITEMS:
        database = database[-MAX_ITEMS:]


    save_global(database)

    return "Global knowledge updated"


# =========================
# SEARCH KNOWLEDGE
# =========================

def search(query, limit=5):

    database = load_global()

    query = query.lower()

    results = []


    for item in database:

        text = (
            item["task"] +
            " " +
            item["answer"]
        ).lower()


        if query in text:
            results.append(item)


    return results[-limit:]


# =========================
# GET CONTEXT FOR AI
# =========================

def get_global_context(query):

    memories = search(query)


    if not memories:
        return "No global knowledge."


    context = "Global experience:\n\n"


    for m in memories:

        context += (
            f"Task: {m['task']}\n"
            f"Solution: {m['answer']}\n\n"
        )


    return context


# =========================
# SHOW STATS
# =========================

def stats():

    data = load_global()


    categories = {}


    for item in data:

        cat = item["category"]

        categories[cat] = (
            categories.get(cat, 0) + 1
        )


    return {
        "total_memories": len(data),
        "categories": categories
    }


# =========================
# RESET GLOBAL MEMORY
# =========================

def reset():

    save_global([])

    return "Global memory deleted"
