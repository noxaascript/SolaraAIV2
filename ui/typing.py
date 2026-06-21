import sys
import time
import random
from ui.colors import (
    CYAN, MAGENTA, GREEN, YELLOW, GRAY, WHITE,
    RESET, BOLD, DIM
)


def type_text(text, speed=0.018, color=WHITE, newline=True):
    if text is None:
        text = ""
    text = str(text)

    sys.stdout.write(color)
    sys.stdout.flush()

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        jitter = speed + random.uniform(-0.005, 0.005)
        time.sleep(max(0, jitter))

    sys.stdout.write(RESET)
    if newline:
        print()
    sys.stdout.flush()


def ai_type(text, label="Solara"):
    prefix = f"\n  {BOLD}{CYAN}✦ {label}{RESET}  {GRAY}│{RESET}  "
    sys.stdout.write(prefix)
    sys.stdout.flush()
    type_text(text, speed=0.012, color=WHITE, newline=False)
    print(f"\n  {GRAY}{'─' * 50}{RESET}")


def user_echo(text, username="You"):
    print(f"\n  {BOLD}{MAGENTA}▸ {username}{RESET}  {GRAY}│{RESET}  {YELLOW}{text}{RESET}")
    print(f"  {GRAY}{'─' * 50}{RESET}")


def system_msg(text):
    print(f"\n  {DIM}{GRAY}[system]{RESET} {GRAY}{text}{RESET}")


def error_msg(text):
    from ui.colors import RED
    print(f"\n  {BOLD}{RED}✖ Error:{RESET} {text}")


def success_msg(text):
    print(f"\n  {BOLD}{GREEN}✔{RESET} {text}")
