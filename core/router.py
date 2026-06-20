from core.commands import run_tool

# OPTIONAL MODEL IMPORT (aman kalau belum ada provider)
try:
    from providers.groq import ask_groq
except:
    ask_groq = None


def route(user_input):

    # =====================
    # COMMAND SYSTEM
    # =====================
    if user_input.startswith("/"):
        return run_tool(user_input)

    # =====================
    # AI BRAIN SYSTEM
    # =====================
    if ask_groq:
        try:
            prompt = f"""You are SolaraAI, a helpful assistant.

User: {user_input}
Answer clearly and naturally.
"""
            return ask_groq("llama3-8b-8192", prompt)
        except Exception as e:
            return f"AI error: {str(e)}"

    # =====================
    # FALLBACK (NO MODEL)
    # =====================
    return "AI belum connect ke model (cek providers/groq.py)"
