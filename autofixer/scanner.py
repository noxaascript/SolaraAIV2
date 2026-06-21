import os

def scan_project(folder):
    files_data = []

    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)

                try:
                    with open(path, "r", encoding="utf-8") as file:
                        content = file.read()

                    files_data.append({
                        "file": path,
                        "content": content
                    })

                except Exception as e:
                    files_data.append({
                        "file": path,
                        "content": f"ERROR READ FILE: {str(e)}"
                    })

    return files_data
