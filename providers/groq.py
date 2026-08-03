from providers.hf import ask_hf
from config import PROVIDERS


def ask_groq(prompt, model=None, api_key=None):
    hf_model = model or PROVIDERS["qwen"]["model"]
    return ask_hf(prompt, model=hf_model, api_key=api_key)
