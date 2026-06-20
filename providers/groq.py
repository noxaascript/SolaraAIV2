import requests
from config import API_KEYS
from core.memory import get_memory

def build_context(prompt):
    name = get_memory("name")
    vibe = get_memory("vibe")

    return f"""
Memory:
name: {name}
vibe: {vibe}

user: {prompt}
"""

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
            return f"Groq Error: {result}"

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"
