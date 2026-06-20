from core.memory import (
    normalize,
    auto_learn,
    build_memory_context,
    get_memory
)

from core.commands import run_tool
from core.personality import get_personality
from core.brain import choose_model

from core.tools import run_tool as run_plugin

from config import MODEL_ROLES, MODELS

from providers.groq import ask_groq
from providers.hf import ask_hf


def route(user_input):

    # =========================
    # NORMALIZE INPUT
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

        if result is not None:
            return result

        return "Unknown command"


    # =========================
    # TOOL SYSTEM (URL / BROWSER)
    # =========================
    if "http" in user_input:
        return run_plugin("browser", user_input)


    # =========================
    # MEMORY CONTEXT
    # =========================
    memory = build_memory_context()


    # =========================
    # PERSONALITY SYSTEM
    # =========================
    mode = get_memory("personality")

    if not mode:
        mode = "normal"

    personality = get_personality(mode)


    # =========================
    # BRAIN (AUTO MODEL SELECT)
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

Respond naturally, use context and personality.
"""


    # =========================
    # MODEL ROUTING
    # =========================
    if model["provider"] == "groq":
        return ask_groq(model["name"], prompt)

    if model["provider"] == "hf":
        return ask_hf(model["name"], prompt)


    return "Invalid AI provider"
