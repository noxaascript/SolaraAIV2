from core.commands import run_tool

# OPTIONAL: kalau kamu sudah punya model AI
try:
    from providers.groq import ask_groq
    from config import MODELS, MODEL_ROLES
except:
    ask_groq = None


def route(user_input):

    # =====================
    # COMMAND SYSTEM
    # =====================
    if user_input.startswith("/"):
        return run_tool(user_input)

    # =====================
    # AI RESPONSE (REAL)
    # =====================
    if ask_groq:
        prompt = f"""
You are SolaraAI.

User message:
{user_input}

Respond naturally and helpful.
"""

        try:
            return ask_groq("llama3-8b-8192", prompt)
        except:
            return "AI error (model call failed)"

    # =====================
    # FALLBACK
    # =====================
    return "No AI model connected"
