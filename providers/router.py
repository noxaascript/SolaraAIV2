from providers.hf              import ask_hf
from providers.openai_provider import ask_openai
from config import PROVIDERS


def run_ai(provider, prompt, model=None, api_key=None):
    cfg = PROVIDERS.get(provider)
    if cfg is None:
        available = ", ".join(PROVIDERS.keys())
        return f"Unknown provider: '{provider}'. Available: {available}"

    _model   = model   or cfg["model"]
    _api_key = api_key or cfg.get("api_key", "")
    backend  = cfg.get("backend", "hf")

    if backend == "openai":
        return ask_openai(prompt, model=_model, api_key=_api_key)

    return ask_hf(prompt, model=_model, api_key=_api_key)


def list_providers():
    return list(PROVIDERS.keys())
