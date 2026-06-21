import sys
from autofixer.scanner import scan_project
from V2.bootstrap import boot


def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <project_folder> <main_file.py>")
        return

    project_folder = sys.argv[1]
    main_file = sys.argv[2]

    print("[MAIN] starting")

    project_files = scan_project(project_folder)

    boot(project_folder, main_file, project_files)


if __name__ == "__main__":
    main()
