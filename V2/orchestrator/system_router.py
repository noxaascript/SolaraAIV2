from V2.runtime.executor_bridge import run_core

def start_system(project_folder, main_file, project_files):
    print("[ROUTER] active")

    return run_core(project_folder, main_file, project_files)
