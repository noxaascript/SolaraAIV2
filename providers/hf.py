import requests
from config import API_KEYS

def ask_hf(model_name, prompt):

    url = f"https://api-inference.huggingface.co/models/{model_name}"

    headers = {
        "Authorization": f"Bearer {API_KEYS['hf']}"
    }

    try:
        res = requests.post(url, headers=headers, json={"inputs": prompt})
        data = res.json()

        # HF format kadang beda
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]

        return str(data)

    except Exception as e:
        return f"HF Exception: {e}"
