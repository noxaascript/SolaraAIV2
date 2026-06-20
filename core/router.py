from core.commands import run_tool
from core.autonomous_agent import autonomous_agent


# =========================
# ROUTER ENGINE CLASS
# =========================
class RouterEngine:

    def __init__(self):
        self.total_requests = 0
        self.command_count = 0
        self.ai_count = 0

    # -------------------------
    # MAIN ROUTE FUNCTION
    # -------------------------
    def route(self, user_input, user_id="default"):

        self.total_requests += 1

        if not isinstance(user_input, str):
            return self.error("Invalid input type")

        user_input = user_input.strip()

        # =========================
        # COMMAND MODE
        # =========================
        if user_input.startswith("/"):
            self.command_count += 1

            return self.handle_command(user_input, user_id)

        # =========================
        # AI MODE
        # =========================
        self.ai_count += 1

        return self.handle_ai(user_input, user_id)

    # -------------------------
    # COMMAND HANDLER
    # -------------------------
    def handle_command(self, user_input, user_id):

        try:
            result = run_tool(user_input, user_id)

            if result is None:
                return self.error("Unknown command. type /help")

            return self.wrap_command(result)

        except Exception as e:
            return self.error(f"command crash: {str(e)}")

    # -------------------------
    # AI HANDLER
    # -------------------------
    def handle_ai(self, user_input, user_id):

        try:
            result = autonomous_agent(user_input, user_id)

            return self.wrap_ai(result)

        except Exception as e:
            return self.error(f"ai crash: {str(e)}")

    # -------------------------
    # FORMATTING
    # -------------------------
    def wrap_command(self, result):

        return f"""⚙️ COMMAND RESULT

{result}

━━━━━━━━━━━━━━━━━━
type: command
"""

    def wrap_ai(self, result):

        return f"""🤖 AI RESPONSE

{result}

━━━━━━━━━━━━━━━━━━
type: autonomous
"""

    def error(self, msg):

        return f"""❌ ROUTER ERROR

{msg}

━━━━━━━━━━━━━━━━━━
system: RouterEngine
"""


# =========================
# GLOBAL ROUTER INSTANCE
# =========================
router = RouterEngine()


# =========================
# PUBLIC ENTRY FUNCTION
# =========================
def route(user_input, user_id="default"):
    return router.route(user_input, user_id)
