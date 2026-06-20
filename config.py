API_KEYS = {
    "groq": "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",
    "hf": "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"
}

# =========================
# MODEL REGISTRY (HYBRID)
# =========================
MODELS = {
    "1": {
        "provider": "groq",
        "name": "llama-3.3-70b-versatile",
        "desc": "Best quality (Groq)"
    },
    "2": {
        "provider": "groq",
        "name": "llama-3.1-8b-instant",
        "desc": "Fast response (Groq)"
    },
    "3": {
        "provider": "groq",
        "name": "mixtral-8x7b-32768",
        "desc": "Long context (Groq)"
    },
    "4": {
        "provider": "hf",
        "name": "meta-llama/Llama-3-8b-instruct",
        "desc": "HF fallback model"
    },
    "5": {
        "provider": "hf",
        "name": "mistralai/Mistral-7B-Instruct-v0.3",
        "desc": "HF creative model"
    }
}

CURRENT_MODEL = "1"
