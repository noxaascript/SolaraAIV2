import json
import os
import time


FILE = "browser_history.json"


def load_history():

    if not os.path.exists(FILE):
        return []

    try:
        with open(FILE, "r") as f:
            return json.load(f)

    except:
        return []


def save_history(data):

    with open(FILE, "w") as f:
        json.dump(
            data,
            f,
            indent=2
        )


def add_history(url, action):

    data = load_history()

    data.append({
        "time": time.time(),
        "url": url,
        "action": action
    })

    save_history(data)


def get_history():

    return load_history()


def clear_history():

    save_history([])

    return "Browser history cleared"
