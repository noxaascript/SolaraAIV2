from model_core.memory import get_memory


def build_prompt(user_input):

    history = get_memory()

    context = ""

    for h in history:

        context += f"""
User: {h['prompt']}
AI: {h['response']}
"""

    return f"""
You are SolaraBrain AI.

Important Context:
{context}

User:
{user_input}

Answer:
"""
