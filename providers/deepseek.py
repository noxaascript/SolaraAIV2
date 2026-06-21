from providers.hf import ask_hf


def ask_deepseek(prompt, model="Qwen/Qwen2.5-7B-Instruct", api_key=None):
    return ask_hf(prompt, model=model, api_key=api_key)
