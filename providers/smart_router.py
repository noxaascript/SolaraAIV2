import time
from providers.groq import ask_groq
from providers.qwen import ask_qwen
from providers.llama import ask_llama
from core.model_memory import get_scores, update_score


MODELS = {
    "groq": lambda prompt: ask_groq("llama3-8b-8192", prompt),
    "qwen": lambda prompt: ask_qwen("Qwen/Qwen2.5-7B-Instruct", prompt),
    "llama": lambda prompt: ask_llama("meta-llama/Llama-3-8B-Instruct", prompt)
}


# =========================
# PICK BEST MODEL (LEARNING)
# =========================
def pick_model(user_id, prompt):

    scores = get_scores(user_id)

    # default score kalau belum ada data
    def score(m):
        return scores.get(m, 1)

    # pilih skor tertinggi
    best = max(MODELS.keys(), key=score)

    return best


# =========================
# AUTO CHAT + LEARNING
# =========================
def auto_chat(prompt, user_id="default"):

    model = pick_model(user_id, prompt)

    start = time.time()

    try:
        result = MODELS[model](prompt)

        latency = time.time() - start

        # =========================
        # SCORE SYSTEM
        # =========================
        score = 1.0

        # cepat = bagus
        if latency < 2:
            score += 1.0
        elif latency > 6:
            score -= 0.5

        # error detection
        if "error" in str(result).lower():
            score -= 1.5

        update_score(user_id, model, score)

        return result

    except Exception as e:
        update_score(user_id, model, -2)
        return f"AI error: {str(e)}"
