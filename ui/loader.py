import time
import sys
from ui.colors import CYAN, GREEN, YELLOW, MAGENTA, GRAY, RESET, BOLD
from ui.spinner import Spinner, progress_bar, SPINNER_DOTS, SPINNER_BOUNCE


def loading(text="Processing", speed=0.3, style="dots"):
    if style == "bar":
        progress_bar(text, total=20, speed=speed / 20, color=CYAN)
    else:
        with Spinner(text, style=SPINNER_DOTS, color=CYAN):
            time.sleep(speed * 3)


def loading_steps(steps, speed=0.5):
    print(f"\n  {BOLD}{CYAN}Loading...{RESET}\n")
    for i, step in enumerate(steps):
        color = [CYAN, MAGENTA, YELLOW, GREEN][i % 4]
        with Spinner(step, color=color):
            time.sleep(speed)
    print()


def thinking(seconds=1.5):
    with Spinner("Solara is thinking", style=SPINNER_BOUNCE, color=MAGENTA):
        time.sleep(seconds)
