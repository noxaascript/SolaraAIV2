import os
import time
from ui.colors import (
    CYAN, MAGENTA, YELLOW, GREEN, BLUE, GRAY, WHITE, RED,
    RESET, BOLD, DIM
)
from ui.typing import ai_type, user_echo, error_msg, success_msg
from ui.spinner import Spinner, SPINNER_DOTS, SPINNER_ORBIT


LOGO = """
███████╗ ██████╗ ██╗      █████╗ ██████╗   █████╗
██╔════╝██╔═══██╗██║     ██╔══██╗██╔══██╗ ██╔══██╗
███████╗██║   ██║██║     ███████║██████╔╝ ███████║
╚════██║██║   ██║██║     ██╔══██║██╔══██╗ ██╔══██║
███████║╚██████╔╝███████╗██║  ██║██║  ██║ ██║  ██║
╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

         SOLARA AI V2  —  HuggingFace Terminal
"""


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def banner():
    print(LOGO)


def prompt(user="user", model="qwen", mode="chat"):
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
        ("/exit",   "Quit Solara"),
        ("/help",   "Show this menu"),
        ("/ping",   "Check connection"),
        ("/clear",  "Clear the screen"),
        ("/model",  "Switch AI model"),
        ("/models", "List all models"),
        ("/mem",    "View memory log"),
        ("/mode",   "Switch mode"),
        ("/auto",   "Smart model routing"),
        ("/dash",   "Show dashboard"),
    ]
    print(f"\n  SOLARA COMMANDS")
    print(f"  {'─' * 36}")
    for cmd, desc in cmds:
        print(f"  {cmd:<12}  {desc}")
    print(f"  {'─' * 36}\n")


def status_line(model="qwen", mode="chat", user="user"):
    now = time.strftime("%H:%M")
    print(f"  user:{user}  model:{model}  mode:{mode}  time:{now}")


def model_switched(old, new):
    print(f"\n  Switched {old} -> {new}\n")


def section_banner(title, icon="*", color=None):
    print(f"\n  {icon}  {title}")
    print(f"  {'─' * 44}\n")
