from core.tools import run_tool


def run_steps(plan, user_id):

    results = []

    steps = [s.strip() for s in plan.split("\n") if s.strip()]

    for step in steps:

        results.append(execute(step))

    return results


def execute(step):

    s = step.lower()

    # =========================
    # BROWSER ACTIONS 🌐
    # =========================
    if "visit" in s or "open url" in s:
        url = extract_url(step)
        return run_tool("browser_visit", url)

    if "summarize" in s or "read website" in s:
        url = extract_url(step)
        return run_tool("browser_summary", url)

    # =========================
    # WEB
    # =========================
    if "http" in s:
        return run_tool("fetch", extract_url(step))

    # =========================
    # DEFAULT
    # =========================
    return step


def extract_url(text):

    for w in text.split():

        if "http" in w:
            return w

    return "https://example.com"
