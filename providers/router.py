from providers.hf              import ask_hf
from config import PROVIDERS
from core.hf_credentials import get_user_key


def run_ai(provider, prompt, model=None, api_key=None, user_id="default"):
    cfg = PROVIDERS.get(provider)
    if cfg is None:
        available = ", ".join(PROVIDERS.keys())
        return f"Unknown provider: '{provider}'. Available: {available}"

    _model   = model   or cfg["model"]
    _api_key = api_key or get_user_key(user_id) or cfg.get("api_key", "")
    backend  = cfg.get("backend", "hf")

    result = ask_hf(prompt, model=_model, api_key=_api_key)
    unsupported = "not available through the selected Hugging Face provider" in str(result)
    if unsupported and _model != PROVIDERS["qwen"]["model"]:
        fallback = PROVIDERS["qwen"]["model"]
        fallback_result = ask_hf(prompt, model=fallback, api_key=_api_key)
        if not str(fallback_result).startswith("✖"):
            return (
                f"{fallback_result}\n\n"
                f"(The selected model was unavailable, so SolaraAI used {fallback}.)"
            )
    return result


def list_providers():
    return list(PROVIDERS.keys())
