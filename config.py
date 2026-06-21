import os

GROQ_API_KEY = "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"
HF_API_KEY = "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"

# ─────────────────────────────────────────────
#  Only HuggingFace is required.
#  The key is pre-loaded by start.sh automatically.
# ─────────────────────────────────────────────

HF_API_KEY = os.environ.get("HF_API_KEY", "")

PROVIDERS = {
    "qwen": {
        "label": "Qwen 2.5 7B  (fast, smart)",
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "api_key": HF_API_KEY,
    },
    "qwen_72b": {
        "label": "Qwen 2.5 72B (powerful)",
        "model": "Qwen/Qwen2.5-72B-Instruct",
        "api_key": HF_API_KEY,
    },
    "llama": {
        "label": "LLaMA 3 8B",
        "model": "meta-llama/Llama-3-8B-Instruct",
        "api_key": HF_API_KEY,
    },
    "llama_70b": {
        "label": "LLaMA 3 70B (powerful)",
        "model": "meta-llama/Llama-3-70B-Instruct",
        "api_key": HF_API_KEY,
    },
    "mistral": {
        "label": "Mistral 7B Instruct",
        "model": "mistralai/Mistral-7B-Instruct-v0.3",
        "api_key": HF_API_KEY,
    },
    "gemma": {
        "label": "Gemma 2 9B (Google)",
        "model": "google/gemma-2-9b-it",
        "api_key": HF_API_KEY,
    },
    "phi": {
        "label": "Phi-3 Mini (Microsoft, tiny+fast)",
        "model": "microsoft/Phi-3-mini-4k-instruct",
        "api_key": HF_API_KEY,
    },
    "codellama": {
        "label": "Code LLaMA 7B (coding)",
        "model": "codellama/CodeLlama-7b-Instruct-hf",
        "api_key": HF_API_KEY,
    },
}

DEFAULT_PROVIDER = "qwen"
