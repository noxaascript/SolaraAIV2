from config import MODELS, CURRENT_MODEL

current = CURRENT_MODEL


def get_model():
    return MODELS[current]


def set_model(key):
    global current

    if key in MODELS:
        current = key
        m = MODELS[key]
        return f"model switched → {key} ({m['provider']}:{m['name']})"

    return "invalid model id"


def list_models():
    return MODELS
