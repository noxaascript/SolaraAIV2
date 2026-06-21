def route_intent(text):

    text = text.lower()

    if any(k in text for k in ["code", "fix", "bug"]):
        return "code_mode"

    if any(k in text for k in ["explain", "why", "how"]):
        return "reason_mode"

    return "chat_mode"
