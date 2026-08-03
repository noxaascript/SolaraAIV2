from autofixer.scanner import scan_project
from runner import run_file
from ai import analyze_and_fix
from patcher import apply_patch
from rollback import rollback_latest

def main():
    folder = "AutoFixer/project"
    file = "AutoFixer/project/main.py"

    print("[AutoFixer SAFE MODE]")

    files = scan_project(folder)

    code, out, err = run_file(file)

    if code == 0:
        print("[OK]")
        return

    print("[ERROR]", err)

    fix = analyze_and_fix(err, files)

    apply_patch(fix)

    print("[RETRY RUN]")

    code2, out2, err2 = run_file(file)

    # 🔁 kalau masih error → rollback
    if code2 != 0:
        print("[FAILED AGAIN → ROLLBACK]")
        rollback_latest()
