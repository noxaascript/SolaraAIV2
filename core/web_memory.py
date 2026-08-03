import os
import json
import time

BASE = "WebMemory"
LOG = f"{BASE}/web.txt"


def ensure():
    os.makedirs(BASE, exist_ok=True)

    if not os.path.exists(LOG):
        open(LOG, "w").write("WEB MEMORY LOG\n\n")


def save_web_project(name, prompt, files):
    ensure()

    with open(f"{BASE}/{name}.json", "w") as f:
        json.dump({
            "name": name,
            "prompt": prompt,
            "files": files,
            "time": time.time()
        }, f, indent=2)


def save_to_main_file(name, prompt, files):
    ensure()

    with open(LOG, "a") as f:
        f.write(f"{name} | {prompt} | {list(files.keys())}\n")

    return "saved"
