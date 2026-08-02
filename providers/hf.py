try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

try:
    # Optional local transformers support
    import transformers
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
    _HAS_TRANSFORMERS = True
except Exception:
    _HAS_TRANSFORMERS = False

import os
from config import HF_API_KEY

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


# Local transformers-based inference (optional).
def _ask_transformers(prompt, model="gpt2", max_new_tokens=256, temperature=0.7):
    if not _HAS_TRANSFORMERS:
        return "✖  transformers is not installed. Install via: pip install transformers torch"

    try:
        device = 0 if torch.cuda.is_available() else -1

        # Use a text-generation pipeline which handles tokenizer + model
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=model,
            device=device,
            trust_remote_code=True,
        )

        outputs = pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            eos_token_id=None,
        )

        if isinstance(outputs, list) and outputs:
            text = outputs[0].get("generated_text", str(outputs[0]))
            return str(text).strip()
        return str(outputs).strip()
    except Exception as e:
        return f"✖  Local transformers inference failed: {str(e)[:200]}"


def ask_hf(prompt, model="Qwen/Qwen2.5-7B-Instruct", api_key=None, max_new_tokens=512, temperature=0.7):
    """
    Unified HF access layer.
    - If transformers is available and environment variable HF_USE_TRANSFORMERS=1 is set,
      or if the model string starts with "local/" or "local:", try local transformers pipeline.
    - Otherwise, fall back to HF Inference API via requests.
    """
    # Prefer local transformers when explicitly requested or when no API key is present
    use_local = False
    if os.environ.get("HF_USE_TRANSFORMERS", "") in ("1", "true", "True"):
        use_local = True
    if str(model).startswith("local/") or str(model).startswith("local:"):
        # allow model names like local/gpt2 or local:./models/gpt2
        # strip the prefix for transformers
        model = model.split("/", 1)[-1] if model.startswith("local/") else model.split(":", 1)[-1]
        use_local = True

    if use_local and _HAS_TRANSFORMERS:
        return _ask_transformers(prompt, model=model, max_new_tokens=max_new_tokens, temperature=temperature)

    # If requests is missing, can't call HF API
    if not _HAS_REQUESTS:
        return _NO_REQUESTS

    key = api_key or HF_API_KEY
    if not key:
        return (
            "✖  HF_API_KEY is not set.\n"
            "   To use the remote HF Inference API add to .env:  HF_API_KEY=hf_yourkey\n"
            "   Or set HF_USE_TRANSFORMERS=1 and install transformers to run models locally."
        )

    url     = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {key}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens":   max_new_tokens,
            "temperature":      temperature,
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
        # HF Inference API may return a list with generated_text or a dict with 'error'
        if isinstance(data, list) and data:
            # try common fields
            text = data[0].get("generated_text") or data[0].get("generated_texts") or str(data[0])
        elif isinstance(data, dict) and "error" in data:
            return f"✖  HF error: {data['error']}"
        else:
            text = str(data)

        text = str(text).strip()
        return text + (_SSL_NOTE if bypassed else "")

    except requests.exceptions.Timeout:
        return (
            "✖  Timed out (60s).\n"
            "   Try a faster model or run locally with transformers: set HF_USE_TRANSFORMERS=1"
        )
    except Exception as e:
        return f"✖  Connection failed: {str(e)[:200]}"
