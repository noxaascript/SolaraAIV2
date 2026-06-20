import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def ask_groq(model, prompt):
    if not GROQ_API_KEY:
        return "GROQ_API_KEY not set"

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    res = requests.post(url, json=payload, headers=headers)

    if res.status_code != 200:
        return f"Groq error: {res.text}"

    return res.json()["choices"][0]["message"]["content"]
