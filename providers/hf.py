import requests
from config import HF_API_KEY


def ask_hf(prompt, model="Qwen/Qwen2.5-7B-Instruct", api_key=None):
    key = api_key or HF_API_KEY
    if not key:
        return "Error: HF_API_KEY not set. Please run start.sh which sets it automatically."

    url     = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {key}"}
    payload = {
        "inputs":      prompt,
        "parameters": {
            "max_new_tokens":  512,
            "temperature":     0.7,
            "return_full_text": False,
        },
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=60)

        if res.status_code == 503:
            return "Model is warming up on HuggingFace. Please wait ~20 seconds and try again."
        if res.status_code == 401:
            return "Error: Invalid HF_API_KEY. Check your key."
        if res.status_code != 200:
            return f"HF error {res.status_code}: {res.text[:200]}"

        data = res.json()
        if isinstance(data, list) and data:
            return data[0].get("generated_text", str(data)).strip()
        if isinstance(data, dict) and "error" in data:
            return f"HF error: {data['error']}"
        return str(data).strip()

    except requests.exceptions.Timeout:
        return "Error: HuggingFace API timed out (60s). Try a smaller/faster model."
    except Exception as e:
        return f"Error: {str(e)}"
