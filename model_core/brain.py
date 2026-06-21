from model_core.prompt import build_prompt
from model_core.memory import add_memory, improve_memory
from model_core.router import route_intent
from model_core.qwen import call_qwen


def brain(user_input, user="default"):

    mode = route_intent(user_input)

    prompt = build_prompt(user_input)

    # 🔥 MEMORY SELF IMPROVE
    improve_memory(user_input)

    # 🔥 CALL QWEN
    response = call_qwen(prompt, mode)

    add_memory(user, user_input, response)

    return response
