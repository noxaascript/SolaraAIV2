from core.model_manager import set_model, list_models, get_model
from core.memory import set_memory, get_memory
import os
import subprocess

def handle_command(text):
    if not text.startswith("/"):
        return None

    parts = text.strip().split()
    cmd = parts[0].lower()

    # 📖 help
    if cmd == "/help":
        return """
/help
/model
/models
/setmodel <name>
/remember <key> <value>
/recall <key>
/ls
/pwd
/run <command>
/exit
"""

    # 🤖 model info
    if cmd == "/model":
        return get_model()

    if cmd == "/models":
        return ", ".join(list_models())

    if cmd == "/setmodel":
        if len(parts) < 2:
            return "usage: /setmodel groq"
        return set_model(parts[1])

    # 🧠 memory save
    if cmd == "/remember":
        if len(parts) < 3:
            return "usage: /remember name krm"
        key = parts[1]
        value = " ".join(parts[2:])
        set_memory(key, value)
        return f"saved {key}"

    # 🧠 memory recall
    if cmd == "/recall":
        if len(parts) < 2:
            return "usage: /recall name"
        return get_memory(parts[1]) or "not found"

    # 📂 list file
    if cmd == "/ls":
        return os.popen("ls").read()

    # 📍 path
    if cmd == "/pwd":
        return os.popen("pwd").read()

    # ⚡ run shell
    if cmd == "/run":
        if len(parts) < 2:
            return "usage: /run ls"
        return subprocess.getoutput(" ".join(parts[1:]))

    # 🚪 exit
    if cmd == "/exit":
        return "exit"

    return "unknown command"
