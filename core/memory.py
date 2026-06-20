import json
import os

FILE = "memory.json"


def load():
    if not os.path.exists(FILE):
        return {}
    return json.load(open(FILE))


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def save_memory(user_id, prompt, result):

    data = load()

    if user_id not in data:
        data[user_id] = []

    data[user_id].append({
        "prompt": prompt,
        "result": str(result)
    })

    save(data)
