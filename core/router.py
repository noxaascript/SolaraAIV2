from core.memory import (
    normalize,
    auto_learn,
    build_memory_context,
    get_memory
)

from core.commands import run_tool
from core.personality import get_personality

from core.model_manager import get_model

from providers.groq import ask_groq
from providers.hf import ask_hf


def route(user_input):

    clean_input = normalize(user_input)


    # AUTO MEMORY
    learned = auto_learn(clean_input)

    if learned:
        return learned


    # COMMAND
    if clean_input.startswith("/"):
        result = run_tool(clean_input)

        if result is None:
            return "Unknown command"

        return result


    # MEMORY CONTEXT
    memory = build_memory_context()


    # PERSONALITY
    mode = get_memory("personality")

    if not mode:
        mode = "normal"

    personality = get_personality(mode)


    # FINAL PROMPT
    prompt = f"""
{personality}

User profile:
{memory}

User message:
{user_input}

Answer based on your personality mode.
"""


    # MODEL ROUTER
    model = get_model()


    if model["provider"] == "groq":
        return ask_groq(
            model["name"],
            prompt
        )


    if model["provider"] == "hf":
        return ask_hf(
            model["name"],
            prompt
        )


    return "Invalid AI provider"
