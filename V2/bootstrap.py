def boot(project_folder, main_file, project_files):
    print("[BOOT] starting system...")

    from V2.orchestrator.system_router import start_system
    return start_system(project_folder, main_file, project_files)
