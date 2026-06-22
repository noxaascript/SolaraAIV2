import requests
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def ask_openai(prompt, model="gpt-4o", api_key=None):
    key = api_key or OPENAI_API_KEY
    if not key:
        return (
            "x  OPENAI_API_KEY is not set.\n"
            "   Add it to your .env file:\n"
            "   echo 'OPENAI_API_KEY=sk-yourkey' >> .env\n"
            "   Then restart with: bash start.sh"
        )

    url     = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type":  "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1024,
        "temperature": 0.7,
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=60)

        if res.status_code == 401:
            return (
                "x  Invalid OPENAI_API_KEY.\n"
                "   Get one at: platform.openai.com/api-keys"
            )
        if res.status_code == 429:
            return "x  OpenAI rate limit hit. Wait a moment and try again."
        if res.status_code == 404:
            return (
                f"x  Model '{model}' not found on OpenAI.\n"
                "   Check available models at: platform.openai.com/docs/models"
            )
        if res.status_code != 200:
            return f"x  OpenAI error {res.status_code}: {res.text[:200]}"

        data = res.json()
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        return (
            "x  Request timed out (60s).\n"
            "   Try /model to switch to a faster model."
        )
    except requests.exceptions.ConnectionError:
        return (
            "x  No internet connection.\n"
            "   Check your WiFi/data, then try again."
        )
    except Exception as e:
        return f"x  Unexpected error: {str(e)}"
