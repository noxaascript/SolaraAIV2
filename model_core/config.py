import os

# =========================
# AI MODEL CONFIG
# =========================

# aktif model utama
ACTIVE_MODEL = "qwen"   # qwen | groq | llama

# API KEYS (boleh isi langsung atau dari env)
QWEN_API_KEY = os.getenv("QWEN_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY", "")

# =========================
# BRAIN SETTINGS
# =========================

TEMPERATURE = 0.7
MAX_MEMORY = 200
MAX_CONTEXT = 5

# =========================
# ROUTING MODE
# =========================

MODES = {
    "chat": "general conversation",
    "coder": "coding and debugging",
    "reason": "logic and explanation",
    "planner": "planning and system design"
}

# =========================
# MODEL ENDPOINTS
# =========================

QWEN_MODEL = "qwen/qwen-2.5-72b-instruct"
GROQ_MODEL = "llama-3.1-70b-versatile"
LLAMA_MODEL = "llama-3.1-8b-instruct"

# =========================
# DEBUG MODE
# =========================

DEBUG = True
