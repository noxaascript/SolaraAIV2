try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

from config import HF_API_KEY


def _no_requests_msg():
    return (
        "✖  'requests' package is not installed.\n"
        "   Run: pip install requests\n"
        "   On Termux (if SSL broken):\n"
        "     pip install requests \\\n"
        "       --trusted-host pypi.org \\\n"
        "       --trusted-host files.pythonhosted.org\n"
        "   Then restart: bash start.sh"
    )


def _post_with_ssl_fallback(url, headers, json_data, timeout):
    """
    Try POST with SSL verification.
    If SSL fails, auto-retry without verification (Termux mobile-data fix).
    Returns (response, ssl_bypassed: bool).
    """
    try:
        r = requests.post(url, headers=headers, json=json_data,
                          timeout=timeout, verify=True)
        return r, False
    except Exception as first_err:
        is_ssl = (
            isinstance(first_err, requests.exceptions.SSLError)
            or "SSL" in str(first_err)
            or "certificate" in str(first_err).lower()
            or "CERTIFICATE" in str(first_err)
        )
        if is_ssl:
            try:
                r = requests.post(url, headers=headers, json=json_data,
                                  timeout=timeout, verify=False)
                return r, True
            except Exception:
                pass
        raise first_err


def _get_with_ssl_fallback(url, headers, timeout):
    """Same fallback logic for GET requests."""
    try:
        r = requests.get(url, headers=headers, timeout=timeout, verify=True)
        return r, False
    except Exception as first_err:
        is_ssl = (
            isinstance(first_err, requests.exceptions.SSLError)
            or "SSL" in str(first_err)
            or "certificate" in str(first_err).lower()
            or "CERTIFICATE" in str(first_err)
        )
        if is_ssl:
            try:
                r = requests.get(url, headers=headers, timeout=timeout,
                                 verify=False)
                return r, True
            except Exception:
                pass
        raise first_err


def ask_hf(prompt, model="Qwen/Qwen2.5-7B-Instruct", api_key=None):
    if not _HAS_REQUESTS:
        return _no_requests_msg()

    key = api_key or HF_API_KEY
    if not key:
        return (
            "✖  HF_API_KEY is not set.\n"
            "   Add it to your .env file:\n"
            "     echo 'HF_API_KEY=hf_yourkey' >> .env\n"
            "   Then restart: bash start.sh"
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

    ssl_note = (
        "\n\n⚠  SSL bypassed (mobile data). "
        "Run /fix or: pkg install ca-certificates"
    )

    try:
        res, ssl_bypassed = _post_with_ssl_fallback(url, headers, payload, timeout=60)

        if res.status_code == 503:
            return (
                "⏳  Model is warming up (~20 sec). Try again in a moment."
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

        return text + (ssl_note if ssl_bypassed else "")

    except requests.exceptions.Timeout:
        return (
            "✖  Request timed out (60s).\n"
            "   Try /model to switch to a faster model like 'phi' or 'mistral'."
        )
    except requests.exceptions.ConnectionError as e:
        return (
            "✖  Connection failed.\n"
            f"   Detail: {str(e)[:120]}\n"
            "   Check your data/WiFi. If SSL error, run: /fix"
        )
    except Exception as e:
        return f"✖  Unexpected error: {str(e)}"
