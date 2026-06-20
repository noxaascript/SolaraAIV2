import os
import json
import time

BASE_DIR = "WebMemory"
MAIN_FILE = os.path.join(BASE_DIR, "web.txt")


# =========================
# INIT
# =========================
def ensure():
    os.makedirs(BASE_DIR, exist_ok=True)

    # bikin file utama kalau belum ada
    if not os.path.exists(MAIN_FILE):
        with open(MAIN_FILE, "w", encoding="utf-8") as f:
            f.write("=== SOLARA WEB MEMORY LOG ===\n\n")


# =========================
# SAVE FULL PROJECT (JSON)
# =========================
def save_web_project(name, prompt, files, platform="auto"):
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


# =========================
# LOAD PROJECT
# =========================
def load_web_project(name):
    path = os.path.join(BASE_DIR, f"{name}.json")

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# =========================
# LIST PROJECTS
# =========================
def list_web_projects():
    ensure()
    return [
        f for f in os.listdir(BASE_DIR)
        if f.endswith(".json")
    ]


# =========================
# WRITE TO MAIN LOG FILE
# =========================
def save_to_main_file(name, prompt, files):
    ensure()

    content = f"""
========================
PROJECT NAME : {name}
PROMPT       : {prompt}
FILES        : {", ".join(files.keys())}
TIME         : {time.ctime()}
========================
"""

    with open(MAIN_FILE, "a", encoding="utf-8") as f:
        f.write(content + "\n")

    return "File Web tersimpan di WebMemory/web.txt"


# =========================
# READ MAIN LOG
# =========================
def read_main_log():
    ensure()

    with open(MAIN_FILE, "r", encoding="utf-8") as f:
        return f.read()
