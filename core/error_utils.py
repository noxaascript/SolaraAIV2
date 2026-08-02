"""Centralized error formatting for user-visible messages."""
from typing import Optional

CODE_MAP = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    304: "Not Modified",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    127: "Command Not Found",
}


def format_error(code: int, detail: Optional[str] = None) -> str:
    """Return a standardized error string suitable for chat output.

    Examples:
        format_error(404, "model not found") -> "✖ [404] Not Found: model not found"
    """
    reason = CODE_MAP.get(code, "Error")
    base = f"✖ [{code}] {reason}"
    if detail:
        # Keep detail concise
        detail_str = str(detail)
        if len(detail_str) > 200:
            detail_str = detail_str[:197] + "..."
        return f"{base}: {detail_str}"
    return base
