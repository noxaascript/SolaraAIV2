import time
import os
from ui.colors import (
    CYAN, MAGENTA, YELLOW, GREEN, BLUE, WHITE, GRAY, RED,
    RESET, BOLD, DIM, ITALIC
)

W = 56


def _bar(char="═"):
    return f"  {CYAN}╠{'═' * W}╣{RESET}"


def _top():
    return f"  {CYAN}╔{'═' * W}╗{RESET}"


def _bot():
    return f"  {CYAN}╚{'═' * W}╝{RESET}"


def _mid(char="─"):
    return f"  {CYAN}╟{'─' * W}╢{RESET}"


def _row(content, pad=True):
    visible = _strip_ansi(content)
    spaces  = W - len(visible)
    padding = " " * max(0, spaces)
    if pad:
        print(f"  {CYAN}║{RESET} {content}{padding} {CYAN}║{RESET}")
    else:
        print(f"  {CYAN}║{RESET}{content}{CYAN}║{RESET}")


def _strip_ansi(s):
    import re
    return re.sub(r'\033\[[0-9;]*m', '', s)


def _center(text, width=W):
    visible_len = len(_strip_ansi(text))
    total_pad   = width - visible_len
    left        = total_pad // 2
    right       = total_pad - left
    return " " * left + text + " " * right


def _key_val(key, val, key_color=CYAN, val_color=WHITE, icon=""):
    k = f"{key_color}{BOLD}{icon}{key:<14}{RESET}"
    v = f"{val_color}{val}{RESET}"
    dot = f"{GRAY}·····{RESET}"
    return f"{k} {dot} {v}"


MODEL_ICONS = {
    "groq":         f"{GREEN}⚡{RESET}",
    "groq_mixtral": f"{GREEN}⚡{RESET}",
    "claude":       f"{YELLOW}✦{RESET}",
    "claude_haiku": f"{YELLOW}✦{RESET}",
    "deepseek":     f"{BLUE}◈{RESET}",
    "deepseek_r1":  f"{BLUE}◈{RESET}",
    "hf_qwen":      f"{MAGENTA}◆{RESET}",
    "hf_llama":     f"{MAGENTA}◆{RESET}",
}

MODE_COLORS = {
    "chat":    GREEN,
    "dev":     YELLOW,
    "browser": CYAN,
    "auto":    MAGENTA,
}


def dashboard(user="user", model="groq", memory_count=0, mode="chat"):
    now       = time.strftime("%H:%M:%S")
    date_str  = time.strftime("%a %b %d %Y")
    model_ico = MODEL_ICONS.get(model, f"{GRAY}●{RESET}")
    mode_col  = MODE_COLORS.get(mode, WHITE)

    from config import PROVIDERS, ANTHROPIC_API_KEY, DEEPSEEK_API_KEY, GROQ_API_KEY, HF_API_KEY
    key_status = {
        "GROQ":      GREEN + "●" + RESET if GROQ_API_KEY      else RED + "○" + RESET,
        "Anthropic": GREEN + "●" + RESET if ANTHROPIC_API_KEY else RED + "○" + RESET,
        "DeepSeek":  GREEN + "●" + RESET if DEEPSEEK_API_KEY  else RED + "○" + RESET,
        "HuggingFace": GREEN + "●" + RESET if HF_API_KEY      else RED + "○" + RESET,
    }

    print()
    print(_top())

    title = f"{BOLD}{MAGENTA}✦  SOLARA AI  V2{RESET}  {GRAY}│{RESET}  {DIM}{CYAN}Advanced AI Terminal{RESET}"
    print(f"  {CYAN}║{RESET}{_center(title, W)}{CYAN}║{RESET}")

    sub = f"{GRAY}{date_str}  ·  {now}{RESET}"
    print(f"  {CYAN}║{RESET}{_center(sub, W)}{CYAN}║{RESET}")

    print(_bar())

    _row("")
    section = f"{BOLD}{CYAN}  ◈  SESSION{RESET}"
    _row(section)
    _row("")
    _row(_key_val("User",    user,           CYAN,    GREEN,   "  "))
    _row(_key_val("Model",   model,          MAGENTA, YELLOW,  f"  {model_ico} "))
    _row(_key_val("Mode",    mode,           BLUE,    mode_col,"  "))
    _row(_key_val("Memory",  f"{memory_count} entries", YELLOW, CYAN, "  "))
    _row("")

    print(_mid())

    _row("")
    _row(f"{BOLD}{CYAN}  ◈  API KEYS{RESET}")
    _row("")
    keys_line = "  "
    for name, status in key_status.items():
        keys_line += f"{status} {GRAY}{name}{RESET}   "
    _row(keys_line)
    _row("")

    print(_mid())

    _row("")
    _row(f"{BOLD}{CYAN}  ◈  MODES{RESET}")
    _row("")
    modes = [
        ("1", "Chat AI",       "💬", GREEN),
        ("2", "BrowserOS",     "🌐", CYAN),
        ("3", "Dev Mode",      "⚙️ ", YELLOW),
        ("4", "Memory Viewer", "🧠", MAGENTA),
        ("5", "Settings",      "🔧", BLUE),
    ]
    for i, (key, label, icon, color) in enumerate(modes):
        left  = f"  {BOLD}{color}[{key}]{RESET} {icon}  {color}{label:<15}{RESET}"
        right_mode = modes[i + 1] if i + 1 < len(modes) else None
        if i % 2 == 0 and right_mode:
            rk, rl, ri, rc = right_mode
            right = f"{BOLD}{rc}[{rk}]{RESET} {ri}  {rc}{rl}{RESET}"
            _row(f"{left}   {right}")
        elif i % 2 == 0:
            _row(left)

    _row("")

    print(_mid())

    _row("")
    _row(f"{BOLD}{CYAN}  ◈  COMMANDS{RESET}")
    _row("")
    cmds = [
        ("/exit",   "Quit",           RED),
        ("/help",   "Help menu",      GREEN),
        ("/clear",  "Clear screen",   CYAN),
        ("/model",  "Switch model",   YELLOW),
        ("/mem",    "Memory log",     MAGENTA),
        ("/models", "List models",    BLUE),
        ("/mode",   "Switch mode",    WHITE),
        ("/auto",   "Auto AI route",  GREEN),
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

    _row("")
    print(_bot())
    print()


def models_menu(current="groq"):
    from config import PROVIDERS
    print()
    print(f"  {CYAN}╔{'═' * 44}╗{RESET}")
    title = _center(f"{BOLD}{MAGENTA}✦  AVAILABLE MODELS{RESET}", 44)
    print(f"  {CYAN}║{RESET}{title}{CYAN}║{RESET}")
    print(f"  {CYAN}╠{'═' * 44}╣{RESET}")

    for i, (key, info) in enumerate(PROVIDERS.items(), 1):
        label = info.get("label", key)
        icon  = MODEL_ICONS.get(key, f"{GRAY}●{RESET}")
        mark  = f" {GREEN}← current{RESET}" if key == current else ""
        line  = f"  {BOLD}{CYAN}[{i}]{RESET} {icon}  {WHITE}{label}{RESET}{mark}"
        vis   = len(_strip_ansi(line))
        pad   = " " * max(0, 44 - vis)
        print(f"  {CYAN}║{RESET}{line}{pad}{CYAN}║{RESET}")

    print(f"  {CYAN}╚{'═' * 44}╝{RESET}")
    print()
