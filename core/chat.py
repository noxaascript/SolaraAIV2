from core.router import handle_input as route
from core.memory import save_chat

import time


def stream(text):
    for c in str(text):
        print(c, end="", flush=True)
        time.sleep(0.004)
    print()


def chat_loop():
    print("SolaraAI Workspace Mode 🔥")

    while True:
        try:
            user = input("you> ")
        except (KeyboardInterrupt, EOFError):
            print("\n[EXIT] Bye.")
            break

        if user.strip().lower() in ("/exit", "exit", "quit"):
            print("Shutting down...")
            break

        result = route(user)

        # handle router exit sentinel
        if result == "__EXIT__":
            print("solara> Goodbye.")
            break

        # ensure we print a string and avoid mixing prints during streaming
        result_text = str(result) if result is not None else "No response."

        print("solara> ", end="")
        stream(result_text)

        try:
            save_chat(user, result_text)
        except Exception:
            # don't crash the chat loop if saving fails
            pass
