import datetime
import os
import subprocess

def run_tool(text):
    text = text.lower()

    # 🕒 time tool
    if "time" in text:
        return str(datetime.datetime.now())

    # 📁 list files
    if text == "/ls":
        return os.popen("ls").read()

    # 📂 pwd
    if text == "/pwd":
        return os.popen("pwd").read()

    # ⚡ simple shell run
    if text.startswith("/run "):
        cmd = text.replace("/run ", "")
        try:
            return subprocess.getoutput(cmd)
        except:
            return "command failed"

    return None
