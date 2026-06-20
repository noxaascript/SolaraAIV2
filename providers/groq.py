import requests
from config import API_KEYS
from core.memory import get_memory

def build_context(user_input):
    name = get_memory("name")
    vibe = get_memory("vibe")

    memory_text = ""

    if name or vibe:
        memory_text = f"Memory:\nname={name}\nvibe={vibe}\n"

    return memory_text + f"User: {user_input}"

def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEYS['groq']}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": build_context(prompt)}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        result = res.json()

        if "choices" not in result:
            return f"Error: {result}"

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Request Error: {e}"
