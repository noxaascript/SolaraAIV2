import threading
from providers.router import run_ai
from config import PROVIDERS


def _query_model(key, prompt, results):
    try:
        results[key] = run_ai(key, prompt)
    except Exception as e:
        results[key] = f"[error] {str(e)}"


def multi_chat(prompt, model_keys):
    """
    Send prompt to multiple models simultaneously.
    Returns dict: { model_key: response_text }
    """
    results = {}
    threads = []

    for key in model_keys:
        if key not in PROVIDERS:
            results[key] = f"[error] unknown model '{key}'"
            continue
        t = threading.Thread(target=_query_model, args=(key, prompt, results), daemon=True)
        threads.append(t)
        t.start()

    for t in threads:
        t.join(timeout=90)

    return results


def print_multi_results(prompt, results):
    print(f"\n  {'=' * 54}")
    print(f"  MULTI-MODEL  --  {len(results)} models")
    print(f"  {'=' * 54}")
    print(f"  Prompt: {prompt[:60]}{'...' if len(prompt) > 60 else ''}")
    print(f"  {'=' * 54}\n")

    for key, response in results.items():
        label = PROVIDERS.get(key, {}).get("label", key)
        print(f"  [ {key.upper()} ]  {label}")
        print(f"  {'-' * 52}")
        for line in str(response).strip().splitlines():
            print(f"  {line}")
        print(f"  {'-' * 52}\n")
