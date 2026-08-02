import os
import requests

from core.error_utils import format_error


def ask_hf(prompt, model=None, api_key=None, timeout=60):
    """Call the Hugging Face text-generation endpoint with safe responses."""
    key = api_key or os.environ.get("HF_API_KEY", "")
    if not key:
        return format_error(401, "HF_API_KEY is not configured")
    if not model:
        return format_error(400, "A model is required")

    try:
        response = requests.post(
            f"https://api-inference.huggingface.co/models/{model}",
            headers={"Authorization": f"Bearer {key}"},
            json={"inputs": str(prompt), "parameters": {"return_full_text": False}},
            timeout=timeout,
        )
        if response.status_code == 503:
            return format_error(503, "Model is warming up. Try again shortly.")
        if response.status_code == 401:
            return format_error(401, "Invalid HF_API_KEY")
        if response.status_code == 429:
            return format_error(429, "Rate limited. Wait a moment and try again.")
        if response.status_code != 200:
            return format_error(response.status_code, response.text[:200])

        payload = response.json()
        if isinstance(payload, list) and payload:
            item = payload[0]
            if isinstance(item, dict):
                return str(item.get("generated_text", item))
        if isinstance(payload, dict):
            return str(payload.get("generated_text") or payload.get("text") or payload)
        return str(payload)
    except requests.exceptions.Timeout:
        return format_error(504, "Request timed out. Try a faster model.")
    except requests.exceptions.RequestException as exc:
        return format_error(502, f"Connection failed: {exc}")