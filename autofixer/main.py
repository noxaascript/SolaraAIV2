import sys
from scanner import scan_project
from runner import run_file
from ai import analyze_and_fix
from patcher import apply_patch

MAX_TRY = 3  # jumlah percobaan auto fix

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <project_folder> <main_file>")
        return

    folder = sys.argv[1]
    file = sys.argv[2]

    print("🔍 scanning project...")
    files = scan_project(folder)

    for i in range(MAX_TRY):
        print(f"\n🚀 RUN #{i+1}")

        code, out, err = run_file(file)

        # kalau sukses
        if code == 0:
            print("✅ CLEAN RUN")
            print(out)
            return

        # kalau error
        print("❌ ERROR DETECTED\n")
        print(err)

        print("\n🧠 AI FIXING...\n")

        # kirim ke AI
        ai_result = analyze_and_fix(err, files)

        # patch file
        apply_patch(ai_result)

    print("\n💀 STOP: MAX TRY REACHED (masih error)")

if __name__ == "__main__":
    main()
