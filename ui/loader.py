import time
import sys


def loading(text="Processing", speed=0.3):

    print(text, end="")

    for _ in range(3):

        time.sleep(speed)

        print(".", end="")

        sys.stdout.flush()

    print("\n")
