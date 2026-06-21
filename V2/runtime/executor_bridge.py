def run_core(project_folder, main_file, project_files):
    print("[EXECUTOR] running")

    return {
        "project": project_folder,
        "main": main_file,
        "files": len(project_files)
    }
