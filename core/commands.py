from core.model_manager import set_model, list_models, get_model


def run_tool(user_input):
    cmd = user_input.strip().lower()

    # ======================
    # HELP
    # ======================
    if cmd == "/help":
        return get_help()

    # ======================
    # PING
    # ======================
    if cmd == "/ping":
        return "pong 🟢"

    # ======================
    # VERSION
    # ======================
    if cmd == "/version":
        return "SolaraAI v1.0"

    # ======================
    # MODEL SYSTEM
    # ======================
    if cmd == "/model":
        m = get_model()
        return f"current model → {m['name']} ({m['provider']})"

    if cmd == "/models":
        models = list_models()

        result = "available models:\n"
        for k, v in models.items():
            result += f"{k}: {v['name']} ({v['provider']})\n"

        return result

    if cmd.startswith("/setmodel"):
        parts = cmd.split()

        if len(parts) < 2:
            return "usage: /setmodel 1|2|3"

        return set_model(parts[1])

    return None


def get_help():
    return """
commands:
/help - show help
/ping - test bot
/version - show version

/model - show current model
/models - list models
/setmodel <id> - change model
"""
