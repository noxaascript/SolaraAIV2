from ui.terminal_ui import clear, banner, prompt
from ui.dashboard import dashboard
from ui.chat_ui import chat_ui
from ui.loader import loading

from core.router import route


# =========================
# MAIN SOLARA AI OS
# =========================
def main():

    clear()
    banner()

    print("System initializing...\n")

    while True:

        # HOME DASHBOARD
        dashboard()

        # USER INPUT
        user_input = prompt("user")

        # EXIT HANDLER
        if user_input.lower() in ["exit", "quit", "/exit"]:
            print("\nShutting down Solara AI OS...")
            break

        if user_input.strip() == "":
            continue

        # LOADING EFFECT
        loading("SolaraAI processing")

        # ROUTER (AI + COMMAND SYSTEM)
        response = route(user_input, user_id="user")

        # CHAT OUTPUT UI
        chat_ui("user", user_input, response)

        print("\n")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
