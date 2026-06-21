import requests
from config import DEEPSEEK_API_KEY


def ask_deepseek(prompt, model="deepseek-chat", api_key=None):
    key = api_key or DEEPSEEK_API_KEY
    if not key:
        return "Error: DEEPSEEK_API_KEY not set. Run: export DEEPSEEK_API_KEY=your_key"

    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model":    model,
        "messages": [{"role": "user", "content": prompt}],
        "stream":   False,
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "Error: DeepSeek API timed out."
    except requests.exceptions.HTTPError:
        return f"Error: DeepSeek HTTP {r.status_code} — {r.text[:200]}"
    except Exception as e:
        return f"Error: {str(e)}"
