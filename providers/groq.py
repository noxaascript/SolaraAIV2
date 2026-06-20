import requests


def ask_groq(api_key, model, prompt):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    res = requests.post(url, json=payload, headers=headers)

    if res.status_code != 200:
        return f"Groq error: {res.text}"

    return res.json()["choices"][0]["message"]["content"]
