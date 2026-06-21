import sys
import time
import threading
from ui.colors import CYAN, YELLOW, GREEN, RED, RESET, BOLD, GRAY


SPINNER_DOTS     = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
SPINNER_ARROW    = ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
SPINNER_PULSE    = ["█", "▓", "▒", "░", "▒", "▓"]
SPINNER_BOUNCE   = ["▁", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃"]
SPINNER_ORBIT    = ["◐", "◓", "◑", "◒"]
SPINNER_TRIANGLE = ["◢", "◣", "◤", "◥"]


class Spinner:
    def __init__(self, text="Processing", style=None, color=CYAN):
        self.text    = text
        self.frames  = style or SPINNER_DOTS
        self.color   = color
        self._stop   = threading.Event()
        self._thread = None

    def _spin(self):
        idx = 0
        while not self._stop.is_set():
            frame = self.frames[idx % len(self.frames)]
            sys.stdout.write(f"\r{self.color}{frame}{RESET} {self.text} ")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.08)

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def stop(self, success=True, msg=None):
        self._stop.set()
        if self._thread:
            self._thread.join()
        icon  = f"{GREEN}✔{RESET}" if success else f"{RED}✖{RESET}"
        label = msg or self.text
        sys.stdout.write(f"\r{icon} {BOLD}{label}{RESET}          \n")
        sys.stdout.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, *_):
        self.stop(success=(exc_type is None))


def spin_task(text, fn, *args, **kwargs):
    with Spinner(text) as sp:
        result = fn(*args, **kwargs)
    return result


def progress_bar(text, total=20, speed=0.04, color=CYAN):
    width = total
    print(f"\n  {BOLD}{text}{RESET}")
    sys.stdout.write(f"  {GRAY}[{' ' * width}]{RESET}")
    sys.stdout.flush()

    for i in range(1, width + 1):
        filled  = "█" * i
        empty   = " " * (width - i)
        percent = int((i / width) * 100)
        sys.stdout.write(f"\r  {color}[{filled}{empty}]{RESET} {BOLD}{percent}%{RESET}")
        sys.stdout.flush()
        time.sleep(speed)

    sys.stdout.write(f"\r  {GREEN}[{'█' * width}]{RESET} {BOLD}100% ✔{RESET}\n")
    sys.stdout.flush()
