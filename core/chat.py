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
        user = input("you> ")

        if user == "/exit":
            break

        result = route(user)

        print("solara> ", end="")
        stream(result)

        save_chat(user, str(result))
