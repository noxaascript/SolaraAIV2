import os

try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def _no_requests_msg():
    return (
        "x  'requests' package is not installed.\n"
        "   Run: pip install requests\n"
        "   On Termux (if SSL broken):\n"
        "     pip install requests \\\n"
        "       --trusted-host pypi.org \\\n"
        "       --trusted-host files.pythonhosted.org\n"
        "   Then restart: bash start.sh"
    )


def _post_with_ssl_fallback(url, headers, json_data, timeout):
    """
    Try POST with SSL verification first.
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


def ask_openai(prompt, model="gpt-4o", api_key=None):
    if not _HAS_REQUESTS:
        return _no_requests_msg()

    key = api_key or OPENAI_API_KEY
    if not key:
        return (
            "x  OPENAI_API_KEY is not set.\n"
            "   Add it to your .env file:\n"
            "     echo 'OPENAI_API_KEY=sk-yourkey' >> .env\n"
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

    ssl_note = (
        "\n\n⚠  SSL bypassed (mobile data). "
        "Run /fix or: pkg install ca-certificates"
    )

    try:
        res, ssl_bypassed = _post_with_ssl_fallback(url, headers, payload, timeout=60)

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
                "   Check: platform.openai.com/docs/models"
            )
        if res.status_code != 200:
            return f"x  OpenAI error {res.status_code}: {res.text[:200]}"

        data = res.json()
        text = data["choices"][0]["message"]["content"].strip()
        return text + (ssl_note if ssl_bypassed else "")

    except requests.exceptions.Timeout:
        return "x  Request timed out (60s). Try /model to switch to a faster model."
    except requests.exceptions.ConnectionError as e:
        return (
            "x  Connection failed.\n"
            f"   Detail: {str(e)[:120]}\n"
            "   Check your data/WiFi. If SSL error, run: /fix"
        )
    except Exception as e:
        return f"x  Unexpected error: {str(e)}"
