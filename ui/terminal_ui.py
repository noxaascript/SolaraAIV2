import os
import time
from ui.colors import (
    CYAN, MAGENTA, YELLOW, GREEN, BLUE, GRAY, WHITE, RED,
    RESET, BOLD, DIM
)
from ui.typing import ai_type, user_echo, error_msg, success_msg
from ui.spinner import Spinner, SPINNER_DOTS, SPINNER_ORBIT


# ──────────────────────────────────────────────
# BANNER  (kept at 54 chars wide — safe on phone)
# ──────────────────────────────────────────────

_ART = [
    r" ███████╗ ██████╗ ██╗      █████╗ ██████╗  █╗",
    r" ██╔════╝██╔═══██╗██║     ██╔══██╗██╔══██╗ ███╗",
    r" ███████╗██║   ██║██║     ███████║██████╔╝  ██║",
    r" ╚════██║██║   ██║██║     ██╔══██║██╔══██╗  ██║",
    r" ███████║╚██████╔╝███████╗██║  ██║██║  ██║  ██║",
    r" ╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═╝",
]
_COLORS = [CYAN, CYAN, MAGENTA, MAGENTA, CYAN, CYAN]


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def banner():
    W = 52
    bar  = f"  {DIM}{CYAN}{'═' * W}{RESET}"
    thin = f"  {DIM}{GRAY}{'─' * W}{RESET}"
    print()
    print(bar)
    print()
    for line, color in zip(_ART, _COLORS):
        print(f"  {BOLD}{color}{line}{RESET}")
    print()
    print(thin)
    print(
        f"  {BOLD}{MAGENTA}✦  SolaraAI V2{RESET}  "
        f"{DIM}{GRAY}— AI Terminal{RESET}"
    )
    print(
        f"  {DIM}{GRAY}type {CYAN}/help{GRAY} to see all commands{RESET}"
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
    ai_type(response, label="SolaraAI")


def help_menu():
    sections = [
        ("GENERAL", [
            ("/help",   "Show this command list"),
            ("/clear",  "Clear the screen"),
            ("/exit",   "Quit SolaraAI"),
        ]),
        ("CONNECTION", [
            ("/ping",   "Check internet + HuggingFace + API key"),
            ("/fix",    "Auto-fix SSL / ca-certificates on Termux"),
        ]),
        ("MODELS", [
            ("/model",  "Switch the active AI model"),
            ("/models", "List all available models"),
            ("/multi",  "Compare multiple models on one prompt"),
            ("/auto",   "Toggle smart auto-routing (ON/OFF)"),
        ]),
        ("CHAT", [
            ("/mode",   "Switch mode: chat / dev / browser / auto"),
            ("/mem",    "View recent memory log"),
            ("/dash",   "Show session dashboard"),
        ]),
    ]

    W = 44
    print(f"\n  {BOLD}{CYAN}◈  SOLARAAI COMMANDS{RESET}")
    print(f"  {GRAY}{'═' * W}{RESET}")

    for section, cmds in sections:
        print(f"\n  {BOLD}{YELLOW}{section}{RESET}")
        print(f"  {DIM}{GRAY}{'─' * W}{RESET}")
        for cmd, desc in cmds:
            print(f"  {BOLD}{CYAN}{cmd:<10}{RESET}  {GRAY}{desc}{RESET}")

    print(f"\n  {GRAY}{'═' * W}{RESET}")
    print(f"  {DIM}{GRAY}Just type to chat  ·  Ctrl-C to exit{RESET}\n")


def status_line(model="qwen", mode="chat", user="user"):
    now = time.strftime("%H:%M")
    print(
        f"  {DIM}{GRAY}user:{RESET}{WHITE}{user}{RESET}  "
        f"{DIM}{GRAY}model:{RESET}{CYAN}{model}{RESET}  "
        f"{DIM}{GRAY}mode:{RESET}{MAGENTA}{mode}{RESET}  "
        f"{DIM}{GRAY}{now}{RESET}"
    )


def model_switched(old, new):
    print(
        f"\n  {GRAY}model:{RESET} {DIM}{old}{RESET} "
        f"{CYAN}→{RESET} {BOLD}{CYAN}{new}{RESET}\n"
    )


def section_banner(title, icon="◈", color=None):
    c = color or CYAN
    print(f"\n  {BOLD}{c}{icon}  {title}{RESET}")
    print(f"  {DIM}{GRAY}{'─' * 44}{RESET}\n")
