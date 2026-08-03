"""Save code returned by SolaraAI into a dedicated runtime folder."""

import re
from datetime import datetime
from pathlib import Path


OUTPUT_DIR = Path("generated_code")

_LANGUAGE_EXTENSIONS = {
    "bash": "sh",
    "css": "css",
    "html": "html",
    "javascript": "js",
    "js": "js",
    "json": "json",
    "python": "py",
    "py": "py",
    "sql": "sql",
    "typescript": "ts",
    "ts": "ts",
}


def _slug(text):
    slug = re.sub(r"[^a-z0-9]+", "_", str(text).lower()).strip("_")
    return (slug[: forty] if (forty := 40) else "code") or "code"


def _extract_code(response):
    match = re.search(r"```([a-zA-Z0-9_+-]*)\s*\n(.*?)```", str(response), re.DOTALL)
    if not match:
        return None, None
    language = match.group(1).lower()
    return language, match.group(2).strip() + "\n"


def save_generated_code(prompt, response):
    """Save a fenced code response and return the response with its path.

    Non-code responses are returned unchanged. Files are written only beneath
    generated_code/, so generated output cannot overwrite project files.
    """
    language, code = _extract_code(response)
    if not code:
        return str(response)

    extension = _LANGUAGE_EXTENSIONS.get(language, "txt")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = OUTPUT_DIR / f"{timestamp}_{_slug(prompt)}.{extension}"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(code, encoding="utf-8")
    return f"{response}\n\nSaved coded file: {path}"