import json
import os

FILE = "model_memory.json"


def load():
    if not os.path.exists(FILE):
        return {}
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_scores(user_id):
    data = load()
    return data.get(user_id, {})


def update_score(user_id, model, score):
    data = load()
    if user_id not in data:
        data[user_id] = {}
    if model not in data[user_id]:
        data[user_id][model] = 0.0
    data[user_id][model] = (data[user_id][model] + score) / 2
    save(data)
