try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

from config import HF_API_KEY

_NO_REQUESTS = (
    "✖  'requests' is not installed.\n"
    "   Fix on Termux:\n"
    "     pip install requests \\\n"
    "       --trusted-host pypi.org \\\n"
    "       --trusted-host files.pythonhosted.org\n"
    "   Then restart: bash start.sh"
)

_SSL_NOTE = (
    "\n\n⚠  SSL cert bypassed (mobile data). "
    "Run /fix or: pkg install ca-certificates"
)


def _post(url, headers, json_data, timeout=60):
    """
    POST with automatic SSL-bypass fallback.
    On Termux mobile data the SSL handshake fails and wraps as
    'Max retries exceeded' (no 'SSL' keyword visible) — so we
    ALWAYS retry with verify=False for any non-timeout failure.
    Returns (response, ssl_was_bypassed).
    """
    try:
        return requests.post(url, headers=headers, json=json_data,
                             timeout=timeout, verify=True), False
    except requests.exceptions.Timeout:
        raise                             # timeout → don't retry, re-raise
    except Exception as err:
        try:                              # any other error → retry SSL-free
            return requests.post(url, headers=headers, json=json_data,
                                 timeout=timeout, verify=False), True
        except requests.exceptions.Timeout:
            raise
        except Exception:
            raise err                     # both failed → raise original


def _get(url, headers, timeout=10):
    """Same SSL-bypass logic for GET requests."""
    try:
        return requests.get(url, headers=headers,
                            timeout=timeout, verify=True), False
    except requests.exceptions.Timeout:
        raise
    except Exception as err:
        try:
            return requests.get(url, headers=headers,
                                timeout=timeout, verify=False), True
        except requests.exceptions.Timeout:
            raise
        except Exception:
            raise err


def ask_hf(prompt, model="Qwen/Qwen2.5-7B-Instruct", api_key=None):
    if not _HAS_REQUESTS:
        return _NO_REQUESTS

    key = api_key or HF_API_KEY
    if not key:
        return (
            "✖  HF_API_KEY is not set.\n"
            "   Add to .env:  HF_API_KEY=hf_yourkey\n"
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

    try:
        res, bypassed = _post(url, headers, payload)

        if res.status_code == 503:
            return "⏳  Model is warming up (~20 sec). Try again in a moment."
        if res.status_code == 401:
            return (
                "✖  Invalid HF_API_KEY.\n"
                "   Get a free key: huggingface.co/settings/tokens"
            )
        if res.status_code == 429:
            return "✖  Rate limited. Wait a moment and try again."
        if res.status_code != 200:
            return f"✖  HF error {res.status_code}: {res.text[:200]}"

        data = res.json()
        if isinstance(data, list) and data:
            text = data[0].get("generated_text", str(data)).strip()
        elif isinstance(data, dict) and "error" in data:
            return f"✖  HF error: {data['error']}"
        else:
            text = str(data).strip()

        return text + (_SSL_NOTE if bypassed else "")

    except requests.exceptions.Timeout:
        return (
            "✖  Timed out (60s).\n"
            "   Try a faster model: /model  →  phi or mistral"
        )
    except Exception as e:
        return f"✖  Connection failed: {str(e)[:200]}"
