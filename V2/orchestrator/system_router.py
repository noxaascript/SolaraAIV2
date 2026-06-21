from V2.runtime.executor_bridge import run_core
from V2.runtime.error_hook import handle_error
from V2.plugins.plugin_loader import load_plugins

def start_system():
    print("[V2] System Router Online")

    load_plugins()

    while True:
        try:
            user = input("[Solara V2] $ ")

            if user.lower() in ["exit", "quit"]:
                print("bye 👋")
                break

            result = run_core(user)
            print(result)

        except Exception as e:
            handle_error(str(e))
