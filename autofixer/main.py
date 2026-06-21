import sys
from utils import print_banner
from scanner import scan_project
from runner import run_file
from ai import analyze_and_fix
from patcher import apply_patch

def main():
    print_banner()

    if len(sys.argv) < 3:
        print("Usage: python main.py <project_folder> <main_file>")
        return

    folder = sys.argv[1]
    file = sys.argv[2]

    print("🔍 scanning project...")
    files = scan_project(folder)

    print("🚀 running program...\n")
    code, out, err = run_file(file)

    if code == 0:
        print("OK")
        print(out)
        return

    print("❌ ERROR DETECTED\n")
    print(err)

    print("\n🧠 AI ANALYZING + FIXING...\n")
    ai_result = analyze_and_fix(err, files)

    apply_patch(ai_result)


if __name__ == "__main__":
    main()
