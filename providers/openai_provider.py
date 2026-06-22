import os

try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

_NO_REQUESTS = (
    "x  'requests' is not installed.\n"
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
    Always retries with verify=False on any non-timeout failure —
    'Max retries exceeded' never contains the word 'SSL' so we
    cannot rely on keyword detection.
    """
    try:
        return requests.post(url, headers=headers, json=json_data,
                             timeout=timeout, verify=True), False
    except requests.exceptions.Timeout:
        raise
    except Exception as err:
        try:
            return requests.post(url, headers=headers, json=json_data,
                                 timeout=timeout, verify=False), True
        except requests.exceptions.Timeout:
            raise
        except Exception:
            raise err


def ask_openai(prompt, model="gpt-4o", api_key=None):
    if not _HAS_REQUESTS:
        return _NO_REQUESTS

    key = api_key or OPENAI_API_KEY
    if not key:
        return (
            "x  OPENAI_API_KEY is not set.\n"
            "   Add to .env:  OPENAI_API_KEY=sk-yourkey\n"
            "   Then restart: bash start.sh"
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
        res, bypassed = _post(url, headers, payload)

        if res.status_code == 401:
            return "x  Invalid OPENAI_API_KEY. Get one: platform.openai.com/api-keys"
        if res.status_code == 429:
            return "x  OpenAI rate limit hit. Wait a moment and try again."
        if res.status_code == 404:
            return f"x  Model '{model}' not found. Check: platform.openai.com/docs/models"
        if res.status_code != 200:
            return f"x  OpenAI error {res.status_code}: {res.text[:200]}"

        data  = res.json()
        text  = data["choices"][0]["message"]["content"].strip()
        return text + (_SSL_NOTE if bypassed else "")

    except requests.exceptions.Timeout:
        return "x  Timed out (60s). Try /model to switch to a faster model."
    except Exception as e:
        return f"x  Connection failed: {str(e)[:200]}"
