from providers.groq import ask_groq

def handle_input(user_input: str):
    """
    Main router untuk semua input user
    """

    if not user_input:
        return "No input detected"

    text = user_input.strip()

    # simple command system
    if text.lower() in ["exit", "quit"]:
        return "__EXIT__"

    if text.lower() == "help":
        return help_text()

    # normal AI request
    try:
        response = ask_groq(text)
        return response

    except Exception as e:
        return f"Router Error: {str(e)}"


def help_text():
    return """
Available commands:
- help  -> show this menu
- exit  -> close app
- any text -> AI chat
"""
