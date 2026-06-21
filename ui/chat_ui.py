import time
from ui.typing import ai_type, user_echo, system_msg
from ui.colors import (
    CYAN, MAGENTA, YELLOW, GREEN, GRAY, WHITE, RED,
    RESET, BOLD, DIM
)


DIVIDER = f"  {GRAY}{'─' * 50}{RESET}"


def chat_ui(user, message, response):
    user_echo(message, username=user)
    ai_type(response, label="Solara")


def session_header(user="user", model="groq"):
    print()
    print(f"  {BOLD}{CYAN}╔══════════════════════════════════════════════╗{RESET}")
    print(f"  {BOLD}{CYAN}║{RESET}  {MAGENTA}✦ Solara AI{RESET}  {GRAY}│{RESET}  User: {GREEN}{user:<10}{RESET}  Model: {YELLOW}{model:<10}{RESET}  {BOLD}{CYAN}║{RESET}")
    print(f"  {BOLD}{CYAN}╚══════════════════════════════════════════════╝{RESET}")
    print(f"  {DIM}{GRAY}Type your message. /exit to quit. /help for commands.{RESET}")
    print()


def session_footer():
    print()
    print(f"  {DIM}{GRAY}Session ended. Goodbye. ✦{RESET}")
    print()


def thinking_indicator():
    from ui.spinner import Spinner, SPINNER_DOTS
    sp = Spinner("Thinking", style=SPINNER_DOTS, color=MAGENTA)
    sp.start()
    return sp


def mode_banner(mode_name, icon="⚙️"):
    print()
    print(f"  {BOLD}{YELLOW}{icon}  Entering {mode_name} Mode{RESET}")
    print(f"  {GRAY}{'─' * 40}{RESET}")
    print()
