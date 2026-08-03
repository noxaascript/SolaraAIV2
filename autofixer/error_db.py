# error_db.py - simple error hint system

ERROR_MAP = {
    "ModuleNotFoundError": "cek apakah file/module sudah ada atau salah import path",
    "ImportError": "nama function/variable tidak ada di file target",
    "KeyError": "cek key di dict config/provider",
    "SyntaxError": "ada typo atau format Python salah",
    "AttributeError": "object tidak punya attribute yang dipanggil"
}

def quick_hint(error_msg: str):
    for key in ERROR_MAP:
        if key in error_msg:
            return f"[HINT] {ERROR_MAP[key]}"
    return "[HINT] unknown error, cek struktur project"
