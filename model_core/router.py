import re


def route_intent(text: str) -> str:
    """Classify user input into one of the intent modes used by the model layer.

    Returns one of:
      - "coder_brain"   : for coding / debugging / error & stack-trace related queries
      - "reason_brain"  : for analysis / explanation / question answering
      - "planner_brain" : for planning / project / design / step-by-step instructions
      - "chat_brain"    : default for general chit-chat
    """

    if not text or not text.strip():
        return "chat_brain"

    t = text.lower()

    # ========== CODER / DEBUGGING ===========
    # Look for explicit code tokens, file extensions, or error/traceback hints.
    code_tokens = [r"\bdef\b", r"\bclass\b", r"\bimport\b", r"\bfrom\b"]
    code_patterns = [r"\.py\b", r"stack trace", r"traceback", r"syntax error", r"exception", r"compile error"]
    code_keywords = ["bug", "fix", "error", "debug", "debugging", "trace", "traceback", "exception", "stacktrace"]

    if any(re.search(p, t) for p in code_tokens) or any(p in t for p in code_patterns) or any(k in t for k in code_keywords):
        return "coder_brain"

    # ========== REASONING / Q&A ============
    # Questions are often indicated by a "?" or question words.
    if "?" in text or any(k in t for k in ["why", "how", "explain", "what", "analyze", "reason", "understand"]):
        return "reason_brain"

    # ========== PLANNING / DESIGN ============
    if any(k in t for k in ["plan", "build", "create", "project", "app", "steps", "design", "architecture", "roadmap"]):
        return "planner_brain"

    # ========== DEFAULT CHAT ==============
    return "chat_brain"
