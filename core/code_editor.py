import os
import time
import shutil


# =========================
# CONFIG
# =========================

BACKUP_FOLDER = "backups"

ALLOWED_EXTENSIONS = [
    ".py",
    ".html",
    ".css",
    ".js",
    ".json",
    ".txt",
    ".md"
]


# =========================
# INIT SYSTEM
# =========================

def init_editor():

    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)


# =========================
# VALIDATE FILE
# =========================

def is_allowed(path):

    ext = os.path.splitext(path)[1]

    return ext in ALLOWED_EXTENSIONS


# =========================
# CREATE BACKUP
# =========================

def create_backup(path):

    init_editor()

    if not os.path.exists(path):
        return None


    filename = os.path.basename(path)

    timestamp = int(time.time())


    backup_path = (
        f"{BACKUP_FOLDER}/"
        f"{timestamp}_{filename}"
    )


    shutil.copy(path, backup_path)


    return backup_path


# =========================
# READ FILE
# =========================

def read_file(path):

    try:

        if not os.path.exists(path):
            return "File not found"


        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()


    except Exception as e:

        return f"Read error: {e}"


# =========================
# WRITE FILE
# =========================

def write_file(path, content):

    try:

        if not is_allowed(path):
            return "File type not allowed"


        create_backup(path)


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)


        return (
            f"File saved successfully\n"
            f"Path: {path}"
        )


    except Exception as e:

        return f"Write error: {e}"


# =========================
# APPEND FILE
# =========================

def append_file(path, content):

    try:

        if not is_allowed(path):
            return "File type not allowed"


        create_backup(path)


        with open(
            path,
            "a",
            encoding="utf-8"
        ) as f:

            f.write(content)


        return (
            "Content added successfully"
        )


    except Exception as e:

        return f"Append error: {e}"


# =========================
# CREATE NEW FILE
# =========================

def create_file(path, content=""):

    try:

        if os.path.exists(path):
            return "File already exists"


        folder = os.path.dirname(path)

        if folder:
            os.makedirs(
                folder,
                exist_ok=True
            )


        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(content)


        return (
            f"New file created: {path}"
        )


    except Exception as e:

        return f"Create error: {e}"


# =========================
# REPLACE TEXT
# =========================

def replace_text(
    path,
    old,
    new
):

    text = read_file(path)


    if text.startswith(
        "File not found"
    ):
        return text


    create_backup(path)


    text = text.replace(
        old,
        new
    )


    return write_file(
        path,
        text
    )


# =========================
# PROJECT SCANNER
# =========================

def scan_project(folder="."):

    result = []


    for root, dirs, files in os.walk(folder):

        for file in files:

            if is_allowed(file):

                result.append(
                    os.path.join(
                        root,
                        file
                    )
                )


    return result


# =========================
# DELETE FILE
# =========================

def delete_file(path):

    try:

        if not os.path.exists(path):
            return "File not found"


        create_backup(path)


        os.remove(path)


        return (
            f"Deleted: {path}"
        )


    except Exception as e:

        return f"Delete error: {e}"
