import os
from datetime import datetime

LOG_FILE = "db/logs.txt"

def log(user, bot):
    os.makedirs("db", exist_ok=True)

    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}]\n")
        f.write(f"USER: {user}\n")
        f.write(f"BOT: {bot}\n")
        f.write("-"*30 + "\n")
