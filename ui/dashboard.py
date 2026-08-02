import time
import re


def _strip_ansi(s):
    return re.sub(r'\033\[[0-9;]*m', '', s)


def dashboard(user="user", model="qwen", memory_count=0, mode="chat"):
    from config import HF_API_KEY
    from ui.colors import CYAN, MAGENTA, YELLOW, GREEN, RED, GRAY, RESET, BOLD, DIM
    
    hf_color = GREEN if HF_API_KEY else RED
    hf_status = f"{hf_color}● {RESET}{BOLD}{hf_color}{'ACTIVE' if HF_API_KEY else 'MISSING'}{RESET}"
    now = time.strftime("%H:%M:%S")
    
    W = 52
    inner_W = 48
    
    def _pad_line(left_content, width=inner_W):
        visual_len = len(_strip_ansi(left_content))
        padding = width - visual_len
        if padding < 0:
            return left_content
        return left_content + " " * padding

    def print_row(content):
        padded = _pad_line(content, inner_W)
        print(f"  {BOLD}{CYAN}│{RESET}  {padded}  {BOLD}{CYAN}│{RESET}")

    border_top = f"  {BOLD}{CYAN}╭{'─' * W}╮{RESET}"
    border_mid = f"  {BOLD}{CYAN}├{'─' * W}┤{RESET}"
    border_bot = f"  {BOLD}{CYAN}╰{'─' * W}╯{RESET}"
    
    # Define row content
    row1 = f"{BOLD}{YELLOW}USER:{RESET} {user:<8}  {BOLD}{MAGENTA}MODE:{RESET} {mode:<6}  {BOLD}{GREEN}TIME:{RESET} {now}"
    row2 = f"{BOLD}{CYAN}MODEL:{RESET} {model:<14}  {BOLD}{YELLOW}API KEY:{RESET} {hf_status}"
    row3 = f"{DIM}{GRAY}Type {CYAN}/help{GRAY} for list of commands | Ctrl+C to exit{RESET}"
    
    print(border_top)
    print_row(row1)
    print_row(row2)
    print(border_mid)
    print_row(row3)
    print(border_bot)
    print()


def models_menu(current="qwen"):
    from config import PROVIDERS
    from ui.colors import CYAN, YELLOW, GRAY, GREEN, RESET, BOLD, DIM
    print(f"\n  {BOLD}{CYAN}◈  AVAILABLE MODELS{RESET}")
    print(f"  {DIM}{GRAY}{'─' * 52}{RESET}")
    for i, (key, info) in enumerate(PROVIDERS.items(), 1):
        label = info.get("label", key)
        if key == current:
            mark = f"  {BOLD}{GREEN}✔ current{RESET}"
            color = GREEN
            bold_key = f"{BOLD}{GREEN}{key:<12}{RESET}"
        else:
            mark = ""
            color = GRAY
            bold_key = f"{CYAN}{key:<12}{RESET}"
        print(f"  {BOLD}{color}[{i:>2}]{RESET}  {bold_key}  {GRAY}{label:<30}{RESET}{mark}")
    print(f"  {DIM}{GRAY}{'─' * 52}{RESET}\n")
