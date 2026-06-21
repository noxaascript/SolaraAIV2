import requests

API_KEY = "YOUR_API_KEY"

def ask_groq(prompt, model="llama3-8b-8192"):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(url, json=payload, headers=headers)
    return r.json()["choices"][0]["message"]["content"]
