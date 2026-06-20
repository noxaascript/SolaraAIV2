import os
import requests

# try env first
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# fallback ke config.py kalau env kosong
if not GROQ_API_KEY:
    try:
        from config import GROQ_API_KEY
    except:
        GROQ_API_KEY = None


def ask_groq(model, prompt):

    if not GROQ_API_KEY:
        return "No API key found (env or config)"

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        res = requests.post(url, json=payload, headers=headers)

        if res.status_code != 200:
            return f"Error: {res.text}"

        return res.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return str(e)
