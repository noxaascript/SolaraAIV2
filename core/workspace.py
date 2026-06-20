import os
import json

BASE_DIR = "workspaces"


def ensure_base():
    os.makedirs(BASE_DIR, exist_ok=True)


def create_workspace(name):
    ensure_base()

    path = os.path.join(BASE_DIR, name)

    if os.path.exists(path):
        return "Workspace already exists"

    os.makedirs(path)
    return f"Workspace created: {name}"


def list_workspaces():
    ensure_base()

    return os.listdir(BASE_DIR)


def add_file(ws_name, file_name, content):
    ensure_base()

    path = os.path.join(BASE_DIR, ws_name)

    if not os.path.exists(path):
        return "Workspace not found"

    file_path = os.path.join(path, file_name)

    with open(file_path, "w") as f:
        f.write(content)

    return f"File created: {file_name}"


def read_workspace(ws_name):
    path = os.path.join(BASE_DIR, ws_name)

    if not os.path.exists(path):
        return "Workspace not found"

    files = os.listdir(path)

    return {
        "workspace": ws_name,
        "files": files
    }
