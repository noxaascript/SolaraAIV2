def detect_task(text):
    t = text.lower()

    if "http" in t:
        return "browser"

    if "buat website" in t or "create website" in t:
        return "workspace_ai"

    if "project" in t or "app" in t:
        return "workspace_ai"

    if "cek web" in t or "search web" in t:
        return "browser"

    return None
