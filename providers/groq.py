from providers.hf import ask_hf


def ask_groq(prompt, model=None, api_key=None):
    hf_model = "Qwen/Qwen2.5-7B-Instruct"
    return ask_hf(prompt, model=hf_model, api_key=api_key)
