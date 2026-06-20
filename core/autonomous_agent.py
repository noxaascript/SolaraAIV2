from core.tools import run_tool
from providers.smart_router import auto_chat


# =========================
# TOOL DECISION ENGINE
# =========================
def decide_actions(prompt):

    p = prompt.lower()

    actions = []

    # WEB ACTION
    if "http" in p or "buka web" in p or "cek link" in p:
        actions.append(("fetch", extract_url(p)))

    # WEB GENERATION
    if "buat website" in p or "generate website" in p:
        actions.append(("web_create", "site", prompt))

    # WORKSPACE
    if "project" in p or "app" in p:
        actions.append(("ws_create", "auto_project"))

    return actions


def extract_url(text):
    for w in text.split():
        if "http" in w:
            return w
    return "https://example.com"


# =========================
# EXECUTOR
# =========================
def execute_actions(actions):

    results = []

    for action in actions:
        tool = action[0]
        args = action[1:]

        try:
            result = run_tool(tool, *args)
            results.append(result)
        except Exception as e:
            results.append(f"tool error: {str(e)}")

    return results


# =========================
# AUTONOMOUS AGENT CORE
# =========================
def autonomous_agent(prompt, user_id="default"):

    # 1. decide tools
    actions = decide_actions(prompt)

    # 2. kalau ada tool → eksekusi dulu
    if actions:
        tool_result = execute_actions(actions)

        # 3. gabung hasil tool + AI reasoning
        ai_prompt = f"""
User request: {prompt}

Tool results:
{tool_result}

Explain or continue task if needed.
"""

        return auto_chat(ai_prompt, user_id)

    # 4. kalau gak ada tool → pure AI
    return auto_chat(prompt, user_id)
