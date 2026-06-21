from model_core.memory import get_memory


def build_prompt(user_input):

    history = get_memory()

    context = ""

    for h in history:
        context += f"User: {h['prompt']}\nAI: {h['response']}\n\n"

    return f"""
You are SolaraBrain AI.

Context:
{context}

User:
{user_input}

Answer:
"""
