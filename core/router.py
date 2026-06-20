from core.plugins import run_plugin
from core.tools import run_tool
from core.memory import auto_learn, get_memory, normalize

from core.model_manager import get_model
from providers.groq import ask_groq
from providers.hf import ask_hf


def route(user_input):

    user_input = normalize(user_input)

    # 🧠 memory learn
    learned = auto_learn(user_input)
    if learned:
        return learned

    # 🔌 plugin
    if user_input.startswith("@"):
        parts = user_input[1:].split(" ", 1)
        name = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        return run_plugin(name, text)

    # ⚙️ tools
    if user_input.startswith("/"):
        return run_tool(user_input)

    # 🤖 AI CORE
    model = get_model()

    name = get_memory("name")

    context = ""
    if name:
        context += f"User name: {name}\n"

    prompt = context + user_input

    # 🔥 HYBRID ROUTING
    if model["provider"] == "groq":
        return ask_groq(model["name"], prompt)

    if model["provider"] == "hf":
        return ask_hf(model["name"], prompt)

    return "invalid provider"
