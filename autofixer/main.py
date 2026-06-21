import sys
from runner import run_file
from debugger import debug_error

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py target.py")
        return

    file = sys.argv[1]

    code, out, err = run_file(file)

    if code == 0:
        print("✅ OK RUN")
        print(out)
    else:
        print("❌ ERROR DETECTED\n")
        print(err)

        print("\n🤖 AI FIX:\n")
        print(debug_error(err))


if __name__ == "__main__":
    main()
