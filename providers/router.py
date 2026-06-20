from providers.groq import ask_groq
from providers.llama import ask_llama
from providers.qwen import ask_qwen


def run_ai(provider, api_key, model, prompt):

    if provider == "groq":
        return ask_groq(api_key, model, prompt)

    if provider == "llama":
        return ask_llama(api_key, model, prompt)

    if provider == "qwen":
        return ask_qwen(api_key, model, prompt)

    return "Unknown provider"
