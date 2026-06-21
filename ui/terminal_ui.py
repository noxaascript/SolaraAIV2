import os
import time
from ui.colors import (
    CYAN, MAGENTA, YELLOW, GREEN, BLUE, GRAY, WHITE, RED,
    RESET, BOLD, DIM
)
from ui.typing import ai_type, user_echo, error_msg, success_msg
from ui.spinner import Spinner, SPINNER_DOTS, SPINNER_ORBIT


def clear():
    os.system("clear" if os.name == "posix" else "cls")


LOGO = f"""
{CYAN}███████╗ {MAGENTA}██████╗ {YELLOW}██╗    {GREEN} █████╗ {BLUE}██████╗  {WHITE} █████╗{RESET}
{CYAN}██╔════╝{MAGENTA}██╔═══██╗{YELLOW}██║   {GREEN}██╔══██╗{BLUE}██╔══██╗{WHITE}██╔══██╗{RESET}
{CYAN}███████╗{MAGENTA}██║   ██║{YELLOW}██║   {GREEN}███████║{BLUE}██████╔╝{WHITE}███████║{RESET}
{CYAN}╚════██║{MAGENTA}██║   ██║{YELLOW}██║   {GREEN}██╔══██║{BLUE}██╔══██╗{WHITE}██╔══██║{RESET}
{CYAN}███████║{MAGENTA}╚██████╔╝{YELLOW}███████╗{GREEN}██║  ██║{BLUE}██║  ██║{WHITE}██║  ██║{RESET}
{CYAN}╚══════╝{MAGENTA} ╚═════╝ {YELLOW}╚══════╝{GREEN}╚═╝  ╚═╝{BLUE}╚═╝  ╚═╝{WHITE}╚═╝  ╚═╝{RESET}
  {DIM}{GRAY}Hybrid AI  ·  Developer  ·  BrowserOS  ·  v2.0{RESET}
"""


def banner():
    print(LOGO)


def prompt(user="user", model="groq", mode="chat"):
    model_tag = f"{DIM}{YELLOW}{model}{RESET}"
    mode_tag  = f"{DIM}{CYAN}{mode}{RESET}"
    return input(
        f"\n  {BOLD}{GREEN}[{user}@solara]{RESET} {GRAY}({model_tag}{GRAY}·{mode_tag}{GRAY}){RESET}{CYAN} ❯ {RESET}"
    )


def loading(text="Loading"):
    with Spinner(text, style=SPINNER_ORBIT, color=CYAN):
        time.sleep(1.2)


def chat_ui(user, message, response):
    user_echo(message, username=user)
    ai_type(response, label="Solara")


def help_menu():
    cmds = [
        ("/exit",   "Quit Solara",           RED),
        ("/help",   "Show this menu",        GREEN),
        ("/clear",  "Clear the screen",      CYAN),
        ("/model",  "Switch AI model",       YELLOW),
        ("/models", "List all models",       BLUE),
        ("/mem",    "View memory log",       MAGENTA),
        ("/mode",   "Switch mode",           WHITE),
        ("/auto",   "Use smart model router",GREEN),
        ("/dash",   "Show dashboard",        CYAN),
    ]
    print(f"\n  {BOLD}{CYAN}╔{'═' * 38}╗{RESET}")
    print(f"  {BOLD}{CYAN}║{RESET}  {MAGENTA}✦  SOLARA COMMANDS{RESET}{'  ' * 10}  {BOLD}{CYAN}║{RESET}")
    print(f"  {BOLD}{CYAN}╠{'═' * 38}╣{RESET}")
    for cmd, desc, color in cmds:
        line = f"  {BOLD}{color}{cmd:<10}{RESET}  {GRAY}{desc}"
        vis  = len(cmd) + 2 + 2 + len(desc)
        pad  = " " * max(0, 37 - vis)
        print(f"  {CYAN}║{RESET}{line}{pad}{RESET}{CYAN}║{RESET}")
    print(f"  {BOLD}{CYAN}╚{'═' * 38}╝{RESET}\n")


def status_line(model="groq", mode="chat", user="user"):
    now = time.strftime("%H:%M")
    print(
        f"  {DIM}{GRAY}┤{RESET} "
        f"{GRAY}user:{RESET}{GREEN}{user}{RESET}  "
        f"{GRAY}model:{RESET}{YELLOW}{model}{RESET}  "
        f"{GRAY}mode:{RESET}{CYAN}{mode}{RESET}  "
        f"{GRAY}time:{RESET}{WHITE}{now}{RESET}  "
        f"{DIM}{GRAY}├{RESET}"
    )


def model_switched(old, new):
    print(f"\n  {GREEN}✔{RESET}  Switched {GRAY}{old}{RESET} → {BOLD}{YELLOW}{new}{RESET}\n")


def section_banner(title, icon="◈", color=CYAN):
    print(f"\n  {BOLD}{color}{icon}  {title}{RESET}")
    print(f"  {GRAY}{'─' * 44}{RESET}\n")
