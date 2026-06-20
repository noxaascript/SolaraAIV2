from core.user_store import get_key, set_key
from providers.groq import ask_groq

MODELS = {
    "1": "llama3-8b-8192",
    "2": "mixtral-8x7b",
    "3": "gemma2-9b-it"
}


def run_tool(user_input, user_id="default"):

    cmd = user_input.strip().lower()

    # SET API KEY PER USER
    if cmd.startswith("/setkey"):
        key = cmd.split(" ", 1)[1]
        set_key(user_id, key)
        return "API key saved for user"

    # SHOW KEY STATUS
    if cmd == "/key":
        return "Key exists" if get_key(user_id) else "No key"

    # MODEL LIST
    if cmd == "/model list":
        return "\n".join([f"{k}. {v}" for k, v in MODELS.items()])

    # MODEL SELECT (optional per request later)
    if cmd.startswith("/model"):
        return "Use /model list first"

    return None
