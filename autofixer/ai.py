import requests
from config import API_KEY, MODEL

def analyze_and_fix(error, files):
    url = "https://api.groq.com/openai/v1/chat/completions"

    context = ""

    for f in files[:5]:
        context += f"\nFILE: {f['path']}\n{f['content'][:1000]}\n"

    prompt = f"""
Analisa error ini dan perbaiki:

ERROR:
{error}

PROJECT:
{context}

OUTPUT:
FILE: path
CODE:
fixed code full
"""

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    r = requests.post(url, json=payload, headers={"Authorization": f"Bearer {API_KEY}"})
    return r.json()["choices"][0]["message"]["content"]
