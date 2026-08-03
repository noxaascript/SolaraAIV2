from providers.hf import ask_hf
from model_core.config import GLM_MODEL


def ask_glm(prompt, model=None):
    """Simple GLM provider wrapper that prefers local transformers."""
    model = model or GLM_MODEL
    try:
        return ask_hf(prompt, model=model)
    except Exception as e:
        return f"[GLM_ERROR] {str(e)}"
