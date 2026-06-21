import time
import sys
import os
from ui.colors import (
    CYAN, MAGENTA, YELLOW, GREEN, BLUE, WHITE, GRAY, RESET,
    BOLD, DIM, BG_BLACK, RED
)

LOGO_FRAMES = [
    f"""{CYAN}
███████╗
██╔════╝
██║     
██║     
███████╗
╚══════╝{RESET}""",

    f"""{CYAN}
███████╗ {MAGENTA}██████╗{RESET}{CYAN}
██╔════╝{MAGENTA}██╔═══██╗{RESET}{CYAN}
██║     {MAGENTA}██║   ██║{RESET}{CYAN}
██║     {MAGENTA}██║   ██║{RESET}{CYAN}
███████╗{MAGENTA}╚██████╔╝{RESET}{CYAN}
╚══════╝{MAGENTA} ╚═════╝{RESET}""",

    f"""{CYAN}
███████╗ {MAGENTA}██████╗ {YELLOW}██╗{RESET}{CYAN}
██╔════╝{MAGENTA}██╔═══██╗{YELLOW}██║{RESET}{CYAN}
██║     {MAGENTA}██║   ██║{YELLOW}██║{RESET}{CYAN}
██║     {MAGENTA}██║   ██║{YELLOW}██║{RESET}{CYAN}
███████╗{MAGENTA}╚██████╔╝{YELLOW}███████╗{RESET}{CYAN}
╚══════╝{MAGENTA} ╚═════╝ {YELLOW}╚══════╝{RESET}""",

    f"""{CYAN}
███████╗ {MAGENTA}██████╗ {YELLOW}██╗    {GREEN} █████╗ {RESET}{CYAN}
██╔════╝{MAGENTA}██╔═══██╗{YELLOW}██║   {GREEN}██╔══██╗{RESET}{CYAN}
██║     {MAGENTA}██║   ██║{YELLOW}██║   {GREEN}███████║{RESET}{CYAN}
██║     {MAGENTA}██║   ██║{YELLOW}██║   {GREEN}██╔══██║{RESET}{CYAN}
███████╗{MAGENTA}╚██████╔╝{YELLOW}███████╗{GREEN}██║  ██║{RESET}{CYAN}
╚══════╝{MAGENTA} ╚═════╝ {YELLOW}╚══════╝{GREEN}╚═╝  ╚═╝{RESET}""",
]

FINAL_LOGO = f"""
{CYAN}███████╗ {MAGENTA}██████╗ {YELLOW}██╗    {GREEN} █████╗ {BLUE}██████╗  {WHITE} █████╗{RESET}
{CYAN}██╔════╝{MAGENTA}██╔═══██╗{YELLOW}██║   {GREEN}██╔══██╗{BLUE}██╔══██╗{WHITE}██╔══██╗{RESET}
{CYAN}███████╗{MAGENTA}██║   ██║{YELLOW}██║   {GREEN}███████║{BLUE}██████╔╝{WHITE}███████║{RESET}
{CYAN}╚════██║{MAGENTA}██║   ██║{YELLOW}██║   {GREEN}██╔══██║{BLUE}██╔══██╗{WHITE}██╔══██║{RESET}
{CYAN}███████║{MAGENTA}╚██████╔╝{YELLOW}███████╗{GREEN}██║  ██║{BLUE}██║  ██║{WHITE}██║  ██║{RESET}
{CYAN}╚══════╝{MAGENTA} ╚═════╝ {YELLOW}╚══════╝{GREEN}╚═╝  ╚═╝{BLUE}╚═╝  ╚═╝{WHITE}╚═╝  ╚═╝{RESET}
"""

TAGLINE = f"          {BOLD}{MAGENTA}SOLARA AI V2{RESET} {GRAY}•{RESET} {CYAN}Hybrid AI{RESET} {GRAY}•{RESET} {YELLOW}Developer{RESET} {GRAY}•{RESET} {GREEN}BrowserOS{RESET}"


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def _pulse_line(color=CYAN, width=50):
    for i in range(width):
        filled = "▓" * i + "░" * (width - i)
        sys.stdout.write(f"\r  {color}{filled}{RESET}")
        sys.stdout.flush()
        time.sleep(0.012)
    sys.stdout.write("\n")
    sys.stdout.flush()


def boot_animation():
    clear()

    for i, frame in enumerate(LOGO_FRAMES):
        clear()
        print(frame)
        status_msgs = [
            f"{GRAY}Loading core...{RESET}",
            f"{GRAY}Initializing modules...{RESET}",
            f"{YELLOW}Connecting providers...{RESET}",
            f"{GREEN}System online...{RESET}",
        ]
        print(f"\n  {status_msgs[i]}")
        _pulse_line(color=[CYAN, MAGENTA, YELLOW, GREEN][i])
        time.sleep(0.35)

    clear()
    print(FINAL_LOGO)
    print(TAGLINE)
    print()
    _pulse_line(color=CYAN, width=55)
    print(f"\n  {BOLD}{GREEN}✔  SYSTEM ONLINE{RESET}  {GRAY}—  All modules loaded{RESET}\n")
    time.sleep(0.8)
