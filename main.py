import sys
import os

from ui.boot_anim   import boot_animation
from ui.terminal_ui import (
    clear, banner, prompt, chat_ui, help_menu,
    status_line, model_switched, section_banner
)
from ui.dashboard   import dashboard, models_menu
from ui.typing      import ai_type, user_echo, error_msg, success_msg, system_msg
from ui.spinner     import Spinner, SPINNER_DOTS
from ui.colors      import CYAN, MAGENTA, YELLOW, GREEN, GRAY, RED, WHITE, RESET, BOLD, DIM
from providers.router import run_ai, list_providers
from config import PROVIDERS, DEFAULT_PROVIDER


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

        elif text == "/auto":
            state["auto"] = not state.get("auto", False)
            status = f"{GREEN}ON{RESET}" if state["auto"] else f"{RED}OFF{RESET}"
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
    clear()
    boot_animation()
    clear()

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
