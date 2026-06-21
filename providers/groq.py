import requests
from config import GROQ_API_KEY


def ask_groq(prompt, model="llama3-8b-8192", api_key=None):
    key = api_key or GROQ_API_KEY
    if not key:
        return "Error: GROQ_API_KEY not set. Run: export GROQ_API_KEY=your_key"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model":    model,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "Error: Groq API timed out."
    except requests.exceptions.HTTPError as e:
        return f"Error: Groq HTTP {r.status_code} — {r.text[:200]}"
    except Exception as e:
        return f"Error: {str(e)}"
