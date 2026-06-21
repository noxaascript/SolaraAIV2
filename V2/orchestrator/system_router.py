from V2.runtime.executor_bridge import run_core
from V2.runtime.error_hook import handle_error

def start_system(project_folder, main_file, project_files):

    while True:
        try:
            user = input("[Solara V2] $ ")

            if user.lower() in ["exit", "quit"]:
                print("bye 👋")
                break

            result = run_core(user)
            print(result)

        except Exception as e:
            print("[V2 ERROR]")
            handle_error(str(e))
