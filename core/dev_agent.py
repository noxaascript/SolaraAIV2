from core.tools import run_tool
from providers.smart_router import auto_chat


# =========================
# PLANNER
# =========================
def make_plan(prompt):

    return auto_chat(f"""
You are a planning AI.
Break this task into steps:

Task: {prompt}

Return simple numbered steps.
""")



# =========================
# TOOL EXECUTOR
# =========================
def execute_tool_step(step):

    s = step.lower()

    # WEB
    if "website" in s or "html" in s:
        return run_tool("web_create", "auto_site", step)

    # PROJECT
    if "project" in s or "app" in s:
        return run_tool("ws_create", "auto_project")

    # FETCH
    if "http" in s:
        return run_tool("fetch", step)

    return None


# =========================
# RUN PLAN
# =========================
def run_plan(plan_text):

    results = []

    steps = plan_text.split("\n")

    for step in steps:

        result = execute_tool_step(step)

        if result:
            results.append(result)

    return results


# =========================
# VERIFIER
# =========================
def verify(prompt, results):

    return auto_chat(f"""
User task: {prompt}

Execution results:
{results}

Check if task is complete.
If not, suggest improvement.
""")


# =========================
# MAIN AUTONOMOUS DEV AGENT
# =========================
def dev_autonomous(prompt, user_id="default"):

    # 1. PLAN
    plan = make_plan(prompt)

    # 2. EXECUTE
    results = run_plan(plan)

    # 3. VERIFY + FINAL AI RESPONSE
    final = verify(prompt, results)

    return final
