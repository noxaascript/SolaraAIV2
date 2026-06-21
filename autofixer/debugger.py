from autofixer.ai import ask_ai
from error_db import quick_hint

def debug_error(error_text, project_files):
    
    hint = quick_hint(error_text)

    context = ""

    # ambil 3 file pertama biar AI ngerti struktur
    for f in project_files[:3]:
        context += f"\nFILE: {f['file']}\n{f['content'][:1000]}\n"

    ai_result = ask_ai(error_text + "\n\nHINT: " + hint, context)

    return ai_result
