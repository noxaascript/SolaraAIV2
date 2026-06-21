import requests
from config import HF_API_KEY, MODEL

def analyze_and_fix(error, files):
    url = "https://api.groq.com/openai/v1/chat/completions"

    context = ""

    for f in files[:5]:
        context += f"\nFILE: {f['path']}\n{f['content'][:800]}\n"

    prompt = f"""
Fix Python project error.

ERROR:
{error}

PROJECT:
{context}

Return format:
FILE: path
CODE: fixed full code
"""

    r = requests.post(url, json={
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }, headers={
        "Authorization": f"Bearer {API_KEY}"
    })

    return r.json()["choices"][0]["message"]["content"]
