import sys
from autofixer.scanner import scan_project
from V2.bootstrap import boot


def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <project_folder> <main_file.py>")
        return

    project_folder = sys.argv[1]
    main_file = sys.argv[2]

    print(f"[MAIN] project: {project_folder}")
    print(f"[MAIN] entry: {main_file}")

    # 🔥 SCAN PROJECT (REAL OUTPUT)
    project_files = scan_project(project_folder)

    print(f"[MAIN] total files: {len(project_files)}")
    print("[MAIN] sample files:")
    print(project_files[:10])  # biar gak spam

    # 🚀 START SYSTEM
    boot(project_folder, main_file, project_files)


if __name__ == "__main__":
    main()
