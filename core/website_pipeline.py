import os

from core.web_generator import generate_website
from core.web_memory import save_web_project, save_to_main_file


BASE_DIR = "workspaces"


def ensure_ws():
    os.makedirs(BASE_DIR, exist_ok=True)


# =========================
# CREATE WEB PROJECT (MAIN)
# =========================
def create_web_project(name, prompt):
    ensure_ws()

    files = generate_website(name, prompt)

    # simpan ke WebMemory (JSON)
    save_web_project(name, prompt, files, platform="auto")

    # simpan ke log utama (web.txt)
    msg = save_to_main_file(name, prompt, files)

    # juga simpan ke workspace folder (biar bisa deploy)
    path = os.path.join(BASE_DIR, name)
    os.makedirs(path, exist_ok=True)

    for file_name, content in files.items():
        with open(os.path.join(path, file_name), "w", encoding="utf-8") as f:
            f.write(content)

    return msg
