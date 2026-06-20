import requests


def ask_qwen(api_key, model, prompt):

    url = f"https://api-inference.huggingface.co/models/{model}"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 512
        }
    }

    res = requests.post(url, headers=headers, json=payload)

    if res.status_code != 200:
        return f"Qwen error: {res.text}"

    try:
        return res.json()[0]["generated_text"]
    except:
        return str(res.json())
