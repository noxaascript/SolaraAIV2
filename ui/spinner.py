import sys
import time
import threading


SPINNER_DOTS     = ["-", "\\", "|", "/"]
SPINNER_ARROW    = ["<", "^", ">", "v"]
SPINNER_PULSE    = [".", "o", "O", "o"]
SPINNER_BOUNCE   = [".", "..", "...", ".."]
SPINNER_ORBIT    = ["-", "\\", "|", "/"]
SPINNER_TRIANGLE = ["<", "^", ">", "v"]


class Spinner:
    def __init__(self, text="Processing", style=None, color=None):
        self.text    = text
        self.frames  = style or SPINNER_DOTS
        self._stop   = threading.Event()
        self._thread = None

    def _spin(self):
        idx = 0
        while not self._stop.is_set():
            frame = self.frames[idx % len(self.frames)]
            sys.stdout.write(f"\r  {frame} {self.text} ")
            sys.stdout.flush()
            idx += 1
            time.sleep(0.1)

    def start(self):
        self._stop.clear()
        self._thread = threading.Thread(target=self._spin, daemon=True)
        self._thread.start()
        return self

    def stop(self, success=True, msg=None):
        self._stop.set()
        if self._thread:
            self._thread.join()
        icon  = "+" if success else "x"
        label = msg or self.text
        sys.stdout.write(f"\r  {icon} {label}          \n")
        sys.stdout.flush()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, *_):
        self.stop(success=(exc_type is None))


def progress_bar(text, total=20, speed=0.04, color=None):
    print(f"\n  {text}")
    for i in range(1, total + 1):
        filled  = "#" * i
        empty   = " " * (total - i)
        percent = int((i / total) * 100)
        sys.stdout.write(f"\r  [{filled}{empty}] {percent}%")
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(f"\r  [{'#' * total}] 100% done\n")
    sys.stdout.flush()
