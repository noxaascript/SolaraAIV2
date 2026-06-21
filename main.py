from ui.boot_anim import boot_animation
from ui.boot import boot
from ui.terminal_ui import banner, prompt, chat_ui
from core.router import router


# =========================
# SAFE ROUTER WRAPPER
# =========================

def safe_router(user_input):
    try:
        response = router(user_input)

        if response is None:
            return "EMPTY_RESPONSE"

        return response

    except Exception as e:
        return f"SYSTEM ERROR: {str(e)}"


# =========================
# MAIN SYSTEM LOOP
# =========================

def main():

    # 1. animated boot
    boot_animation()

    # 2. system check boot (optional tambahan)
    boot()

    # 3. show banner
    banner()

    print("\nSOLARA AI V2 ONLINE ✔")
    print("Type 'exit' or 'quit' to shutdown system\n")

    # =========================
    # CHAT LOOP
    # =========================

    while True:

        # input user
        user_input = prompt("user")

        # exit condition
        if user_input.lower().strip() in ["exit", "quit"]:
            print("\nShutting down Solara AI...")
            break

        # process AI safely
        response = safe_router(user_input)

        # output chat
        chat_ui("user", user_input, response)


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSYSTEM STOPPED (CTRL+C)")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
