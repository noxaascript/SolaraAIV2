from config import PROVIDERS, DEFAULT_PROVIDER

def ask_ai(provider, prompt):
    config = PROVIDERS.get(provider, PROVIDERS[DEFAULT_PROVIDER])

    model = config["model"]
    api_key = config["api_key"]

    print(f"[DEBUG] provider={provider}")
    print(f"[DEBUG] model={model}")

    if provider == "groq":
        return groq_request(model, api_key, prompt)

    if provider == "hf_qwen":
        return hf_request(model, api_key, prompt)

    if provider == "hf_kimi":
        return hf_request(model, api_key, prompt)

    return "[ERROR] provider not found"


# ===== GROQ =====
def groq_request(model, api_key, prompt):
    return f"[GROQ:{model}] {prompt}"


# ===== HF (QWEN + KIMI) =====
def hf_request(model, api_key, prompt):
    return f"[HF:{model}] {prompt}"
