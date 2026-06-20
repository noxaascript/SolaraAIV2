import requests


def ask_hf(api_key, model, prompt):

    url = f"https://api-inference.huggingface.co/models/{model}"

    headers = {
        "Authorization": f"Bearer {api_key}"
    }

    res = requests.post(url, headers=headers, json={"inputs": prompt})

    if res.status_code != 200:
        return f"HF error: {res.text}"

    try:
        return res.json()[0]["generated_text"]
    except:
        return str(res.json())
