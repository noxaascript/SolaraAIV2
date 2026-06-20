import os

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

    return os.listdir(path)


# =========================
# 🧠 AI WORKSPACE GENERATOR
# =========================

def ai_generate_workspace(ws_name, prompt):
    ensure_base()

    path = os.path.join(BASE_DIR, ws_name)

    if os.path.exists(path):
        return "Workspace already exists"

    os.makedirs(path, exist_ok=True)

    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{ws_name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="container">
        <h1>{ws_name}</h1>
        <p>{prompt}</p>
    </div>

    <script src="script.js"></script>
</body>
</html>
"""

    css = """
body {
    font-family: Arial;
    background: #111;
    color: white;
    text-align: center;
    margin: 0;
}

.container {
    margin-top: 100px;
}
"""

    js = """
console.log("AI Workspace Loaded");
"""

    files = {
        "index.html": html,
        "style.css": css,
        "script.js": js
    }

    for file_name, content in files.items():
        file_path = os.path.join(path, file_name)

        with open(file_path, "w") as f:
            f.write(content)

    return f"AI Workspace created: {ws_name}"
