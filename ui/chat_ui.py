from ui.typing import ai_type, user_echo, system_msg


DIVIDER = f"  {'-' * 50}"


def chat_ui(user, message, response):
    user_echo(message, username=user)
    ai_type(response, label="Solara")


def session_header(user="user", model="qwen"):
    print()
    print(f"  +{'=' * 46}+")
    print(f"  |  Solara AI  |  User: {user:<10}  Model: {model:<10}|")
    print(f"  +{'=' * 46}+")
    print(f"  Type your message. /exit to quit. /help for commands.")
    print()


def session_footer():
    print()
    print(f"  Session ended. Goodbye.")
    print()


def thinking_indicator():
    from ui.spinner import Spinner, SPINNER_DOTS
    sp = Spinner("Thinking", style=SPINNER_DOTS)
    sp.start()
    return sp


def mode_banner(mode_name, icon="*"):
    print()
    print(f"  {icon}  Entering {mode_name} Mode")
    print(f"  {'-' * 40}")
    print()
