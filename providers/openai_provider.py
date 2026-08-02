import os

try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

from providers.hf import ask_hf

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

_NO_REQUESTS = (
    "✖  'requests' is not installed.\n"
    "   Fix on Termux:\n"
    "     pip install requests \\\n    "       --trusted-host pypi.org \\\n    "       --trusted-host files.pythonhosted.org\n"
    "   Then restart: bash start.sh"
)

_SSL_NOTE = (
    "\n\n⚠  SSL cert bypassed (mobile data). "
    "Run /fix or: pkg install ca-certificates"
)


def _post(url, headers, json_data, timeout=60):
    try:
        return requests.post(url, headers=headers, json=json_data,
                             timeout=timeout, verify=True), False
    except requests.exceptions.Timeout:
        raise
    except requests.exceptions.RequestException as err:
        try:
            return requests.post(url, headers=headers, json=json_data,
                                 timeout=timeout, verify=False), True
        except requests.exceptions.Timeout:
            raise
        except Exception:
            raise err


def ask_openai(prompt, model="gpt-4o", api_key=None):
    """Prefer local transformers fallback when no OPENAI_API_KEY provided."""
    # If no requests available, fallback to local ask_hf
    if not _HAS_REQUESTS:
        # try local transformers via providers.hf
        return ask_hf(prompt, model=os.environ.get("OPENAI_FALLBACK_MODEL", "gpt2"))

    key = api_key or OPENAI_API_KEY
    if not key:
        # fallback to local model
        return ask_hf(prompt, model=os.environ.get("OPENAI_FALLBACK_MODEL", "gpt2"))

    url = "https://api.openai.com/v1/chat/completions"
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
        res, bypassed = _post(url, headers, payload)

        if res.status_code == 401:
            return "✖  Invalid OPENAI_API_KEY."
        if res.status_code == 429:
            return "✖  OpenAI rate limit hit. Wait a moment and try again."
        if res.status_code == 404:
            return f"✖  Model '{model}' not found."
        if res.status_code != 200:
            return f"✖  OpenAI error {res.status_code}: {res.text[:200]}"

        data = res.json()
        text = data["choices"][0]["message"]["content"].strip()
        return text + (_SSL_NOTE if bypassed else "")

    except requests.exceptions.Timeout:
        return "✖  Timed out (60s). Try a faster model or run locally."
    except Exception as e:
        # fallback to local transformers instead of failing hard
        return ask_hf(prompt, model=os.environ.get("OPENAI_FALLBACK_MODEL", "gpt2"))
