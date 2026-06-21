import os

def scan_project(folder):
    files = []

    for root, _, fns in os.walk(folder):
        for f in fns:
            if f.endswith(".py"):
                path = os.path.join(root, f)

                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()

                files.append({
                    "path": path,
                    "content": content
                })

    return files
