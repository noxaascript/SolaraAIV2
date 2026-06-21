GROQ_API_KEY = "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"
HF_API_KEY = "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"

# PROVIDER + MODEL SETUP
PROVIDERS = {
    "groq": {
        "model": "llama3-8b-8192",
        "api_key": GROQ_API_KEY
    },
    "hf_qwen": {
        "model": "Qwen/Qwen3.6-27B",
        "api_key": HF_API_KEY
    },
    "hf_kimi": {
        "model": "moonshotai/Kimi-K2.7-Code",
        "api_key": HF_API_KEY
    }
}

DEFAULT_PROVIDER = "groq"
