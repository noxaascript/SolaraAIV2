from config import MODELS

current_model = "groq"

def get_model():
    return current_model

def set_model(name):
    global current_model
    if name in MODELS:
        current_model = name
        return f"Switched to {name}"
    return "Invalid model"

def list_models():
    return MODELS
