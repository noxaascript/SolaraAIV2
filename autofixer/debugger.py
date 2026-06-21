from ai import ask_ai

def debug_error(error_text):
    if not error_text:
        return "No error detected"

    return ask_ai(error_text)
