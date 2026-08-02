# core/router.py
"""
Main router for all user input. Uses smart_router.auto_chat when available,
otherwise falls back to providers.hf (local transformers first).
"""


def help_text():
    return """
Available commands:
- /help  -> show this menu
- /exit  -> close app
- any text -> AI chat
"""


def handle_input(user_input: str):
    """
    Main router for user input. Returns plain strings or the sentinel "__EXIT__".
    """
    if not user_input:
        return "No input detected"

    text = user_input.strip()
    tl = text.lower()

    # basic commands
    if tl in ["exit", "quit", "/exit"]:
        return "__EXIT__"

    if tl in ["help", "/help"]:
        return help_text()

    # Try smart router first (auto model selection)
    try:
        from providers.smart_router import auto_chat
        try:
            maybe = auto_chat(text)
            # auto_chat commonly returns (result, model)
            if isinstance(maybe, tuple) and len(maybe) >= 1:
                result = maybe[0]
            else:
                result = maybe
            return str(result)
        except Exception:
            # fallback to direct provider below
            pass
    except Exception:
        pass

    # fallback: use configured HF provider which prefers local transformers
    try:
        from config import DEFAULT_PROVIDER, PROVIDERS
        provider_key = DEFAULT_PROVIDER if 'DEFAULT_PROVIDER' in globals() else 'hf_qwen'
        cfg = PROVIDERS.get(provider_key, {}) if 'PROVIDERS' in globals() else {}
        model = cfg.get("model") if isinstance(cfg, dict) else None

        from providers.hf import ask_hf
        response = ask_hf(text, model=model)
        return str(response)
    except Exception as e:
        return f"Router Error: {str(e)}"
