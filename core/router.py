from core.plugins import run_plugin
from core.tools import run_tool
from core.memory import auto_learn, get_memory, normalize
from providers.groq import ask_groq


def route(user_input):

    # 🧠 normalize dulu (slang fix)
    user_input = normalize(user_input)

    # 🧠 auto learn
    learned = auto_learn(user_input)
    if learned:
        return learned

    # 🔌 plugin system
    if user_input.startswith("@"):
        parts = user_input[1:].split(" ", 1)
        name = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        return run_plugin(name, text)

    # ⚙️ tools
    if user_input.startswith("/"):
        return run_tool(user_input)

    # 🤖 AI mode
    name = get_memory("name")

    context = ""
    if name:
        context = f"User name: {name}\n"

    return ask_groq(context + user_input)
