def route_intent(text):

    t = text.lower()

    # =========================
    # CODER BRAIN
    # =========================
    if any(k in t for k in [
        "code", "bug", "fix", "error", "python", "function"
    ]):
        return "coder_brain"

    # =========================
    # REASONING BRAIN
    # =========================
    if any(k in t for k in [
        "why", "how", "explain", "what", "analyze"
    ]):
        return "reason_brain"

    # =========================
    # PLANNER BRAIN
    # =========================
    if any(k in t for k in [
        "plan", "build", "create", "project", "app"
    ]):
        return "planner_brain"

    # =========================
    # DEFAULT CHAT
    # =========================
    return "chat_brain"
