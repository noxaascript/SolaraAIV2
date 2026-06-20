import os
import json
import time

BASE_DIR = "WebMemory"
MAIN_FILE = os.path.join(BASE_DIR, "web.txt")


def ensure():
    os.makedirs(BASE_DIR, exist_ok=True)

    if not os.path.exists(MAIN_FILE):
        with open(MAIN_FILE, "w", encoding="utf-8") as f:
            f.write("=== SOLARA WEB MEMORY ===\n\n")


def save_web_project(name, prompt, files, platform="auto"):
    ensure()

    data = {
        "name": name,
        "prompt": prompt,
        "files": files,
        "platform": platform,
        "created_at": time.time()
    }

    with open(os.path.join(BASE_DIR, f"{name}.json"), "w") as f:
        json.dump(data, f, indent=2)


def save_to_main_file(name, prompt, files):
    ensure()

    with open(MAIN_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n{name} | {prompt} | {list(files.keys())}\n")

    return "File Web tersimpan di WebMemory/web.txt"
