import sys
import os

from ui.boot_anim   import boot_animation
from ui.terminal_ui import (
    clear, banner, prompt, chat_ui, help_menu,
    status_line, model_switched, section_banner
)
from ui.dashboard   import dashboard, models_menu
from ui.typing      import ai_type, user_echo, error_msg, success_msg, system_msg
from ui.spinner     import Spinner, SPINNER_DOTS, SPINNER_ORBIT
from ui.colors      import CYAN, MAGENTA, YELLOW, GREEN, GRAY, RED, WHITE, RESET, BOLD, DIM
from providers.router import run_ai, list_providers
from config import PROVIDERS, DEFAULT_PROVIDER


# ──────────────────────────────────────────────
# /ping — test internet + HuggingFace connection
# ──────────────────────────────────────────────

def cmd_ping():
    import socket
    import requests
    from config import HF_API_KEY

    print(f"\n  {BOLD}{CYAN}◈  CONNECTION CHECK{RESET}")
    print(f"  {GRAY}{'─' * 44}{RESET}\n")

    checks = []

    # 1. Internet (DNS) — try multiple hosts so one blocked domain doesn't
    #    falsely report "no internet" on mobile networks
    sp = Spinner("Internet (DNS)", style=SPINNER_ORBIT, color=CYAN)
    sp.start()
    _dns_hosts = ["huggingface.co", "cloudflare.com", "google.com"]
    _connected = False
    socket.setdefaulttimeout(5)
    for _host in _dns_hosts:
        try:
            socket.getaddrinfo(_host, 443)
            _connected = True
            break
        except Exception:
            continue
    if _connected:
        sp.stop(success=True, msg="Internet   ✔  connected")
        checks.append(True)
    else:
        sp.stop(success=False, msg="Internet   ✖  no connection — check WiFi/data")
        checks.append(False)

    # 2. HuggingFace reachable
    sp = Spinner("HuggingFace API", style=SPINNER_ORBIT, color=MAGENTA)
    sp.start()
    try:
        r = requests.get("https://huggingface.co", timeout=8)
        if r.status_code < 400:
            sp.stop(success=True, msg="HuggingFace  ✔  reachable")
            checks.append(True)
        else:
            sp.stop(success=False, msg=f"HuggingFace  ✖  HTTP {r.status_code}")
            checks.append(False)
    except requests.exceptions.ConnectionError:
        sp.stop(success=False, msg="HuggingFace  ✖  unreachable")
        checks.append(False)
    except Exception as e:
        sp.stop(success=False, msg=f"HuggingFace  ✖  {str(e)[:40]}")
        checks.append(False)

    # 3. API key valid
    sp = Spinner("API key", style=SPINNER_ORBIT, color=YELLOW)
    sp.start()
    if not HF_API_KEY:
        sp.stop(success=False, msg="API key      ✖  not set")
        checks.append(False)
    else:
        try:
            r = requests.get(
                "https://huggingface.co/api/whoami-v2",
                headers={"Authorization": f"Bearer {HF_API_KEY}"},
                timeout=8,
            )
            if r.status_code == 200:
                name = r.json().get("name", "unknown")
                sp.stop(success=True, msg=f"API key      ✔  valid  ({name})")
                checks.append(True)
            elif r.status_code == 401:
                sp.stop(success=False, msg="API key      ✖  invalid — get one at huggingface.co/settings/tokens")
                checks.append(False)
            else:
                sp.stop(success=False, msg=f"API key      ✖  HTTP {r.status_code}")
                checks.append(False)
        except Exception:
            sp.stop(success=False, msg="API key      ✖  could not verify (no internet?)")
            checks.append(False)

    print(f"\n  {GRAY}{'─' * 44}{RESET}")
    if all(checks):
        print(f"  {BOLD}{GREEN}✔  All systems go — ready to chat!{RESET}\n")
    else:
        print(f"  {BOLD}{RED}✖  Some checks failed — see above.{RESET}\n")


# ──────────────────────────────────────────────
# COMMAND HANDLERS
# ──────────────────────────────────────────────

def handle_model_switch(state):
    models_menu(current=state["model"])
    keys = list(PROVIDERS.keys())
    try:
        choice = input(
            f"  {CYAN}Enter model name or number (1–{len(keys)}): {RESET}"
        ).strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                old = state["model"]
                state["model"] = keys[idx]
                model_switched(old, state["model"])
            else:
                error_msg(f"Invalid number. Choose 1–{len(keys)}.")
        elif choice in PROVIDERS:
            old = state["model"]
            state["model"] = choice
            model_switched(old, state["model"])
        elif choice:
            error_msg(f"Unknown model: '{choice}'")
    except (KeyboardInterrupt, EOFError):
        pass


# ──────────────────────────────────────────────
# MAIN CHAT LOOP
# ──────────────────────────────────────────────

def chat_loop(state):
    username = state.get("user", "user")

    while True:
        try:
            raw = prompt(user=username, model=state["model"], mode=state["mode"])
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n  {DIM}{GRAY}Session ended. Goodbye. ✦{RESET}\n")
            break

        text = raw.strip()
        if not text:
            continue

        # ── commands ──
        if text in ("/exit", "exit", "quit"):
            print(f"\n  {DIM}{GRAY}Goodbye. ✦{RESET}\n")
            break

        elif text in ("/help", "help"):
            help_menu()

        elif text == "/ping":
            cmd_ping()

        elif text == "/dash":
            clear()
            dashboard(
                user=username,
                model=state["model"],
                memory_count=state.get("memory_count", 0),
                mode=state["mode"],
            )

        elif text == "/clear":
            clear()
            banner()

        elif text == "/model":
            handle_model_switch(state)

        elif text == "/models":
            models_menu(current=state["model"])

        elif text == "/mem":
            section_banner("Memory Log", color=MAGENTA)
            try:
                from core.memory import get_history
                history = get_history()
                if history:
                    for entry in history[-10:]:
                        print(f"  {GRAY}· {entry}{RESET}")
                else:
                    system_msg("No memory entries yet.")
            except Exception as e:
                system_msg(f"Memory unavailable: {e}")

        elif text == "/multi":
            from providers.multi_model import multi_chat, print_multi_results
            keys = list(PROVIDERS.keys())
            print(f"\n  MULTI-MODEL COMPARE")
            print(f"  {'-' * 40}")
            for i, k in enumerate(keys, 1):
                label = PROVIDERS[k].get("label", k)
                print(f"  [{i}]  {k:<12}  {label}")
            print(f"  {'-' * 40}")
            try:
                sel = input("  Select models (e.g. 1,2,3 or all): ").strip()
                if sel.lower() == "all":
                    chosen = keys
                else:
                    chosen = []
                    for part in sel.split(","):
                        part = part.strip()
                        if part.isdigit():
                            idx = int(part) - 1
                            if 0 <= idx < len(keys):
                                chosen.append(keys[idx])
                        elif part in PROVIDERS:
                            chosen.append(part)
                if not chosen:
                    system_msg("No valid models selected.")
                else:
                    q = input("  Prompt: ").strip()
                    if q:
                        sp = Spinner(f"Querying {len(chosen)} models", style=SPINNER_DOTS)
                        sp.start()
                        results = multi_chat(q, chosen)
                        sp.stop(success=True, msg=f"Done — {len(results)} responses")
                        print_multi_results(q, results)
            except (KeyboardInterrupt, EOFError):
                pass

        elif text == "/auto":
            state["auto"] = not state.get("auto", False)
            status = "ON" if state["auto"] else "OFF"
            system_msg(f"Smart auto-routing: {status}")

        elif text == "/mode":
            modes = ["chat", "dev", "browser", "auto"]
            print(f"\n  {GRAY}Available modes:{RESET} {', '.join(modes)}")
            m = input(f"  {CYAN}Choose mode: {RESET}").strip()
            if m in modes:
                state["mode"] = m
                success_msg(f"Mode → {m}")
            else:
                error_msg(f"Unknown mode: '{m}'")

        else:
            # ── AI call ──
            sp = Spinner("Thinking", style=SPINNER_DOTS, color=MAGENTA)
            sp.start()

            if state.get("auto"):
                from providers.smart_router import auto_chat
                response, used_model = auto_chat(text, user_id=username)
                sp.stop(success=True, msg=f"Done  [{used_model}]")
            else:
                response = run_ai(state["model"], text)
                sp.stop(success=True, msg="Done")

            ai_type(response, label="Solara")

            try:
                from core.memory import save_chat
                save_chat(text, str(response))
                state["memory_count"] = state.get("memory_count", 0) + 1
            except Exception:
                pass


# ──────────────────────────────────────────────
# ENTRY POINTS
# ──────────────────────────────────────────────

def run_autofixer(project_folder, main_file):
    from autofixer.scanner import scan_project
    from V2.bootstrap      import boot
    print(f"  {CYAN}[AUTOFIXER]{RESET} Scanning: {project_folder}")
    project_files = scan_project(project_folder)
    boot(project_folder, main_file, project_files)


def main():
    # ── autofixer mode: python main.py <folder> <file> ──
    if len(sys.argv) == 3:
        run_autofixer(sys.argv[1], sys.argv[2])
        return

    # ── interactive AI mode ──
    boot_animation()

    dashboard(user="user", model=DEFAULT_PROVIDER, memory_count=0, mode="chat")

    state = {
        "user":         "user",
        "model":        DEFAULT_PROVIDER,
        "mode":         "chat",
        "memory_count": 0,
        "auto":         False,
    }

    chat_loop(state)


if __name__ == "__main__":
    main()
