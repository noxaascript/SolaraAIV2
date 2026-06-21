# ==============================
# SOLARA AI V2 Router System
# ==============================

from providers.hf import ask_hf
from providers.groq import ask_groq


def router(prompt, model="auto"):
    """
    Solara AI Router
    Auto select model.
    """

    try:
        if model == "groq":
            return ask_groq(prompt)

        if model == "hf":
            return ask_hf(prompt)

        # Auto mode
        if len(prompt) > 150:
            return ask_hf(prompt)

        return ask_groq(prompt)

    except Exception as e:
        return f"⚠ Router Error: {e}"
