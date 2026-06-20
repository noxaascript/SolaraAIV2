from core.commands import run_tool, MODELS, get_selected_model
from core.memory import get_memory
from providers.groq import ask_groq


def route(user_input):

    # COMMAND MODE
    if user_input.startswith("/"):
        return run_tool(user_input)

    # AI MODE
    mid = get_selected_model()
    model = MODELS[mid]

    prompt = f"""
You are SolaraAI.
User: {user_input}
Answer clearly and naturally.
"""

    return ask_groq(model, prompt)
