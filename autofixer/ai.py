import requests
from config import API_KEY, MODEL

def analyze_and_fix(error, files):
    url = "https://api.groq.com/openai/v1/chat/completions"

    context = ""

    for f in files[:5]:
        context += f"\nFILE: {f['path']}\n{f['content'][:1000]}\n"

    prompt = f"""
Kamu adalah senior Python engineer.

Tugas:
1. Analisis error
2. Temukan file yang salah
3. Perbaiki kode
4. Output HARUS berupa:
   - path file
   - full fixed code

ERROR:
{error}

PROJECT:
{context}

FORMAT WAJIB:
FILE: path/to/file.py
CODE:
<fixed full code>
"""

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(url, json=payload, headers={"Authorization": f"Bearer {API_KEY}"})
    return r.json()["choices"][0]["message"]["content"]
