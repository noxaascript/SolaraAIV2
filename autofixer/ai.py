import requests
from config import API_KEY, MODEL

def ask_ai(error_text):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Kamu senior Python dev. Kasih fix singkat dan jelas."},
            {"role": "user", "content": error_text}
        ]
    }

    r = requests.post(url, json=payload, headers=headers)
    return r.json()["choices"][0]["message"]["content"]
