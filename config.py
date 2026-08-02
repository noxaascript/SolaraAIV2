import os

HF_API_KEY = os.environ.get("HF_API_KEY", "")

PROVIDERS = {
    "qwen": {
        "label":    "Qwen 2.5 7B  (fast, smart)",
        "model":    os.environ.get("QWEN_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "qwen_72b": {
        "label":    "Qwen 2.5 72B  (powerful)",
        "model":    os.environ.get("QWEN_72B_MODEL", "Qwen/Qwen2.5-72B-Instruct"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "llama": {
        "label":    "LLaMA 3 8B",
        "model":    os.environ.get("LLAMA_MODEL", "meta-llama/Llama-3-8B-Instruct"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "llama_70b": {
        "label":    "LLaMA 3 70B  (powerful)",
        "model":    os.environ.get("LLAMA_70B_MODEL", "meta-llama/Llama-3-70B-Instruct"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "mistral": {
        "label":    "Mistral 7B Instruct",
        "model":    os.environ.get("MISTRAL_MODEL", "mistralai/Mistral-7B-Instruct-v0.3"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "gemma": {
        "label":    "Gemma 2 9B  (Google)",
        "model":    os.environ.get("GEMMA_MODEL", "google/gemma-2-9b-it"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "phi": {
        "label":    "Phi-3 Mini  (Microsoft, tiny + fast)",
        "model":    os.environ.get("PHI_MINI_MODEL", "microsoft/Phi-3-mini-4k-instruct"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "phi4": {
        "label":    "Phi-4  (Microsoft, powerful + fast)",
        "model":    os.environ.get("PHI4_MODEL", "microsoft/phi-4"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "deepseek": {
        "label":    "DeepSeek-R1 7B  (reasoning, chain-of-thought)",
        "model":    os.environ.get("DEEPSEEK_MODEL", "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "codellama": {
        "label":    "Code LLaMA 7B  (coding)",
        "model":    os.environ.get("CODELLAMA_MODEL", "codellama/CodeLlama-7b-Instruct-hf"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
    "kimi_code": {
        "label":    "Kimi K2  (Moonshot AI, coding)",
        "model":    os.environ.get("KIMI_MODEL", "moonshotai/Kimi-K2-Instruct"),
        "api_key":  HF_API_KEY,
        "backend":  "hf",
    },
}
