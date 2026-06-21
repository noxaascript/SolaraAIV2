from AutoFixer.main import main as auto_fix

def handle_error(error_text):
    print("[V2] Error detected → AutoFixer running...")

    try:
        auto_fix()
    except Exception as e:
        print("[AutoFixer FAILED]", str(e))
