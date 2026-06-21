from scanner import scan_project
from runner import run_file
from ai import analyze_and_fix
from patcher import apply_patch

def main():
    folder = "AutoFixer/project"
    file = "AutoFixer/project/main.py"

    print("[AutoFixer] scanning...")

    files = scan_project(folder)

    print("[AutoFixer] running...")

    code, out, err = run_file(file)

    if code == 0:
        print("OK")
        return

    print("[ERROR DETECTED]")
    print(err)

    print("[AI FIXING...]")

    fix = analyze_and_fix(err, files)

    apply_patch(fix)

    print("[RETRY...]")

    run_file(file)
