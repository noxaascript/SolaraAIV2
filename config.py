GROQ_API_KEY = "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"

MODELS = {
    "1": {
        "name": "llama-3.1-8b-instant",
        "provider": "groq"
    },
    "2": {
        "name": "llama-3.3-70b-versatile",
        "provider": "groq"
    },
    "3": {
        "name": "qwen/qwen3-32b",
        "provider": "hf"
    }
}

MODEL_ROLES = {
    "fast": "1",
    "reasoning": "2",
    "coding": "3"
}
