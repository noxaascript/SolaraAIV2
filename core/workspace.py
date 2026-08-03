import os

BASE = "workspaces"


def ensure():
    os.makedirs(BASE, exist_ok=True)


def create_workspace(name):
    ensure()
    path = os.path.join(BASE, name)

    if os.path.exists(path):
        return "exists"

    os.makedirs(path)
    return f"workspace {name} created"


def list_workspaces():
    ensure()
    return os.listdir(BASE)


def read_workspace(name):
    path = os.path.join(BASE, name)
    return os.listdir(path) if os.path.exists(path) else "not found"


def add_file(ws, file, content):
    ensure()
    path = os.path.join(BASE, ws)

    if not os.path.exists(path):
        return "not found"

    with open(os.path.join(path, file), "w") as f:
        f.write(content)

    return "file added"


def auto_app(name, prompt):
    ensure()
    path = os.path.join(BASE, name)

    if os.path.exists(path):
        return "exists"

    os.makedirs(path)

    with open(os.path.join(path, "index.html"), "w") as f:
        f.write(f"<h1>{name}</h1><p>{prompt}</p>")

    return "app created"
