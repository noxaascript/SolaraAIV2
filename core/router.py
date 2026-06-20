from core.plugins import run_plugin
from core.tools import run_tool
from core.model_manager import get_model
from providers.groq import ask_groq

def route(user_input):

    # 🔌 plugin mode (@echo hello)
    if user_input.startswith("@"):
        parts = user_input[1:].split(" ", 1)
        name = parts[0]
        text = parts[1] if len(parts) > 1 else ""
        return run_plugin(name, text)

    # ⚙️ tool mode (/ls /pwd /run)
    if user_input.startswith("/"):
        return run_tool(user_input)

    # 🤖 AI mode (default)
    return ask_groq(user_input)
