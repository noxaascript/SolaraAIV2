from config import MODELS

current_model = "1"


def get_model():
    return MODELS[current_model]


def list_models():
    return MODELS


def set_model(model_id):
    global current_model

    if model_id in MODELS:
        current_model = model_id
        m = MODELS[model_id]
        return f"model switched → {model_id} ({m['name']})"

    return "invalid model id (use 1-3)"
