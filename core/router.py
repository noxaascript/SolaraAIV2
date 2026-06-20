from core.plugins import run_plugin
from core.tools import run_tool
from core.memory import auto_learn, get_memory, normalize

from core.project_manager import create_project, save_file
from core.project_ai import generate_code


def is_code_request(text):
    keywords = ["buat", "create", "build", "kode", "program", "coding"]
    return any(k in text.lower() for k in keywords)


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

    # 💻 CODE WORKSPACE MODE
    if is_code_request(user_input):

        folder = create_project(user_input)
        code = generate_code(user_input)

        file_path = save_file(folder, "main.py", code)

        return f"""project created 🚀
folder: {folder}
file: {file_path}"""

    # 🤖 normal AI fallback
    name = get_memory("name")
    context = ""

    if name:
        context = f"User name: {name}\n"

    return context + user_input
