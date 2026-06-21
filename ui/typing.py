import sys
import time


# =========================
# LIVE TYPING EFFECT
# =========================
def type_text(text, speed=0.02):

    if text is None:
        text = ""

    text = str(text)

    for char in text:

        sys.stdout.write(char)
        sys.stdout.flush()

        time.sleep(speed)

    print("\n")


# =========================
# AI TYPING WRAPPER
# =========================
def ai_type(text):

    print("\nAI: ", end="")

    type_text(text, speed=0.01)
