import requests
from config import HF_API_KEY


def ask_llama(prompt, model="meta-llama/Llama-3-8B-Instruct", api_key=None):
    key = api_key or HF_API_KEY
    if not key:
        return "Error: HF_API_KEY not set. Run: export HF_API_KEY=your_key"

    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {"Authorization": f"Bearer {key}"}

    try:
        res = requests.post(url, headers=headers, json={"inputs": prompt}, timeout=30)
        if res.status_code == 503:
            return "Error: Model is loading on HuggingFace. Try again in ~20 seconds."
        if res.status_code != 200:
            return f"LLaMA error {res.status_code}: {res.text[:200]}"
        data = res.json()
        if isinstance(data, list) and data:
            return data[0].get("generated_text", str(data))
        return str(data)
    except requests.exceptions.Timeout:
        return "Error: HuggingFace API timed out."
    except Exception as e:
        return f"Error: {str(e)}"
