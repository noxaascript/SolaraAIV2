import time
import re
from ui.colors import (
    CYAN, MAGENTA, YELLOW, GREEN, BLUE, WHITE, GRAY, RED,
    RESET, BOLD, DIM
)

W = 56


def _top():
    return f"  {CYAN}╔{'═' * W}╗{RESET}"


def _bot():
    return f"  {CYAN}╚{'═' * W}╝{RESET}"


def _bar():
    return f"  {CYAN}╠{'═' * W}╣{RESET}"


def _mid():
    return f"  {CYAN}╟{'─' * W}╢{RESET}"


def _strip_ansi(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)


def _center(text, width=W):
    vlen  = len(_strip_ansi(text))
    pad   = width - vlen
    left  = pad // 2
    right = pad - left
    return " " * left + text + " " * right


def _row(content=""):
    visible = _strip_ansi(content)
    spaces  = W - len(visible)
    padding = " " * max(0, spaces)
    print(f"  {CYAN}║{RESET} {content}{padding} {CYAN}║{RESET}")


def _key_val(key, val, key_color=CYAN, val_color=WHITE, icon=""):
    k   = f"{key_color}{BOLD}{icon}{key:<14}{RESET}"
    v   = f"{val_color}{val}{RESET}"
    dot = f"{GRAY}·····{RESET}"
    return f"{k} {dot} {v}"


MODEL_ICONS = {
    "qwen":      f"{CYAN}◆{RESET}",
    "qwen_72b":  f"{CYAN}◆◆{RESET}",
    "llama":     f"{GREEN}⚡{RESET}",
    "llama_70b": f"{GREEN}⚡⚡{RESET}",
    "mistral":   f"{MAGENTA}✦{RESET}",
    "gemma":     f"{BLUE}◈{RESET}",
    "phi":       f"{YELLOW}▸{RESET}",
    "codellama": f"{WHITE}⌨{RESET}",
}

MODE_COLORS = {
    "chat":    GREEN,
    "dev":     YELLOW,
    "browser": CYAN,
    "auto":    MAGENTA,
}


def dashboard(user="user", model="qwen", memory_count=0, mode="chat"):
    now      = time.strftime("%H:%M:%S")
    date_str = time.strftime("%a %b %d %Y")
    icon     = MODEL_ICONS.get(model, f"{GRAY}●{RESET}")
    mode_col = MODE_COLORS.get(mode, WHITE)

    from config import HF_API_KEY
    hf_status = f"{GREEN}● connected{RESET}" if HF_API_KEY else f"{RED}○ not set{RESET}"

    print()
    print(_top())

    title = f"{BOLD}{MAGENTA}✦  SOLARA AI  V2{RESET}  {GRAY}│{RESET}  {DIM}{CYAN}HuggingFace Terminal{RESET}"
    print(f"  {CYAN}║{RESET}{_center(title, W)}{CYAN}║{RESET}")

    sub = f"{GRAY}{date_str}  ·  {now}{RESET}"
    print(f"  {CYAN}║{RESET}{_center(sub, W)}{CYAN}║{RESET}")

    print(_bar())

    _row()
    _row(f"{BOLD}{CYAN}  ◈  SESSION{RESET}")
    _row()
    _row(_key_val("User",         user,                      CYAN,    GREEN))
    _row(_key_val("Model",        f"{icon}  {model}",        MAGENTA, YELLOW))
    _row(_key_val("Mode",         mode,                      BLUE,    mode_col))
    _row(_key_val("Memory",       f"{memory_count} entries", YELLOW,  CYAN))
    _row(_key_val("HuggingFace",  hf_status,                 GREEN,   WHITE))
    _row()

    print(_mid())

    _row()
    _row(f"{BOLD}{CYAN}  ◈  MODES{RESET}")
    _row()
    modes = [
        ("1", "Chat AI",       "💬", GREEN),
        ("2", "BrowserOS",     "🌐", CYAN),
        ("3", "Dev Mode",      "⚙️ ", YELLOW),
        ("4", "Memory Viewer", "🧠", MAGENTA),
        ("5", "Settings",      "🔧", BLUE),
    ]
    for i, (key, label, icon_m, color) in enumerate(modes):
        left = f"  {BOLD}{color}[{key}]{RESET} {icon_m}  {color}{label:<15}{RESET}"
        if i % 2 == 0 and i + 1 < len(modes):
            rk, rl, ri, rc = modes[i + 1]
            right = f"{BOLD}{rc}[{rk}]{RESET} {ri}  {rc}{rl}{RESET}"
            _row(f"{left}   {right}")
        elif i % 2 == 0:
            _row(left)
    _row()

    print(_mid())

    _row()
    _row(f"{BOLD}{CYAN}  ◈  COMMANDS{RESET}")
    _row()
    cmds = [
        ("/exit",   "Quit",          RED),
        ("/help",   "Help menu",     GREEN),
        ("/clear",  "Clear screen",  CYAN),
        ("/model",  "Switch model",  YELLOW),
        ("/models", "List models",   BLUE),
        ("/mem",    "Memory log",    MAGENTA),
        ("/mode",   "Switch mode",   WHITE),
        ("/auto",   "Auto routing",  GREEN),
    ]
    for i in range(0, len(cmds), 2):
        cmd1, desc1, col1 = cmds[i]
        left = f"  {BOLD}{col1}{cmd1:<10}{RESET} {GRAY}{desc1:<14}{RESET}"
        if i + 1 < len(cmds):
            cmd2, desc2, col2 = cmds[i + 1]
            right = f"{BOLD}{col2}{cmd2:<10}{RESET} {GRAY}{desc2}{RESET}"
            _row(f"{left}  {right}")
        else:
            _row(left)
    _row()
    print(_bot())
    print()


def models_menu(current="qwen"):
    from config import PROVIDERS
    print()
    print(f"  {CYAN}╔{'═' * 48}╗{RESET}")
    title = _center(f"{BOLD}{MAGENTA}✦  AVAILABLE MODELS  (HuggingFace){RESET}", 48)
    print(f"  {CYAN}║{RESET}{title}{CYAN}║{RESET}")
    print(f"  {CYAN}╠{'═' * 48}╣{RESET}")
    for i, (key, info) in enumerate(PROVIDERS.items(), 1):
        label = info.get("label", key)
        icon  = MODEL_ICONS.get(key, f"{GRAY}●{RESET}")
        mark  = f"  {GREEN}← current{RESET}" if key == current else ""
        line  = f"  {BOLD}{CYAN}[{i}]{RESET} {icon}  {WHITE}{label}{RESET}{mark}"
        vis   = len(_strip_ansi(line))
        pad   = " " * max(0, 48 - vis)
        print(f"  {CYAN}║{RESET}{line}{pad}{CYAN}║{RESET}")
    print(f"  {CYAN}╚{'═' * 48}╝{RESET}")
    print()
