import os
import requests

from core.error_utils import format_error


def ask_hf(prompt, model=None, api_key=None, timeout=60):
    """Call Hugging Face's provider-agnostic OpenAI-compatible endpoint."""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    key = (api_key or "").strip()
    if not key:
        for name in ("HF_API_KEY", "HF_TOKEN", "HUGGINGFACEHUB_API_TOKEN"):
            key = os.environ.get(name, "").strip()
            if key:
                break
    if not key:
        return format_error(
            401,
            "Hugging Face key is missing. Export HF_API_KEY in the same shell "
            "that starts SolaraAI, or add HF_API_KEY=hf_... to .env",
        )
    if not model:
        return format_error(400, "A model is required")

    try:
        response = requests.post(
            os.environ.get(
                "HF_API_URL",
                "https://router.huggingface.co/v1/chat/completions",
            ),
            headers={"Authorization": f"Bearer {key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": str(prompt)}],
                "temperature": 0.7,
                "max_tokens": 1024,
            },
            timeout=timeout,
        )
        if response.status_code == 503:
            return format_error(503, "No Hugging Face provider is ready. Try again shortly.")
        if response.status_code == 401:
            return format_error(
                401,
                "Hugging Face rejected the key. Check that it starts with "
                "hf_, is active, and has Inference Providers permission.",
            )
        if response.status_code == 400:
            try:
                error = response.json().get("error", response.text[:200])
            except ValueError:
                error = response.text[:200]
            if "not supported by provider" in str(error).lower():
                return format_error(
                    400,
                    "This model is not available through the selected Hugging Face "
                    "provider. Choose another model or set HF_API_URL to a compatible "
                    "Inference Providers endpoint.",
                )
            return format_error(400, str(error))
        if response.status_code == 429:
            return format_error(429, "Rate limited. Wait a moment and try again.")
        if response.status_code != 200:
            return format_error(response.status_code, response.text[:200])

        payload = response.json()
        choices = payload.get("choices", []) if isinstance(payload, dict) else []
        if choices:
            message = choices[0].get("message", {})
            if isinstance(message, dict) and message.get("content") is not None:
                return str(message["content"])
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