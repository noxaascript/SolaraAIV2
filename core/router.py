from core.commands import run_tool, MODELS
from core.user_store import get_key
from providers.groq import ask_groq


def route(user_input, user_id="default", model_id="1"):

    # COMMAND MODE
    if user_input.startswith("/"):
        return run_tool(user_input, user_id)

    api_key = get_key(user_id)

    if not api_key:
        return "User has no API key. Use /setkey <key>"

    model = MODELS.get(model_id, MODELS["1"])

    prompt = f"""
User: {user_input}
Answer naturally.
"""

    return ask_groq(api_key, model, prompt)
