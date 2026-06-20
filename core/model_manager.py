from config import MODELS, CURRENT_MODEL

current = CURRENT_MODEL


def get_model():
    return MODELS[current]["name"]


def get_model_info():
    return MODELS[current]


def set_model(key):
    global current

    if key in MODELS:
        current = key
        return f"model switched → {key} ({MODELS[key]['name']})"

    return "invalid model (use 1/2/3)"


def list_models():
    return MODELS
