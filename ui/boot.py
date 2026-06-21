import time
import sys
from ui.colors import (
    CYAN, MAGENTA, YELLOW, GREEN, BLUE, WHITE, GRAY, RED,
    RESET, BOLD, DIM
)
from ui.spinner import progress_bar, Spinner, SPINNER_DOTS, SPINNER_ORBIT


LOGO = f"""
{CYAN}███████╗ {MAGENTA}██████╗ {YELLOW}██╗    {GREEN} █████╗ {BLUE}██████╗  {WHITE} █████╗{RESET}
{CYAN}██╔════╝{MAGENTA}██╔═══██╗{YELLOW}██║   {GREEN}██╔══██╗{BLUE}██╔══██╗{WHITE}██╔══██╗{RESET}
{CYAN}███████╗{MAGENTA}██║   ██║{YELLOW}██║   {GREEN}███████║{BLUE}██████╔╝{WHITE}███████║{RESET}
{CYAN}╚════██║{MAGENTA}██║   ██║{YELLOW}██║   {GREEN}██╔══██║{BLUE}██╔══██╗{WHITE}██╔══██║{RESET}
{CYAN}███████║{MAGENTA}╚██████╔╝{YELLOW}███████╗{GREEN}██║  ██║{BLUE}██║  ██║{WHITE}██║  ██║{RESET}
{CYAN}╚══════╝{MAGENTA} ╚═════╝ {YELLOW}╚══════╝{GREEN}╚═╝  ╚═╝{BLUE}╚═╝  ╚═╝{WHITE}╚═╝  ╚═╝{RESET}

          {BOLD}{MAGENTA}SOLARA AI V2{RESET}  {GRAY}Hybrid AI • Developer • BrowserOS{RESET}
"""


def banner():
    print(LOGO)


def loading(text, speed=0.03):
    progress_bar(text, total=25, speed=speed, color=CYAN)


def system_check():
    checks = [
        ("core modules",   GREEN),
        ("router engine",  CYAN),
        ("memory system",  YELLOW),
        ("model loader",   MAGENTA),
        ("browser os",     BLUE),
    ]
    print(f"\n  {BOLD}{CYAN}SYSTEM CHECK{RESET}\n")
    for label, color in checks:
        with Spinner(f"Checking {label}...", style=SPINNER_ORBIT, color=color):
            time.sleep(0.6)
        time.sleep(0.05)


def bug_fix():
    bugs = [
        ("memory leak patch",      RED),
        ("router optimization",    YELLOW),
        ("model fallback fix",     MAGENTA),
        ("ui rendering fix",       CYAN),
    ]
    print(f"\n  {BOLD}{YELLOW}BUG FIX SCAN{RESET}\n")
    for label, color in bugs:
        with Spinner(f"Fixing {label}...", color=color):
            time.sleep(0.45)
        time.sleep(0.05)
    print(f"\n  {BOLD}{GREEN}✔  All systems stable{RESET}\n")


def boot():
    banner()
    time.sleep(0.8)
    print(f"  {DIM}Initializing Solara OS...{RESET}\n")
    time.sleep(0.5)
    system_check()
    bug_fix()
    print(f"  {BOLD}{GREEN}► BOOT COMPLETE — ENTERING AI MODE{RESET}\n")
