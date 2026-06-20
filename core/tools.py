import requests
import os
from core.workspace import create_workspace, add_file
from core.website_pipeline import create_web_project


# =========================
# WEB FETCH TOOL (BASIC BROWSER)
# =========================
def fetch_url(url):
    try:
        r = requests.get(url, timeout=10)
        return r.text[:3000]  # limit biar gak overload
    except Exception as e:
        return f"Fetch error: {str(e)}"


# =========================
# WORKSPACE TOOL
# =========================
def tool_workspace_create(name):
    return create_workspace(name)


def tool_workspace_add(ws, file, content):
    return add_file(ws, file, content)


# =========================
# WEB GENERATOR TOOL
# =========================
def tool_create_web(name, prompt):
    return create_web_project(name, prompt)


# =========================
# TOOL ROUTER (MAIN ENTRY)
# =========================
def run_tool(tool_name, *args):

    # ================= WEB =================
    if tool_name == "fetch":
        return fetch_url(*args)

    # ================= WORKSPACE =================
    if tool_name == "ws_create":
        return tool_workspace_create(*args)

    if tool_name == "ws_add":
        return tool_workspace_add(*args)

    # ================= WEB AI =================
    if tool_name == "web_create":
        return tool_create_web(*args)

    return f"Unknown tool: {tool_name}"
