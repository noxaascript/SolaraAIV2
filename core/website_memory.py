import os
import json
import time

BASE = "website_memory"


def ensure():
    os.makedirs(BASE, exist_ok=True)


def save_project(name, prompt, files):
    ensure()

    data = {
        "name": name,
        "prompt": prompt,
        "files": files,
        "timestamp": time.time()
    }

    path = os.path.join(BASE, f"{name}.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    return path


def load_project(name):
    path = os.path.join(BASE, f"{name}.json")

    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        return json.load(f)


def list_projects():
    ensure()
    return os.listdir(BASE)
