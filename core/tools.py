from core.browser import fetch_url

TOOLS = {}


def register_tool(name, func):
    TOOLS[name] = func


def run_tool(name, *args):
    if name not in TOOLS:
        return "Tool not found"

    return TOOLS[name](*args)


def list_tools():
    return list(TOOLS.keys())


# =========================
# DEFAULT TOOL REGISTRATION
# =========================

register_tool("browser", fetch_url)


# optional chrome bridge (kalau sudah ada chrome_bridge.py)
try:
    from core.chrome_bridge import send_to_chrome

    register_tool("chrome_open", lambda url: send_to_chrome("open", url))
    register_tool("chrome_tabs", lambda: send_to_chrome("tabs"))

except:
    pass
