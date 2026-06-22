import os

# ─────────────────────────────────────────────
#  Config — HuggingFace + OpenAI
#
#  Key loading order:
#    1. Environment variable (set by start.sh from .env)
#    2. Falls back to empty string (error shown at runtime)
#
#  Setup:
#    echo 'HF_API_KEY=hf_yourkey' > .env
#    bash start.sh
# ─────────────────────────────────────────────

HF_API_KEY = os.environ.get("HF_API_KEY", "")

PROVIDERS = {
    "qwen": {
        "label":    "Qwen 2.5 7B  (fast, smart)",
        "model":    "Qwen/Qwen2.5-7B-Instruct",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "qwen_72b": {
        "label":    "Qwen 2.5 72B  (powerful)",
        "model":    "Qwen/Qwen2.5-72B-Instruct",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "llama": {
        "label":    "LLaMA 3 8B",
        "model":    "meta-llama/Llama-3-8B-Instruct",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "llama_70b": {
        "label":    "LLaMA 3 70B  (powerful)",
        "model":    "meta-llama/Llama-3-70B-Instruct",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "mistral": {
        "label":    "Mistral 7B Instruct",
        "model":    "mistralai/Mistral-7B-Instruct-v0.3",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "gemma": {
        "label":    "Gemma 2 9B  (Google)",
        "model":    "google/gemma-2-9b-it",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "phi": {
        "label":    "Phi-3 Mini  (Microsoft, tiny + fast)",
        "model":    "microsoft/Phi-3-mini-4k-instruct",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "phi4": {
        "label":    "Phi-4  (Microsoft, powerful + fast)",
        "model":    "microsoft/phi-4",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "deepseek": {
        "label":    "DeepSeek-R1 7B  (reasoning, chain-of-thought)",
        "model":    "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "codellama": {
        "label":    "Code LLaMA 7B  (coding)",
        "model":    "codellama/CodeLlama-7b-Instruct-hf",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "kimi_code": {
        "label":    "Kimi K2  (Moonshot AI, coding)",
        "model":    "moonshotai/Kimi-K2-Instruct",
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
}

DEFAULT_PROVIDER = "qwen"
