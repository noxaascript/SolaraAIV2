from core.dev_agent import dev_autonomous


# =========================
# AUTONOMOUS AGENT CORE WRAPPER
# =========================
class AutonomousAgent:

    def __init__(self):
        self.mode = "dev_autonomous"
        self.last_task = None
        self.last_result = None

    # -------------------------
    # MAIN ENTRY
    # -------------------------
    def run(self, prompt, user_id="default"):

        self.last_task = prompt

        try:
            result = dev_autonomous(prompt, user_id)

            self.last_result = result

            return self.format_output(result)

        except Exception as e:
            return self.handle_error(e)

    # -------------------------
    # OUTPUT FORMATTER
    # -------------------------
    def format_output(self, result):

        if result is None:
            return "[AUTO] No result generated"

        return f"""🤖 AUTONOMOUS RESULT

{result}

━━━━━━━━━━━━━━━━━━
mode: {self.mode}
status: completed
"""

    # -------------------------
    # ERROR HANDLER
    # -------------------------
    def handle_error(self, error):

        return f"""❌ AUTONOMOUS ERROR

error: {str(error)}

system: {self.mode}
status: failed
"""


# =========================
# GLOBAL INSTANCE
# =========================
agent_instance = AutonomousAgent()


# =========================
# PUBLIC FUNCTION
# =========================
def autonomous_agent(prompt, user_id="default"):
    return agent_instance.run(prompt, user_id)
