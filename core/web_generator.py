def generate_website(name, prompt):
    return {
        "index.html": f"<h1>{name}</h1><p>{prompt}</p>",
        "style.css": "body{font-family:Arial;background:#111;color:white;}",
        "script.js": "console.log('loaded');"
    }
