from core.router import route
from core.memory import save_chat, init_db
import time

init_db()


def stream(text):
    for c in str(text):
        print(c, end="", flush=True)
        time.sleep(0.004)
    print()


def chat_loop():
    print("SolaraAI Hybrid Core 🔥")

    while True:
        user = input("you> ")

        if user == "/exit":
            break

        result = route(user)

        print("solara> ", end="")
        stream(result)

        save_chat(user, str(result))
