from core.memory import (
    normalize,
    auto_learn,
    build_memory_context,
    get_memory
)

from core.commands import run_tool
from core.personality import get_personality
from core.brain import choose_model

from config import MODEL_ROLES, MODELS

from providers.groq import ask_groq
from providers.hf import ask_hf


def route(user_input):

    clean_input = normalize(user_input)

    # =========================
    # MEMORY LEARN
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
            return "Unknown command"
        return result

    # =========================
    # MEMORY CONTEXT
    # =========================
    memory = build_memory_context()

    # =========================
    # PERSONALITY
    # =========================
    mode = get_memory("personality")
    if not mode:
        mode = "normal"

    personality = get_personality(mode)

    # =========================
    # BRAIN MODEL SELECTOR
    # =========================
    role = choose_model(user_input)

    model_id = MODEL_ROLES.get(role, "1")
    model = MODELS[model_id]

    # =========================
    # FINAL PROMPT
    # =========================
    prompt = f"""
{personality}

User profile:
{memory}

User message:
{user_input}

Respond naturally and helpfully.
"""

    # =========================
    # PROVIDER ROUTE
    # =========================
    if model["provider"] == "groq":
        return ask_groq(model["name"], prompt)

    if model["provider"] == "hf":
        return ask_hf(model["name"], prompt)

    return "Invalid provider"
