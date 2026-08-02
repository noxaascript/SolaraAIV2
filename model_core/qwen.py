from model_core.config import QWEN_MODEL
from providers.hf import ask_hf


def call_qwen(prompt, mode="chat"):
    """Call Qwen model via providers.hf (local-first)."""
    try:
        return ask_hf(prompt, model=QWEN_MODEL)
    except Exception as e:
        return f"[QWEN_ERROR] {str(e)}"
