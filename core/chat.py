from core.router import route
from core.memory import save_chat
from core.plugins import load_plugins
from core.logs import log

import time, sys

load_plugins()

def stream(text):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(0.005)
    print()

def chat_loop():
    print("SolaraAI Core v2 🔥")

    while True:
        user = input("you> ")

        if user == "/exit":
            break

        result = route(user)

        print("solara> ", end="")
        stream(str(result))

        save_chat(user, str(result))
        log(user, result)
