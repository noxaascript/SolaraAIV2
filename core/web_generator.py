def generate_website(name, prompt):
    html = f"""<!DOCTYPE html>
<html>
<head>
<title>{name}</title>
<style>
body {{
    font-family: Arial;
    background: #111;
    color: white;
    text-align: center;
    padding-top: 100px;
}}
</style>
</head>
<body>

<h1>{name}</h1>
<p>{prompt}</p>

<button onclick="alert('Hello from {name}')">Click</button>

</body>
</html>
"""

    return {
        "index.html": html,
        "style.css": "",
        "script.js": "console.log('loaded')"
    }
