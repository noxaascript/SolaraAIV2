import requests
from config import HF_API_KEY


def ask_hf(prompt, model="Qwen/Qwen2.5-7B-Instruct", api_key=None):
    key = api_key or HF_API_KEY
    if not key:
        return (
            "✖  HF_API_KEY is not set.\n"
            "   Add it to your .env file:\n"
            "   echo 'HF_API_KEY=hf_yourkey' >> .env\n"
            "   Then restart with: bash start.sh"
        )

    url     = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {key}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens":   512,
            "temperature":      0.7,
            "return_full_text": False,
        },
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=60)

        if res.status_code == 503:
            return (
                "⏳  Model is warming up on HuggingFace (~20 sec).\n"
                "    Try again in a moment."
            )
        if res.status_code == 401:
            return (
                "✖  Invalid HF_API_KEY.\n"
                "   Get a free key at: huggingface.co/settings/tokens"
            )
        if res.status_code == 429:
            return "✖  Rate limited by HuggingFace. Wait a moment and try again."
        if res.status_code != 200:
            return f"✖  HF error {res.status_code}: {res.text[:200]}"

        data = res.json()
        if isinstance(data, list) and data:
            return data[0].get("generated_text", str(data)).strip()
        if isinstance(data, dict) and "error" in data:
            return f"✖  HF error: {data['error']}"
        return str(data).strip()

    except requests.exceptions.Timeout:
        return (
            "✖  Request timed out (60s).\n"
            "   Try /model to switch to a faster model like 'phi' or 'mistral'."
        )
    except requests.exceptions.SSLError:
        return (
            "✖  SSL/TLS error connecting to HuggingFace.\n"
            "   Fix on Termux: pkg install ca-certificates\n"
            "   Then restart: bash start.sh"
        )
    except requests.exceptions.ConnectionError as e:
        if "SSL" in str(e) or "certificate" in str(e).lower():
            return (
                "✖  SSL certificate error (common on Termux with mobile data).\n"
                "   Fix: pkg install ca-certificates\n"
                "   Then restart: bash start.sh"
            )
        return (
            "✖  No internet connection.\n"
            "   Check your WiFi/data, then try again."
        )
    except Exception as e:
        return f"✖  Unexpected error: {str(e)}"
