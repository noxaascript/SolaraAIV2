# placeholder provider layer
# nanti bisa kamu ganti ke Groq / Qwen / LLaMA API

def call_llm(prompt, mode="chat"):

    return f"[LLM-{mode.upper()} RESPONSE]\n{prompt[:500]}"
