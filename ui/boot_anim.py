import time
import sys
import os

FRAMES = [
"""
███████╗
██╔════╝
██║     
██║     
███████╗
╚══════╝
""",
"""
███████╗ ██████╗
██╔════╝██╔═══██╗
██║     ██║   ██║
██║     ██║   ██║
███████╗╚██████╔╝
╚══════╝ ╚═════╝
""",
"""
███████╗ ██████╗ ██╗
██╔════╝██╔═══██╗██║
██║     ██║   ██║██║
██║     ██║   ██║██║
███████╗╚██████╔╝███████╗
╚══════╝ ╚═════╝ ╚══════╝
""",
"""
███████╗ ██████╗ ██╗     █████╗
██╔════╝██╔═══██╗██║    ██╔══██╗
██║     ██║   ██║██║    ███████║
██║     ██║   ██║██║    ██╔══██║
███████╗╚██████╔╝███████╗██║  ██║
╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""
]

def clear():
    os.system("clear" if os.name == "posix" else "cls")


def boot_animation():
    clear()
    print("BOOTING SOLARA AI V2...\n")

    for frame in FRAMES:
        clear()
        print(frame)
        print("\nINITIALIZING SYSTEM...")
        time.sleep(0.5)

    clear()
    print(FRAMES[-1])
    print("\nSYSTEM ONLINE ✔")
    time.sleep(1)
