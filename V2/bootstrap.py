from V2.orchestrator.system_router import start_system

def boot(project_folder, main_file, project_files):
    print("[BOOT] active")

    return start_system(project_folder, main_file, project_files)
