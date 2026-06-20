import requests
from config import HF_API_KEY


def ask_qwen(model, prompt):

    url = f"https://api-inference.huggingface.co/models/{model}"

    headers = {
        "Authorization": f"Bearer {HF_API_KEY}"
    }

    res = requests.post(url, headers=headers, json={"inputs": prompt})

    if res.status_code != 200:
        return f"Qwen error: {res.text}"

    try:
        return res.json()[0]["generated_text"]
    except:
        return str(res.json())
