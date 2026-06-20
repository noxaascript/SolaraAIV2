import os

BASE_DIR = "workspaces"


def ensure():
    os.makedirs(BASE_DIR, exist_ok=True)


def create_workspace(name):
    ensure()
    path = os.path.join(BASE_DIR, name)

    if os.path.exists(path):
        return "Workspace already exists"

    os.makedirs(path)
    return f"Workspace created: {name}"


def list_workspaces():
    ensure()
    return os.listdir(BASE_DIR)


def read_workspace(name):
    path = os.path.join(BASE_DIR, name)

    if not os.path.exists(path):
        return "Workspace not found"

    return os.listdir(path)


def add_file(ws, file_name, content):
    ensure()

    path = os.path.join(BASE_DIR, ws)

    if not os.path.exists(path):
        return "Workspace not found"

    with open(os.path.join(path, file_name), "w", encoding="utf-8") as f:
        f.write(content)

    return "File created"


# IMPORTANT: dipakai router
def auto_app(name, prompt):
    ensure()

    path = os.path.join(BASE_DIR, name)

    if os.path.exists(path):
        return "Workspace already exists"

    os.makedirs(path, exist_ok=True)

    html = f"""<!DOCTYPE html>
<html>
<head>
<title>{name}</title>
</head>
<body>
<h1>{name}</h1>
<p>{prompt}</p>
</body>
</html>
"""

    with open(os.path.join(path, "index.html"), "w") as f:
        f.write(html)

    return f"APP CREATED: {name}"
