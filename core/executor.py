from core.tools import run_tool
import time


def run_steps(plan_text, user_id):

    results = []

    steps = [s.strip() for s in plan_text.split("\n") if s.strip()]

    for step in steps:

        try:

            result = execute(step)

            results.append(result)

        except Exception as e:
            results.append(f"step error: {str(e)}")

        time.sleep(0.2)

    return results


def execute(step):

    s = step.lower()

    if "website" in s:
        return run_tool("web_create", "auto_site", step)

    if "project" in s:
        return run_tool("ws_create", "auto_project")

    if "http" in s:
        return run_tool("fetch", step)

    return step
