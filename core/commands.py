from core.memory import get_memory, set_memory
from core.workspace import create_workspace, list_workspaces, read_workspace, add_file
from core.website_pipeline import create_web_project


# =========================
# MODELS
# =========================
MODELS = {
    "1": "llama3-8b-8192",
    "2": "mixtral-8x7b",
    "3": "gemma2-9b-it"
}


def get_selected_model():
    return get_memory("model") or "1"


def set_selected_model(mid):
    if mid not in MODELS:
        return "Model not found"

    set_memory("model", mid)
    return f"Model set to {MODELS[mid]}"


# =========================
# COMMAND ROUTER
# =========================
def run_tool(user_input):
    cmd = user_input.strip().lower()

    # HELP
    if cmd == "/help":
        return """
/model list
/model select <id>
/model current

/workspace create <name>
/workspace list
/workspace open <name>
/workspace addfile <ws> <file> <content>

/web create <name> <prompt>

/ping
/version
"""

    # MODEL LIST
    if cmd == "/model list":
        out = ""
        for k, v in MODELS.items():
            out += f"{k}. {v}\n"
        return out

    # MODEL SELECT
    if cmd.startswith("/model select"):
        parts = cmd.split()
        return set_selected_model(parts[2])

    # MODEL CURRENT
    if cmd == "/model current":
        mid = get_selected_model()
        return f"Current model: {MODELS[mid]}"

    # WORKSPACE
    if cmd.startswith("/workspace create"):
        return create_workspace(cmd.split()[2])

    if cmd == "/workspace list":
        return "\n".join(list_workspaces())

    if cmd.startswith("/workspace open"):
        return str(read_workspace(cmd.split()[2]))

    if cmd.startswith("/workspace addfile"):
        p = cmd.split()
        return add_file(p[2], p[3], " ".join(p[4:]))

    # WEB
    if cmd.startswith("/web create"):
        p = cmd.split()
        return create_web_project(p[2], " ".join(p[3:]))

    # SYSTEM
    if cmd == "/ping":
        return "pong"

    if cmd == "/version":
        return "SolaraAI V2"

    return None
