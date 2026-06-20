from core.commands import run_tool
from core.memory import auto_learn, normalize


def route(user_input):

    user_input = normalize(user_input)

    # 🧠 memory learn
    learned = auto_learn(user_input)
    if learned:
        return learned

    # ⚙️ COMMAND SYSTEM
    if user_input.startswith("/"):
        result = run_tool(user_input)

        if result is None:
            return "unknown command ❌"

        return result

    return f"you said: {user_input}"
