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


def get_memory(key):
    return load().get(key)


def set_memory(key, value):
    data = load()
    data[key] = value
    save(data)
