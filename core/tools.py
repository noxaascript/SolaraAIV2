import requests

# BrowserOS import
from browser_os.agent import agent as browser_agent


# =========================
# MAIN TOOL ROUTER
# =========================
def run_tool(name, *args):

    # =========================
    # BASIC FETCH
    # =========================
    if name == "fetch":
        return fetch(args[0])

    # =========================
    # CLEAN FETCH
    # =========================
    if name == "fetch_clean":
        return fetch_clean(args[0])

    # =========================
    # WORKSPACE
    # =========================
    if name == "ws_create":
        return f"Workspace created: {args}"

    # =========================
    # WEB PROJECT
    # =========================
    if name == "web_create":
        return f"Web created: {args}"

    # =========================
    # 🌐 BROWSEROS INTEGRATION
    # =========================
    if name == "browser_visit":
        url = args[0]
        return browser_agent.visit(url)

    if name == "browser_summary":
        url = args[0]
        return browser_agent.summarize(url)

    return f"Unknown tool: {name}"


# =========================
# RAW FETCH
# =========================
def fetch(url):

    try:
        r = requests.get(url, timeout=10)
        return r.text[:3000]
    except Exception as e:
        return f"fetch error: {e}"


# =========================
# CLEAN FETCH
# =========================
def fetch_clean(url):

    try:
        from bs4 import BeautifulSoup

        r = requests.get(url, timeout=10)

        soup = BeautifulSoup(r.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.decompose()

        return soup.get_text()[:4000]

    except Exception as e:
        return f"browser error: {e}"
