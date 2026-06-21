from Core import router
from V2.runtime.error_hook import handle_error
from V2.runtime.executor_bridge import run_core

def start_system():
    print("[V2] System Router Online")

    while True:
        try:
            user_input = input("[Solara V2] $ ")

            if user_input.lower() in ["exit", "quit"]:
                print("shutting down...")
                break

            # kirim ke core system lama
            result = run_core(user_input)

            print(result)

        except Exception as e:
            print("[V2 ERROR DETECTED]")
            handle_error(str(e))
