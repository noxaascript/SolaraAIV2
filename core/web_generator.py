def generate_website(name, prompt):
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <h1>{name}</h1>
    <p>{prompt}</p>

    <button onclick="alert('Hello from {name}')">
        Click Me
    </button>

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
console.log("Website loaded");
"""

    return {
        "index.html": html,
        "style.css": css,
        "script.js": js
    }
