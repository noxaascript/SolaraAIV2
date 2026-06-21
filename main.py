import sys
import time
from core.router import handle_input

VERSION = "1.0.0"


def banner():
    print("=" * 40)
    print("      SOLARA AI TERMINAL")
    print(f"          v{VERSION}")
    print("=" * 40)
    print("Type 'help' for commands")
    print("Type 'exit' to quit\n")


def loading_effect():
    print("Starting system", end="")
    for _ in range(3):
        time.sleep(0.3)
        print(".", end="")
    print("\n")


def print_help():
    print("""
COMMANDS:
- help   : show commands
- exit   : close program
- clear  : clear screen
- any text -> AI chat
""")


def clear_screen():
    print("\033c", end="")


def safe_input():
    try:
        return input("[user@solara $ ")
    except KeyboardInterrupt:
        print("\nExit signal detected")
        sys.exit(0)


def main():
    loading_effect()
    banner()

    while True:
        user_input = safe_input()

        if not user_input:
            continue

        command = user_input.strip().lower()

        # EXIT
        if command == "exit":
            print("Shutting down...")
            break

        # HELP
        if command == "help":
            print_help()
            continue

        # CLEAR
        if command == "clear":
            clear_screen()
            banner()
            continue

        # PROCESS AI
        try:
            result = handle_input(user_input)

            if result == "__EXIT__":
                print("bye 👋")
                break

            print("\nAI:", result, "\n")

        except Exception as e:
            print(f"[ERROR] {str(e)}")


if __name__ == "__main__":
    main()
