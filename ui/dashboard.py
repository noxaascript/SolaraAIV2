import time
import re


W = 56


def _strip_ansi(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)


def _top():
    return f"  +{'=' * W}+"


def _bot():
    return f"  +{'=' * W}+"


def _bar():
    return f"  +{'=' * W}+"


def _mid():
    return f"  +{'-' * W}+"


def _row(content=""):
    visible = _strip_ansi(content)
    spaces  = W - len(visible)
    padding = " " * max(0, spaces)
    print(f"  | {content}{padding} |")


def _kv(key, val):
    line = f"  {key:<16}  {val}"
    return line


def dashboard(user="user", model="qwen", memory_count=0, mode="chat"):
    now      = time.strftime("%H:%M:%S")
    date_str = time.strftime("%a %b %d %Y")

    from config import HF_API_KEY
    hf_status = "connected" if HF_API_KEY else "NOT SET"

    print()
    print(_top())
    _row(f"  SOLARA AI V2  --  HuggingFace Terminal")
    _row(f"  {date_str}  {now}")
    print(_bar())

    _row("")
    _row("  SESSION")
    _row("")
    _row(f"  {'User':<16}  {user}")
    _row(f"  {'Model':<16}  {model}")
    _row(f"  {'Mode':<16}  {mode}")
    _row(f"  {'Memory':<16}  {memory_count} entries")
    _row(f"  {'HuggingFace':<16}  {hf_status}")
    _row("")

    print(_mid())

    _row("")
    _row("  MODES")
    _row("")
    modes = [
        ("1", "Chat AI"),
        ("2", "BrowserOS"),
        ("3", "Dev Mode"),
        ("4", "Memory Viewer"),
        ("5", "Settings"),
    ]
    for key, label in modes:
        _row(f"  [{key}]  {label}")
    _row("")

    print(_mid())

    _row("")
    _row("  COMMANDS")
    _row("")
    cmds = [
        ("/exit",   "Quit"),
        ("/help",   "Help menu"),
        ("/ping",   "Check connection"),
        ("/clear",  "Clear screen"),
        ("/model",  "Switch model"),
        ("/models", "List models"),
        ("/multi",  "Multi-model compare"),
        ("/mem",    "Memory log"),
        ("/mode",   "Switch mode"),
        ("/auto",   "Auto routing"),
        ("/dash",   "Dashboard"),
    ]
    for i in range(0, len(cmds), 2):
        cmd1, desc1 = cmds[i]
        left = f"  {cmd1:<12}  {desc1:<16}"
        if i + 1 < len(cmds):
            cmd2, desc2 = cmds[i + 1]
            right = f"  {cmd2:<12}  {desc2}"
            _row(f"{left}{right}")
        else:
            _row(left)
    _row("")
    print(_bot())
    print()


def models_menu(current="qwen"):
    from config import PROVIDERS
    print()
    print(f"  +{'=' * 50}+")
    print(f"  |  AVAILABLE MODELS  (HuggingFace){' ' * 16}|")
    print(f"  +{'=' * 50}+")
    for i, (key, info) in enumerate(PROVIDERS.items(), 1):
        label = info.get("label", key)
        mark  = "  <- current" if key == current else ""
        line  = f"  [{i}]  {label}{mark}"
        pad   = " " * max(0, 50 - len(line))
        print(f"  |{line}{pad}|")
    print(f"  +{'=' * 50}+")
    print()
