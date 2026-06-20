from providers.groq import ask_groq
from providers.qwen import ask_qwen
from providers.llama import ask_llama
from config import GROQ_API_KEY, HF_API_KEY


# =========================
# SIMPLE INTENT CLASSIFIER
# =========================
def pick_model(prompt):

    p = prompt.lower()

    # fast & general Q&A → Groq
    if len(p) < 200:
        return "groq"

    # coding / reasoning → LLaMA
    if "code" in p or "python" in p or "bug" in p:
        return "llama"

    # heavy reasoning / long text → Qwen
    if len(p) > 300:
        return "qwen"

    return "groq"


# =========================
# MAIN AUTO ROUTER
# =========================
def auto_chat(prompt):

    provider = pick_model(prompt)

    # ================= GROQ =================
    if provider == "groq":
        model = "llama3-8b-8192"
        return ask_groq(model, prompt)

    # ================= LLAMA =================
    if provider == "llama":
        model = "meta-llama/Llama-3-8B-Instruct"
        return ask_llama(model, prompt)

    # ================= QWEN =================
    if provider == "qwen":
        model = "Qwen/Qwen2.5-7B-Instruct"
        return ask_qwen(model, prompt)

    return "No provider selected"
