import os


def clear():
    os.system("clear" if os.name == "posix" else "cls")


def boot_animation():
    clear()
    from ui.terminal_ui import banner
    banner()
