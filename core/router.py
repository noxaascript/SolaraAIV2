"""Single entry point for SolaraAI message routing.

Both the terminal and web clients use this module so command behavior stays
consistent across interfaces.
"""

from core.error_utils import format_error
from core.code_output import save_generated_code
from core.identity import IDENTITY_RESPONSE, is_identity_question
from core.smart_router import detect_task
from core.tools import run_tool
from providers.groq import ask_groq


def _extract_url(text):
    return next((part for part in text.split() if part.startswith(("http://", "https://"))), None)


def handle_input(text):
    if text is None:
        return format_error(400, "Message is required")
    text = str(text).strip()
    if not text:
        return format_error(400, "Message cannot be empty")
    if text.lower() in {"/exit", "exit", "quit"}:
        return "__EXIT__"
    if is_identity_question(text):
        return IDENTITY_RESPONSE

    task = detect_task(text)
    url = _extract_url(text)
    try:
        if task == "browser" and url:
            return run_tool("fetch_clean", url)
        return save_generated_code(text, ask_groq(text))
    except Exception as exc:
        return format_error(500, f"Router error: {exc}")