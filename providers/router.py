from providers.groq import ask_groq
from providers.hf import ask_hf


def run_ai(provider, api_key, model, prompt):

    if provider == "groq":
        return ask_groq(api_key, model, prompt)

    if provider == "hf":
        return ask_hf(api_key, model, prompt)

    return "Unknown provider"
