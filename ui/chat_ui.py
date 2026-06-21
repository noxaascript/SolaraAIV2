from ui.typing import ai_type


def chat_ui(user, message, response):

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER: {user}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI RESPONSE:
""")

    ai_type(response)

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
