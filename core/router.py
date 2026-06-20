from core.brain_memory import learn_pattern, get_learned
from core.workspace import auto_app
from core.deploy import deploy_vercel

from core.memory import (
    normalize,
    auto_learn,
    build_memory_context,
    get_memory
)

from core.chat_memory import (
    add_chat,
    build_chat_context
)

from core.agent import agent_process

from core.commands import run_tool
from core.personality import get_personality
from core.brain import choose_model

from config import MODEL_ROLES, MODELS

from providers.groq import ask_groq
from providers.hf import ask_hf


def route(user_input):

    clean_input = normalize(user_input)


    # =========================
    # AGENT MODE (AUTO TOOL)
    # =========================
    agent_result = agent_process(user_input)

    if agent_result:
        return agent_result


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
        return run_tool(clean_input)


    # =========================
    # CONTEXT BUILDING
    # =========================
    memory = build_memory_context()
    chat = build_chat_context()


    # =========================
    # PERSONALITY
    # =========================
    mode = get_memory("personality") or "normal"
    personality = get_personality(mode)


    # =========================
    # BRAIN MODEL SELECT
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

Conversation:
{chat}

User message:
{user_input}

Respond naturally.
"""


    # =========================
    # AI CALL
    # =========================
    if model["provider"] == "groq":
        response = ask_groq(model["name"], prompt)

    elif model["provider"] == "hf":
        response = ask_hf(model["name"], prompt)

    else:
        response = "Invalid provider"


    # =========================
    # SAVE CHAT MEMORY
    # =========================
    add_chat(user_input, response)

    return response
