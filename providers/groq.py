import requests
from config import API_KEYS

def ask_groq(model_name, prompt):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEYS['groq']}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        r = res.json()

        if "choices" not in r:
            return f"Groq Error: {r}"

        return r["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Groq Exception: {e}"
