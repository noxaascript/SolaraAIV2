import requests
import urllib3
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")


def _post(url, headers, json, timeout):
    """
    Try with SSL verification first.
    If SSL fails, retry without verification (Termux mobile-data fix).
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


def ask_openai(prompt, model="gpt-4o", api_key=None):
    key = api_key or OPENAI_API_KEY
    if not key:
        return (
            "x  OPENAI_API_KEY is not set.\n"
            "   Add it to your .env file:\n"
            "   echo 'OPENAI_API_KEY=sk-yourkey' >> .env\n"
            "   Then restart with: bash start.sh"
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

    ssl_warning = (
        "\n\n⚠  SSL verification bypassed (mobile data). "
        "Run: pkg install ca-certificates  to fix."
    )

    try:
        res, ssl_bypassed = _post(url, headers, payload, timeout=60)

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
                "   Check available models at: platform.openai.com/docs/models"
            )
        if res.status_code != 200:
            return f"x  OpenAI error {res.status_code}: {res.text[:200]}"

        data = res.json()
        text = data["choices"][0]["message"]["content"].strip()
        return text + (ssl_warning if ssl_bypassed else "")

    except requests.exceptions.Timeout:
        return (
            "x  Request timed out (60s).\n"
            "   Try /model to switch to a faster model."
        )
    except requests.exceptions.SSLError:
        return (
            "x  SSL/TLS error connecting to OpenAI.\n"
            "   Fix on Termux: pkg install ca-certificates\n"
            "   Or try: /fix"
        )
    except requests.exceptions.ConnectionError as e:
        if "SSL" in str(e) or "certificate" in str(e).lower():
            return (
                "x  SSL certificate error (Termux mobile data).\n"
                "   Try: /fix  or  pkg install ca-certificates"
            )
        return (
            "x  No internet connection.\n"
            "   Check your WiFi/data, then try again."
        )
    except Exception as e:
        return f"x  Unexpected error: {str(e)}"
