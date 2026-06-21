import sys
from scanner import scan_project
from runner import run_file
from ai import analyze_and_fix
from patcher import apply_patch

def main():
    folder = sys.argv[1]
    file = sys.argv[2]

    print("SCAN PROJECT...")
    files = scan_project(folder)

    print("RUN PROGRAM...\n")
    code, out, err = run_file(file)

    if code == 0:
        print("OK")
        print(out)
        return

    print("ERROR:\n")
    print(err)

    print("\nAI FIXING...\n")
    ai_result = analyze_and_fix(err, files)

    apply_patch(ai_result)

if __name__ == "__main__":
    main()
