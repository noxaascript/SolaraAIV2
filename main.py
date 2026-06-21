import sys
from autofixer.runner import run_file
from autofixer.scanner import scan_project
from debugger import debug_error
from V2.bootstrap import boot
def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <project_folder> <main_file.py>")
        return

    project_folder = sys.argv[1]
    target_file = sys.argv[2]

    print("🔍 Scanning project...")
    project_files = scan_project(project_folder)

    print("🚀 Running file...\n")

    code, out, err = run_file(target_file)

    if code == 0:
        print("✅ RUN SUCCESS")
        print(out)
    else:
        print("❌ ERROR DETECTED\n")
        print(err)

        print("\n🤖 AI MULTI-FILE ANALYSIS:\n")
        result = debug_error(err, project_files)
        print(result)


if __name__ == "__main__":
    main()
