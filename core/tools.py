import requests
import os


# =========================
# MAIN TOOL ENTRY
# =========================
def run_tool(name, *args):

    # =========================
    # WEB FETCH TOOL (RAW)
    # =========================
    if name == "fetch":
        url = args[0] if args else None
        return fetch(url)

    # =========================
    # CLEAN WEB SCRAPE TOOL
    # =========================
    if name == "fetch_clean":
        url = args[0] if args else None
        return fetch_clean(url)

    # =========================
    # WORKSPACE TOOL
    # =========================
    if name == "ws_create":
        return workspace_create(*args)

    # =========================
    # WEB GENERATOR TOOL
    # =========================
    if name == "web_create":
        return web_create(*args)

    return f"Unknown tool: {name}"


# =========================
# RAW FETCH (BROWSER BASIC)
# =========================
def fetch(url):

    if not url:
        return "No URL provided"

    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=10)

        return r.text[:3000]

    except Exception as e:
        return f"fetch error: {str(e)}"


# =========================
# CLEAN FETCH (TEXT ONLY BROWSER)
# =========================
def fetch_clean(url):

    if not url:
        return "No URL provided"

    try:
        from bs4 import BeautifulSoup

        headers = {"User-Agent": "Mozilla/5.0"}

        r = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator="\n")

        lines = [line.strip() for line in text.splitlines()]
        clean = "\n".join([l for l in lines if l])

        return clean[:4000]

    except Exception as e:
        return f"browser error: {str(e)}"


# =========================
# WORKSPACE CREATOR
# =========================
def workspace_create(name="project"):

    try:
        os.makedirs(name, exist_ok=True)

        main_file = os.path.join(name, "main.py")

        with open(main_file, "w") as f:
            f.write("# auto generated workspace\nprint('hello world')\n")

        return f"Workspace created: {name}"

    except Exception as e:
        return f"workspace error: {str(e)}"


# =========================
# WEB PROJECT GENERATOR
# =========================
def web_create(name, prompt=""):

    try:
        os.makedirs(name, exist_ok=True)

        html_file = os.path.join(name, "index.html")

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{name}</title>
</head>
<body>
    <h1>Auto Generated Site</h1>
    <p>{prompt}</p>
</body>
</html>
"""

        with open(html_file, "w") as f:
            f.write(html_content)

        return f"Web project created: {name}"

    except Exception as e:
        return f"web error: {str(e)}"
