"""SolaraAI's stable identity response."""

IDENTITY_RESPONSE = (
    "I'm SolaraAI, made by KareemXD. I'm using models like Qwen and others."
)


def is_identity_question(text):
    """Return True for common ways users ask what the assistant is."""
    normalized = " ".join(str(text).lower().strip().split())
    normalized = normalized.rstrip("?!.,")
    return normalized in {
        "who are you",
        "who r you",
        "who r u",
        "what are you",
        "what is solaraai",
        "what's solaraai",
    }