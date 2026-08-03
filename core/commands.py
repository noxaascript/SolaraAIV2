from core.hf_credentials import clear_user_key, has_user_key, set_user_key

MODELS = {
    "1": "Qwen/Qwen2.5-7B-Instruct",
    "2": "Qwen/Qwen2.5-Coder-32B-Instruct",
    "3": "moonshotai/Kimi-K2.6",
    "4": "moonshotai/Kimi-K2.5",
    "5": "meta-llama/Llama-3.3-70B-Instruct",
    "6": "mistralai/Mistral-7B-Instruct-v0.3",
    "7": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
}


def run_tool(user_input, user_id="default"):

    raw = user_input.strip()
    cmd = raw.lower()

    # API keys must never be accepted as normal chat text.
    if cmd == "/sethfkeyauto":
        return "Use the secure key prompt to connect your Hugging Face key."

    if cmd in {"/key", "/hfstatus"}:
        return "Hugging Face key is configured for this session." if has_user_key(user_id) else "No user Hugging Face key is configured."

    if cmd == "/clearhfkey":
        clear_user_key(user_id)
        return "User Hugging Face key cleared from this session."

    # MODEL LIST
    if cmd == "/model list":
        return "\n".join([f"{k}. {v}" for k, v in MODELS.items()])

    # MODEL SELECT (optional per request later)
    if cmd.startswith("/model"):
        return "Use /model list first"

    return None
