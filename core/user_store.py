import json
import os

FILE = "users.json"


def load():
    if not os.path.exists(FILE):
        return {}
    return json.load(open(FILE))


def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_user(user_id):
    return load().get(user_id)


def set_user(user_id, data):
    db = load()
    db[user_id] = data
    save(db)


def get_key(user_id):
    user = get_user(user_id)
    return user.get("api_key") if user else None


def set_key(user_id, key):
    db = load()
    db[user_id] = db.get(user_id, {})
    db[user_id]["api_key"] = key
    save(db)
