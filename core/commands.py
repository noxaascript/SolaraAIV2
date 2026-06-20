from core.memory import (
    get_all_memory,
    delete_memory
)

from core.model_manager import (
    get_model,
    list_models,
    set_model
)


def run_tool(user_input):
    cmd = user_input.strip()

    # =========================
    # HELP
    # =========================

    if cmd == "/help":
        return """
Commands:

Memory:
/memory - show all memories
/forget <key> - delete memory

AI:
/model - current model
/models - list models
/setmodel <id> - change model

System:
/ping
/version
"""

    # =========================
    # MEMORY COMMANDS
    # =========================

    if cmd == "/memory":
        memories = get_all_memory()

        if not memories:
            return "Memory is empty"

        result = "🧠 Solara Memory:\n"

        for key, value in memories:
            result += f"- {key}: {value}\n"

        return result


    if cmd.startswith("/forget"):
        parts = cmd.split()

        if len(parts) < 2:
            return "Usage: /forget <key>"

        key = parts[1]

        delete_memory(key)

        return f"Forgot memory: {key}"


    # =========================
    # MODEL COMMANDS
    # =========================

    if cmd == "/model":
        model = get_model()

        return (
            f"Current model:\n"
            f"{model['name']}\n"
            f"Provider: {model['provider']}"
        )


    if cmd == "/models":
        models = list_models()

        result = "Available models:\n"

        for key, value in models.items():
            result += (
                f"{key}. {value['name']} "
                f"({value['provider']})\n"
            )

        return result


    if cmd.startswith("/setmodel"):
        parts = cmd.split()

        if len(parts) < 2:
            return "Usage: /setmodel 1, 2, 3..."

        return set_model(parts[1])


    # =========================
    # SYSTEM
    # =========================

    if cmd == "/ping":
        return "pong 🟢"


    if cmd == "/version":
        return "SolaraAI V2"


    # Unknown command
    return None
