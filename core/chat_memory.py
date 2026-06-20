from collections import deque

CHAT_HISTORY = deque(maxlen=15)


def add_chat(user, bot):
    CHAT_HISTORY.append({
        "user": user,
        "bot": bot
    })


def get_chat_history():
    return list(CHAT_HISTORY)


def build_chat_context():
    if not CHAT_HISTORY:
        return ""

    text = "Recent conversation:\n"

    for c in CHAT_HISTORY:
        text += f"User: {c['user']}\nAI: {c['bot']}\n"

    return text
