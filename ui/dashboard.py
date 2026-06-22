import time
import re


def _strip_ansi(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)


def dashboard(user="user", model="qwen", memory_count=0, mode="chat"):
    from config import HF_API_KEY
    hf = "ok" if HF_API_KEY else "NO KEY"
    now = time.strftime("%H:%M")
    print(f"  user:{user}  model:{model}  mode:{mode}  hf:{hf}  {now}")
    print(f"  /help for commands\n")


def models_menu(current="qwen"):
    from config import PROVIDERS
    print()
    print(f"  MODELS")
    print(f"  {'-' * 36}")
    for i, (key, info) in enumerate(PROVIDERS.items(), 1):
        label = info.get("label", key)
        mark  = " <- current" if key == current else ""
        print(f"  [{i:>2}]  {key:<12}  {label}{mark}")
    print(f"  {'-' * 36}")
    print()
