from core.memory import (
    get_all_memory,
    delete_memory,
    set_memory,
    get_memory
)

from core.model_manager import (
    get_model,
    list_models,
    set_model
)

from core.personality import (
    get_modes
)


def run_tool(user_input):
    cmd = user_input.strip().lower()


    # HELP
    if cmd == "/help":
        return """
Commands:

Memory:
 /memory
 /forget <key>

Model:
 /model
 /models
 /setmodel <id>

Personality:
 /mode
 /modes
 /setmode <name>

System:
 /ping
 /version
"""


    # MEMORY
    if cmd == "/memory":
        data = get_all_memory()

        if not data:
            return "Memory is empty"

        result = "Solara Memory:\n"

        for key, value in data:
            result += f"- {key}: {value}\n"

        return result


    if cmd.startswith("/forget"):
        parts = cmd.split()

        if len(parts) < 2:
            return "Usage: /forget <key>"

        delete_memory(parts[1])
        return f"Forgot {parts[1]}"


    # MODEL
    if cmd == "/model":
        model = get_model()

        return (
            f"Current model:\n"
            f"{model['name']}\n"
            f"Provider: {model['provider']}"
        )


    if cmd == "/models":
        result = "Available models:\n"

        for key, value in list_models().items():
            result += (
                f"{key}. {value['name']} "
                f"({value['provider']})\n"
            )

        return result


    if cmd.startswith("/setmodel"):
        parts = cmd.split()

        if len(parts) < 2:
            return "Usage: /setmodel <id>"

        return set_model(parts[1])


    # PERSONALITY
    if cmd == "/mode":
        mode = get_memory("personality")

        if not mode:
            mode = "normal"

        return f"Current mode: {mode}"


    if cmd == "/modes":
        result = "Available modes:\n"

        for mode in get_modes():
            result += f"- {mode}\n"

        return result


    if cmd.startswith("/setmode"):
        parts = cmd.split()

        if len(parts) < 2:
            return "Usage: /setmode <mode>"

        mode = parts[1]

        if mode not in get_modes():
            return "Invalid mode. Use /modes"

        set_memory("personality", mode)

        return f"Mode changed to {mode}"


    # SYSTEM
    if cmd == "/ping":
        return "pong 🟢"


    if cmd == "/version":
        return "SolaraAI V2"


    return None
