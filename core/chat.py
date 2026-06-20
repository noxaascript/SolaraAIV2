import time
import sys
from core.router import get_response
from core.memory import save_chat
from core.commands import handle_command
from core.tools import run_tool

def stream_text(text):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.005)
    print()

def chat_loop():
    print("SolaraAI Core Mode 🔥 /help")

    while True:
        user = input("you> ")

        # 🧠 command system
        cmd = handle_command(user)
        if cmd:
            if cmd == "exit":
                break
            print("solara>", cmd)
            continue

        # ⚙️ tool system
        tool_result = run_tool(user)
        if tool_result:
            print("solara> ", tool_result)
            save_chat(user, tool_result)
            continue

        # 🤖 AI fallback
        bot = get_response(user)

        print("solara> ", end="")
        stream_text(bot)

        save_chat(user, bot)
