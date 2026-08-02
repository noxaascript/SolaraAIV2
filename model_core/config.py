import os

# Prefer reading API keys and model ids from environment variables.
HF_API_KEY = os.environ.get("HF_API_KEY", None)
HF_FORCE_REMOTE = os.environ.get("HF_FORCE_REMOTE", "0").lower() in ("1", "true", "yes")
HF_USE_TRANSFORMERS = os.environ.get("HF_USE_TRANSFORMERS", "1").lower() in ("1", "true", "yes")

# Default model IDs (change via env vars if needed)
QWEN_MODEL = os.environ.get("QWEN_MODEL", "Qwen/Qwen2.5-7B-Instruct")
KIMI_MODEL = os.environ.get("KIMI_MODEL", "moonshotai/Kimi-K2.7-Code")
GLM_MODEL = os.environ.get("GLM_MODEL", "THUDM/chatglm-6b")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B")

# Active model
ACTIVE_MODEL = os.environ.get("ACTIVE_MODEL", "kimi")
