from core.workspace import (
    create_workspace,
    list_workspaces,
    read_workspace,
    add_file,
    auto_app
)

from core.website_pipeline import create_web_project

from core.memory import get_memory, set_memory


# =========================
# SIMPLE MODEL STORE (LOCAL)
# =========================
MODELS = {
    "1": {"name": "llama3-8b", "provider": "groq"},
    "2": {"name": "mixtral", "provider": "groq"},
    "3": {"name": "qwen", "provider": "hf"},
}


def get_selected_model():
    return get_memory("model") or "1"


def set_selected_model(model_id):
    if model_id not in MODELS:
        return "Model not found"

    set_memory("model", model_id)
    return f"Model set to {MODELS[model_id]['name']}"


# =========================
# MAIN ROUTER
# =========================
def run_tool(user_input):
    cmd = user_input.strip().lower()

    # =========================
    # HELP
    # =========================
    if cmd == "/help":
        return """
=== SOLARA AI ===

[MODEL]
/model list
/model select <id>
/model current

[WORKSPACE]
/workspace create <name>
/workspace list
/workspace open <name>
/workspace addfile <ws> <file> <content>

[WEB]
/web create <name> <prompt>

[SYSTEM]
/ping
/version
"""

    # =========================
    # MODEL LIST
    # =========================
    if cmd == "/model list":
        out = "Available Models:\n"
        for k, v in MODELS.items():
            out += f"{k}. {v['name']} ({v['provider']})\n"
        return out


    # =========================
    # MODEL SELECT
    # =========================
    if cmd.startswith("/model select"):
        parts = cmd.split()

        if len(parts) < 3:
            return "Usage: /model select <id>"

        return set_selected_model(parts[2])


    # =========================
    # CURRENT MODEL
    # =========================
    if cmd == "/model current":
        mid = get_selected_model()
        m = MODELS.get(mid, {})
        return f"Current model: {m.get('name')} ({m.get('provider')})"


    # =========================
    # WORKSPACE
    # =========================
    if cmd.startswith("/workspace create"):
        return create_workspace(cmd.split()[2])

    if cmd == "/workspace list":
        return "\n".join(list_workspaces())

    if cmd.startswith("/workspace open"):
        return str(read_workspace(cmd.split()[2]))

    if cmd.startswith("/workspace addfile"):
        parts = cmd.split()
        return add_file(parts[2], parts[3], " ".join(parts[4:]))

    if cmd.startswith("/workspace ai"):
        parts = cmd.split()
        return auto_app(parts[3], " ".join(parts[4:]))

    # =========================
    # WEB AI
    # =========================
    if cmd.startswith("/web create"):
        parts = cmd.split()
        return create_web_project(parts[2], " ".join(parts[3:]))

    # =========================
    # SYSTEM
    # =========================
    if cmd == "/ping":
        return "pong 🟢"

    if cmd == "/version":
        return "SolaraAI V2"

    return None
