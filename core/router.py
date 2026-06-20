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
        result = run_tool(user_input, user_id)

        # command valid
        if result is not None:
            return result

        return "Unknown command. type /help"

    # =========================
    # AI MODE (SELF-IMPROVING)
    # =========================
    try:
        return auto_chat(user_input, user_id)
    except Exception as e:
        return f"Router error: {str(e)}"
