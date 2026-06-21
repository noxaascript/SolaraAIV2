from model_core.prompt import build_prompt
from model_core.memory import add_memory
from model_core.router import route_intent


def brain(user_input, user="default"):

    mode = route_intent(user_input)

    prompt = build_prompt(user_input)

    # SIMULASI AI (nanti bisa ganti Groq/Qwen/LLaMA)
    response = f"[{mode.upper()} MODE]\n" + prompt[:300]

    add_memory(user, user_input, response)

    return response
