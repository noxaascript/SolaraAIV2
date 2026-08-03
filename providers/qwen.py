from providers.hf import ask_hf
from config import PROVIDERS


def ask_qwen(prompt, model=None, api_key=None):
    return ask_hf(prompt, model=model or PROVIDERS["qwen"]["model"], api_key=api_key)
