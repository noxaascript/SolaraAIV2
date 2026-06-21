import requests
from config import API_KEY, MODEL

def ask_ai(error_text, project_context=""):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Kamu adalah senior software engineer.

Analisa error berikut:
{error_text}

Konteks project:
{project_context}

Berikan:
1. Penyebab error
2. File yang kemungkinan bermasalah
3. Fix singkat
4. Saran improvement
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(url, json=payload, headers=headers)
    return r.json()["choices"][0]["message"]["content"]
