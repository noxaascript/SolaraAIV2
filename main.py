from ui.boot import boot
from ui.terminal_ui import banner, prompt, chat_ui
from core.router import router


# =========================
# ERROR HANDLER
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
# MAIN LOOP
# =========================

def main():

    # boot sequence
    boot()

    # show banner
    banner()

    print("Solara AI is now online 🔥\n")
    print("Type 'exit' or 'quit' to stop system\n")

    while True:

        # input user
        user_input = prompt("user")

        # exit condition
        if user_input.lower().strip() in ["exit", "quit"]:
            print("\nShutting down Solara AI...")
            break

        # process AI safely
        response = safe_router(user_input)

        # display chat
        chat_ui("user", user_input, response)


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSYSTEM INTERRUPTED (CTRL+C)")
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
