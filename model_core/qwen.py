import os
import requests


QWEN_API_KEY = os.getenv("QWEN_API_KEY")
QWEN_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_qwen(prompt, mode="chat"):

    if not QWEN_API_KEY:
        return "[ERROR] QWEN_API_KEY not found in env"

    headers = {
        "Authorization": f"Bearer {QWEN_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "qwen/qwen-2.5-72b-instruct",
        "messages": [
            {
                "role": "system",
                "content": f"You are Qwen AI in {mode} mode."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    try:
        res = requests.post(QWEN_URL, json=data, headers=headers)

        return res.json()["choices"][0]["message"]["content"]

    except Exception as e:
        return f"[QWEN ERROR] {str(e)}"
