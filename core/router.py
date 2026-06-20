from core.commands import run_tool
from core.agent_os import dev_os_agent


# =========================
# AI DEV OS ROUTER
# =========================
def route(user_input, user_id="default"):

    # safety check
    if not isinstance(user_input, str):
        return "Invalid input"

    user_input = user_input.strip()

    # =========================
    # COMMAND MODE
    # =========================
    if user_input.startswith("/"):

        try:
            result = run_tool(user_input, user_id)

            if result is None:
                return "Unknown command. type /help"

            return f"""⚙️ COMMAND EXECUTED

{result}
"""

        except Exception as e:
            return f"COMMAND ERROR: {str(e)}"

    # =========================
    # AI DEV OS MODE 🤖
    # =========================
    try:
        result = dev_os_agent(user_input, user_id)

        return f"""🤖 AI DEV OS RESPONSE

{result}
"""

    except Exception as e:
        return f"ROUTER ERROR: {str(e)}"
