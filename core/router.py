from core.commands import run_tool
from core.autonomous_agent import autonomous_agent


# =========================
# MAIN ROUTER ENTRY
# =========================
def route(user_input, user_id="default"):

    # =========================
    # COMMAND MODE
    # =========================
    if user_input.startswith("/"):
        result = run_tool(user_input, user_id)

        if result is not None:
            return result

        return "Unknown command. type /help"

    # =========================
    # AUTONOMOUS AI MODE 🤖
    # =========================
    try:
        return autonomous_agent(user_input, user_id)

    except Exception as e:
        return f"Router error: {str(e)}"
