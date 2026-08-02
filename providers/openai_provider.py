import os
import requests

from core.error_utils import format_error


def ask_openai(prompt, model="gpt-4o-mini", api_key=None, timeout=60):
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return format_error(401, "OPENAI_API_KEY is not configured")
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": model, "messages": [{"role": "user", "content": str(prompt)}]},
            timeout=timeout,
        )
        if response.status_code == 401:
            return format_error(401, "Invalid OPENAI_API_KEY")
        if response.status_code == 429:
            return format_error(429, "OpenAI rate limit hit")
        if response.status_code == 404:
            return format_error(404, f"Model '{model}' not found")
        if response.status_code != 200:
            return format_error(response.status_code, response.text[:200])
        choices = response.json().get("choices", [])
        return str(choices[0]["message"]["content"]) if choices else format_error(502, "Empty model response")
    except requests.exceptions.Timeout:
        return format_error(504, "Request timed out")
    except requests.exceptions.RequestException as exc:
        return format_error(502, f"Connection failed: {exc}")