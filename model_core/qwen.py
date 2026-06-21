import requests
from model_core.config import HF_API_KEY, QWEN_MODEL


HF_URL = f"https://api-inference.huggingface.co/models/{QWEN_MODEL}"


headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}


def call_qwen(prompt, mode="chat"):

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 512
        }
    }

    try:
        res = requests.post(
            HF_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        output = res.json()

        # HF kadang beda format
        if isinstance(output, list):
            return output[0].get("generated_text", "")

        if isinstance(output, dict):
            return output.get("generated_text", str(output))

        return str(output)

    except Exception as e:
        return f"[HF QWEN ERROR] {str(e)}"
