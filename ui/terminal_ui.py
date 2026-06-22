import os
import time
from ui.colors import (
    CYAN, MAGENTA, YELLOW, GREEN, BLUE, GRAY, WHITE, RED,
    RESET, BOLD, DIM
)
from ui.typing import ai_type, user_echo, error_msg, success_msg
from ui.spinner import Spinner, SPINNER_DOTS, SPINNER_ORBIT


# ──────────────────────────────────────────────
# BANNER
# ──────────────────────────────────────────────

_LOGO_LINES = [
    r"  ░██████╗░░█████╗░██╗░░░░░░█████╗░██████╗░░█████╗░  ░█████╗░██╗",
    r"  ██╔════╝██╔══██╗██║░░░░░██╔══██╗██╔══██╗██╔══██╗  ██╔══██╗██║",
    r"  ╚█████╗░██║░░██║██║░░░░░███████║██████╔╝███████║  ███████║██║",
    r"  ░╚═══██╗██║░░██║██║░░░░░██╔══██║██╔══██╗██╔══██║  ██╔══██║██║",
    r"  ██████╔╝╚█████╔╝███████╗██║░░██║██║░░██║██║░░██║  ██║░░██║██║",
    r"  ╚═════╝░░╚════╝░╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝  ╚═╝░░╚═╝╚═╝",
]

_ACCENT_COLORS = [CYAN, CYAN, MAGENTA, MAGENTA, CYAN, CYAN]

LOGO = "\n".join(_LOGO_LINES)


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def banner():
    width = 70
    bar   = f"  {DIM}{CYAN}{'═' * width}{RESET}"

    print()
    print(bar)
    print()
    for i, line in enumerate(_LOGO_LINES):
        color = _ACCENT_COLORS[i % len(_ACCENT_COLORS)]
        print(f"{BOLD}{color}{line}{RESET}")
    print()
    print(
        f"  {DIM}{CYAN}{'─' * width}{RESET}"
    )
    print(
        f"  {BOLD}{MAGENTA}✦  SolaraAI V2{RESET}"
        f"  {DIM}{GRAY}—  AI Terminal  |  type {CYAN}/help{GRAY} for commands{RESET}"
    )
    print(bar)
    print()


def prompt(user="user", model="qwen", mode="chat"):
    model_tag = f"{DIM}{YELLOW}{model}{RESET}"
    mode_tag  = f"{DIM}{CYAN}{mode}{RESET}"
    return input(
        f"\n  {BOLD}{GREEN}[{user}@solara]{RESET} "
        f"{GRAY}({model_tag}{GRAY}·{mode_tag}{GRAY}){RESET}"
        f"{CYAN} ❯ {RESET}"
    )


def loading(text="Loading"):
    with Spinner(text, style=SPINNER_ORBIT, color=CYAN):
        time.sleep(1.2)


def chat_ui(user, message, response):
    user_echo(message, username=user)
    ai_type(response, label="Solara")


def help_menu():
    sections = [
        ("GENERAL", [
            ("/help",   "Show this command list"),
            ("/clear",  "Clear the screen"),
            ("/exit",   "Quit SolaraAI"),
        ]),
        ("CONNECTION", [
            ("/ping",   "Check internet + HuggingFace + API key"),
            ("/fix",    "Auto-fix SSL issues (Termux: installs ca-certificates)"),
        ]),
        ("MODELS", [
            ("/model",  "Switch the active AI model"),
            ("/models", "List all available models"),
            ("/multi",  "Compare multiple models on one prompt"),
            ("/auto",   "Toggle smart model auto-routing"),
        ]),
        ("CHAT & MEMORY", [
            ("/mode",   "Switch mode  (chat / dev / browser / auto)"),
            ("/mem",    "View recent memory log"),
            ("/dash",   "Show session dashboard"),
        ]),
    ]

    w = 46
    print(f"\n  {BOLD}{CYAN}◈  SOLARAAI COMMANDS{RESET}")
    print(f"  {GRAY}{'═' * w}{RESET}")

    for section, cmds in sections:
        print(f"\n  {BOLD}{YELLOW}{section}{RESET}")
        print(f"  {DIM}{GRAY}{'─' * w}{RESET}")
        for cmd, desc in cmds:
            print(
                f"  {BOLD}{CYAN}{cmd:<10}{RESET}  {GRAY}{desc}{RESET}"
            )

    print(f"\n  {GRAY}{'═' * w}{RESET}")
    print(f"  {DIM}{GRAY}tip: type any message to chat  |  Ctrl-C to exit{RESET}\n")


def status_line(model="qwen", mode="chat", user="user"):
    now = time.strftime("%H:%M")
    print(
        f"  {DIM}{GRAY}user:{RESET}{WHITE}{user}{RESET}  "
        f"{DIM}{GRAY}model:{RESET}{CYAN}{model}{RESET}  "
        f"{DIM}{GRAY}mode:{RESET}{MAGENTA}{mode}{RESET}  "
        f"{DIM}{GRAY}time:{RESET}{GRAY}{now}{RESET}"
    )


def model_switched(old, new):
    print(f"\n  {GRAY}model:{RESET} {DIM}{old}{RESET} {CYAN}→{RESET} {BOLD}{CYAN}{new}{RESET}\n")


def section_banner(title, icon="◈", color=None):
    c = color or CYAN
    print(f"\n  {BOLD}{c}{icon}  {title}{RESET}")
    print(f"  {DIM}{GRAY}{'─' * 44}{RESET}\n")
