import time
from providers.hf      import ask_hf
from core.model_memory import get_scores, update_score
from config            import PROVIDERS


def _call(provider_key, prompt):
    cfg = PROVIDERS[provider_key]
    return ask_hf(prompt, model=cfg["model"], api_key=cfg["api_key"])


def pick_model(user_id):
    scores = get_scores(user_id)
    keys   = list(PROVIDERS.keys())

    def score(m):
        return scores.get(m, 1.0)

    return max(keys, key=score)


def auto_chat(prompt, user_id="default"):
    model = pick_model(user_id)
    start = time.time()

    try:
        result  = _call(model, prompt)
        latency = time.time() - start

        score = 1.0
        if latency < 3:
            score += 1.0
        elif latency > 10:
            score -= 0.5
        if "error" in str(result).lower():
            score -= 1.5

        update_score(user_id, model, score)
        return result, model

    except Exception as e:
        update_score(user_id, model, -2)
        return f"AI error: {str(e)}", model
