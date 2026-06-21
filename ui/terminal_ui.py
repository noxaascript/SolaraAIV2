import os
import time


def clear():
    os.system("clear")


def banner():

    print("""
╔════════════════════════════╗
║       SOLARA AI OS         ║
║   Dev + Browser System     ║
╚════════════════════════════╝
""")


def prompt(user="user"):

    return input(f"[{user}@solara] $ ")


def loading(text="loading"):

    print(f"{text}...")

    time.sleep(0.5)

def chat_ui(user, message, response):
    print()
    print(f"👤 You: {message}")
    print()
    print("🤖 Solara:")
    print(response)
    print()
