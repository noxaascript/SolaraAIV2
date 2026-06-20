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

from core.personality import get_modes

from core.workspace import (
    create_workspace,
    list_workspaces,
    add_file,
    read_workspace
)


def run_tool(user_input):
    cmd = user_input.strip().lower()

    # =========================
    # HELP
    # =========================
    if cmd == "/help":
        return (
            "Commands:\n"
            "/memory\n"
            "/forget <key>\n"
            "/model\n"
            "/models\n"
            "/setmodel <id>\n"
            "/mode\n"
            "/modes\n"
            "/setmode <name>\n"
            "/workspace create <name>\n"
            "/workspace list\n"
            "/workspace open <name>\n"
            "/workspace addfile <ws> <file> <content>\n"
            "/ping\n"
            "/version"
        )

    # =========================
    # MEMORY
    # =========================
    if cmd == "/memory":
        data = get_all_memory()

        if not data:
            return "Memory is empty"

        result = "Memory:\n"
        for k, v in data:
            result += f"- {k}: {v}\n"

        return result


    if cmd.startswith("/forget"):
        parts = cmd.split()

        if len(parts) < 2:
            return "Usage: /forget <key>"

        delete_memory(parts[1])
        return f"Forgot {parts[1]}"


    # =========================
    # MODEL
    # =========================
    if cmd == "/model":
        m = get_model()
        return f"{m['name']} ({m['provider']})"


    if cmd == "/models":
        result = ""

        for k, v in list_models().items():
            result += f"{k}. {v['name']} ({v['provider']})\n"

        return result


    if cmd.startswith("/setmodel"):
        parts = cmd.split()

        if len(parts) < 2:
            return "Usage: /setmodel <id>"

        return set_model(parts[1])


    # =========================
    # PERSONALITY
    # =========================
    if cmd == "/mode":
        mode = get_memory("personality")

        if not mode:
            mode = "normal"

        return mode


    if cmd == "/modes":
        result = ""

        for m in get_modes():
            result += f"- {m}\n"

        return result


    if cmd.startswith("/setmode"):
        parts = cmd.split()

        if len(parts) < 2:
            return "Usage: /setmode <mode>"

        mode = parts[1]

        if mode not in get_modes():
            return "Invalid mode"

        set_memory("personality", mode)

        return f"Mode set to {mode}"


    # =========================
    # WORKSPACE SYSTEM
    # =========================
    if cmd.startswith("/workspace create"):
        parts = cmd.split()

        if len(parts) < 3:
            return "Usage: /workspace create <name>"

        return create_workspace(parts[2])


    if cmd == "/workspace list":
        ws = list_workspaces()

        if not ws:
            return "No workspaces"

        return "\n".join(ws)


    if cmd.startswith("/workspace open"):
        parts = cmd.split()

        if len(parts) < 3:
            return "Usage: /workspace open <name>"

        return str(read_workspace(parts[2]))


    if cmd.startswith("/workspace addfile"):
        parts = cmd.split()

        if len(parts) < 5:
            return "Usage: /workspace addfile <ws> <file> <content>"

        ws = parts[2]
        file_name = parts[3]
        content = " ".join(parts[4:])

        return add_file(ws, file_name, content)


    # =========================
    # SYSTEM
    # =========================
    if cmd == "/ping":
        return "pong 🟢"


    if cmd == "/version":
        return "SolaraAI V2"


    return None
