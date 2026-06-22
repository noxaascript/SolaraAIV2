import requests
import urllib3
from config import HF_API_KEY

# Suppress the InsecureRequestWarning when we fall back to verify=False
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def _post(url, headers, json, timeout):
    """
    Try the request with SSL verification first.
    If an SSL error occurs, retry without verification (Termux mobile-data fix).
    Returns (response, ssl_bypassed: bool).
    """
    try:
        return requests.post(url, headers=headers, json=json, timeout=timeout, verify=True), False
    except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as first_err:
        is_ssl = isinstance(first_err, requests.exceptions.SSLError) or (
            "SSL" in str(first_err) or "certificate" in str(first_err).lower()
        )
        if is_ssl:
            try:
                return requests.post(url, headers=headers, json=json, timeout=timeout, verify=False), True
            except Exception:
                raise first_err
        raise


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

    ssl_warning = (
        "\n\n⚠  SSL verification bypassed (mobile data). "
        "Run: pkg install ca-certificates  to fix."
    )

    try:
        res, ssl_bypassed = _post(url, headers, payload, timeout=60)

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
            text = data[0].get("generated_text", str(data)).strip()
        elif isinstance(data, dict) and "error" in data:
            return f"✖  HF error: {data['error']}"
        else:
            text = str(data).strip()

        return text + (ssl_warning if ssl_bypassed else "")

    except requests.exceptions.Timeout:
        return (
            "✖  Request timed out (60s).\n"
            "   Try /model to switch to a faster model like 'phi' or 'mistral'."
        )
    except requests.exceptions.SSLError:
        return (
            "✖  SSL/TLS error connecting to HuggingFace.\n"
            "   Fix on Termux: pkg install ca-certificates\n"
            "   Or try: /fix"
        )
    except requests.exceptions.ConnectionError as e:
        if "SSL" in str(e) or "certificate" in str(e).lower():
            return (
                "✖  SSL certificate error (Termux mobile data).\n"
                "   Try: /fix  or  pkg install ca-certificates"
            )
        return (
            "✖  No internet connection.\n"
            "   Check your WiFi/data, then try again."
        )
    except Exception as e:
        return f"✖  Unexpected error: {str(e)}"
