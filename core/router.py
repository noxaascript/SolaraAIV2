from core.model_manager import get_model
from providers.groq import ask_groq

def get_response(prompt):
    model = get_model()

    # primary model
    if model == "groq":
        res = ask_groq(prompt)

        # fallback kalau error dari API
        if str(res).startswith("Groq Error") or str(res).startswith("Request Error"):
            return ask_groq(prompt + " (retry safe mode)")

        return res

    return "Model not implemented"
