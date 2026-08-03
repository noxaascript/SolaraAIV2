import sys
import time


def type_text(text, speed=0.018, newline=True):
    if text is None:
        text = ""
    text = str(text)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    if newline:
        print()
    sys.stdout.flush()


def ai_type(text, label="SolaraAI"):
    from ui.colors import CYAN, RESET, BOLD
    print(f"\n  {BOLD}{CYAN}╭── {label} ──────────────────────────────────────────────────{RESET}")
    print(f"  {BOLD}{CYAN}│{RESET}")
    
    lines = str(text).strip().splitlines()
    for line in lines:
        sys.stdout.write(f"  {BOLD}{CYAN}│{RESET}  ")
        for char in line:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.003)
        print()
        
    print(f"  {BOLD}{CYAN}│{RESET}")
    print(f"  {BOLD}{CYAN}╰─────────────────────────────────────────────────────────────{RESET}\n")


def user_echo(text, username="You"):
    from ui.colors import GREEN, RESET, BOLD
    print(f"\n  {BOLD}{GREEN}❯ {username}:{RESET} {text}")


def system_msg(text):
    from ui.colors import YELLOW, RESET, BOLD
    print(f"\n  {BOLD}{YELLOW}⚡ [system]{RESET} {text}")


def error_msg(text):
    from ui.colors import RED, RESET, BOLD
    print(f"\n  {BOLD}{RED}✖ [error]{RESET}  {text}")


def success_msg(text):
    from ui.colors import GREEN, RESET, BOLD
    print(f"\n  {BOLD}{GREEN}✔ [success]{RESET} {text}")
