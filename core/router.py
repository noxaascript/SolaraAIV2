from core.commands import run_tool
from providers.smart_router import auto_chat


# =========================
# MAIN ROUTER
# =========================
def route(user_input, user_id="default"):

    # =========================
    # COMMAND MODE
    # =========================
    if user_input.startswith("/"):
        result = run_tool(user_input)

        # kalau command valid
        if result is not None:
            return result

        return "Unknown command. type /help"

    # =========================
    # AI MODE (AUTO SWITCH)
    # =========================
    try:
        return auto_chat(user_input)
    except Exception as e:
        return f"AI router error: {str(e)}"
