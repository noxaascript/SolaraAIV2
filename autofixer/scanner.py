import os

def scan_project(project_folder):
    files = []

    for root, dirs, filenames in os.walk(project_folder):
        for f in filenames:
            path = os.path.join(root, f)
            files.append(path)

    print(f"[SCANNER] found {len(files)} files")
    return files
