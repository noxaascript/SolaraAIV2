import os
import json
from datetime import datetime

BASE_DIR = "projects"


def create_project(name):
    os.makedirs(BASE_DIR, exist_ok=True)

    safe_name = name.lower().replace(" ", "_")
    folder = f"{BASE_DIR}/{safe_name}_{int(datetime.now().timestamp())}"

    os.makedirs(folder, exist_ok=True)

    meta = {
        "name": name,
        "created_at": str(datetime.now())
    }

    with open(f"{folder}/meta.json", "w") as f:
        json.dump(meta, f, indent=2)

    return folder


def save_code(folder, filename, code):
    path = f"{folder}/{filename}"

    with open(path, "w") as f:
        f.write(code)

    return path
