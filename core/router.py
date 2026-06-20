from core.memory import (
    auto_learn,
    normalize,
    build_memory_context
)

from core.commands import run_tool

from core.model_manager import get_model

from providers.groq import ask_groq
from providers.hf import ask_hf


def route(user_input):

    # =========================
    # NORMALIZE TEXT
    # =========================
    clean_input = normalize(user_input)


    # =========================
    # AUTO LEARN MEMORY
    # =========================
    learned = auto_learn(clean_input)

    if learned:
        return learned


    # =========================
    # COMMAND SYSTEM
    # =========================
    if clean_input.startswith("/"):
        result = run_tool(clean_input)

        if result is None:
            return "Unknown command ❌"

        return result


    # =========================
    # BUILD AI CONTEXT
    # =========================
    memory_context = build_memory_context()

    prompt = f"""
You are SolaraAI, a powerful AI assistant.

{memory_context}

User message:
{user_input}

Answer naturally.
"""


    # =========================
    # MODEL ROUTER
    # =========================
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


    return "Error: Invalid AI provider"
