import json
import os

PATH = "brain_memory.json"


def load():
    if not os.path.exists(PATH):
        return {}

    with open(PATH, "r") as f:
        return json.load(f)


def save(data):
    with open(PATH, "w") as f:
        json.dump(data, f, indent=2)


def learn_pattern(user_input, response):
    data = load()

    key = user_input.lower().strip()

    if key not in data:
        data[key] = {
            "count": 0,
            "best_response": response
        }

    data[key]["count"] += 1

    save(data)


def get_learned(user_input):
    data = load()

    return data.get(user_input.lower().strip())
