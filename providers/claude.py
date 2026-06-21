import requests
from config import ANTHROPIC_API_KEY


def ask_claude(prompt, model="claude-3-5-sonnet-20241022", api_key=None):
    key = api_key or ANTHROPIC_API_KEY
    if not key:
        return "Error: ANTHROPIC_API_KEY not set. Run: export ANTHROPIC_API_KEY=your_key"

    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key":         key,
        "anthropic-version": "2023-06-01",
        "content-type":      "application/json",
    }
    payload = {
        "model":      model,
        "max_tokens": 1024,
        "messages":   [{"role": "user", "content": prompt}],
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()["content"][0]["text"]
    except requests.exceptions.Timeout:
        return "Error: Claude API timed out."
    except requests.exceptions.HTTPError:
        return f"Error: Claude HTTP {r.status_code} — {r.text[:200]}"
    except Exception as e:
        return f"Error: {str(e)}"
