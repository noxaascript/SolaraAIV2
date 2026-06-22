import sys
import time


def type_text(text, speed=0.018, newline=True):
    if text is None:
        text = ""
    text = str(text)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    if newline:
        print()
    sys.stdout.flush()


def ai_type(text, label="Solara"):
    print(f"\n  {label} :")
    print(f"  {'-' * 50}")
    print(f"  {str(text).strip()}")
    print(f"  {'-' * 50}")


def user_echo(text, username="You"):
    print(f"\n  {username} > {text}")
    print(f"  {'-' * 50}")


def system_msg(text):
    print(f"\n  [system] {text}")


def error_msg(text):
    print(f"\n  [error]  {text}")


def success_msg(text):
    print(f"\n  [ok]     {text}")
