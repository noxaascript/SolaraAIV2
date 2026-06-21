from AutoFixer.main import main as auto_fix

retry_count = 0
MAX_RETRY = 2

def handle_error(error_text):
    global retry_count

    print("[V2] Error detected")

    if retry_count >= MAX_RETRY:
        print("[STOP] Max retry reached 💀")
        return

    retry_count += 1

    try:
        auto_fix()
    except Exception as e:
        print("[AutoFixer FAILED]", str(e))
