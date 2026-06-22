from providers.hf import ask_hf


def ask_llama(prompt, model="meta-llama/Llama-3-8B-Instruct", api_key=None):
    return ask_hf(prompt, model=model, api_key=api_key)
