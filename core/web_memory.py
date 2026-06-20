import os
import json
import time

BASE_DIR = "WebMemory"


def ensure():
    os.makedirs(BASE_DIR, exist_ok=True)


def save_web_project(name, prompt, files, platform="unknown"):
    ensure()

    data = {
        "name": name,
        "prompt": prompt,
        "files": files,
        "platform": platform,
        "created_at": time.time()
    }

    path = os.path.join(BASE_DIR, f"{name}.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return path


def load_web_project(name):
    path = os.path.join(BASE_DIR, f"{name}.json")

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_web_projects():
    ensure()
    return os.listdir(BASE_DIR)
