import os

def scan_project(project_folder):
    files = []

    for root, _, filenames in os.walk(project_folder):
        for f in filenames:
            files.append(os.path.join(root, f))

    print(f"[SCANNER] {len(files)} files found")
    return files
