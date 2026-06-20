import os

BASE = "workspaces"


def ensure():
    os.makedirs(BASE, exist_ok=True)


def auto_app(name, prompt):
    ensure()

    path = os.path.join(BASE, name)

    if os.path.exists(path):
        return "Workspace already exists"

    os.makedirs(path)

    html = f"""<!DOCTYPE html>
<html>
<head>
<title>{name}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>

<h1>{name}</h1>
<p>{prompt}</p>

<button onclick="alert('Hello from {name}')">Click</button>

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
    padding-top: 100px;
}
"""

    js = """
console.log("App running");
"""

    files = {
        "index.html": html,
        "style.css": css,
        "script.js": js
    }

    for k, v in files.items():
        with open(os.path.join(path, k), "w") as f:
            f.write(v)

    return f"APP GENERATED: {name}"
