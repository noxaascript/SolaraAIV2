from core.smart_router import detect_task
from core.tools import run_tool


AGENT_ON = True


def agent_process(user_input):
    if not AGENT_ON:
        return None

    task = detect_task(user_input)

    if task == "browser":
        return run_tool("browser", user_input)

    if task == "workspace_ai":
        # fallback simple trigger
        return "AGENT: use /workspace ai command"

    return None


def toggle_agent(state: bool):
    global AGENT_ON
    AGENT_ON = state
