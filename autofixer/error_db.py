COMMON_ERRORS = {
    "ModuleNotFoundError": "Kamu belum install library (pip install ...)",
    "IndentationError": "Python error karena spasi/tab berantakan",
    "SyntaxError": "Ada kode yang typo atau kurang tanda (:, ) , dll)",
    "TypeError": "Tipe data salah (string vs int vs dict)",
    "KeyError": "Key dictionary tidak ada",
    "AttributeError": "Object tidak punya attribute yang dipanggil",
    "IndexError": "List index keluar batas",
    "ValueError": "Nilai input tidak sesuai format"
}

def quick_hint(error_text):
    for key in COMMON_ERRORS:
        if key in error_text:
            return COMMON_ERRORS[key]

    return "Error tidak dikenal, butuh AI analysis"
