from model_core.prompt import build_prompt
from model_core.memory import add_memory, get_memory
from model_core.router import route_intent
from model_core.llm import call_llm


def brain(user_input, user="default"):

    mode = route_intent(user_input)

    prompt = build_prompt(user_input)

    response = call_llm(prompt, mode)

    add_memory(user, user_input, response)

    return response
