from backup import backup_file
from config import SAFE_MODE
from backup import backup_file

def apply_patch(output):
    blocks = output.split("FILE:")

    for b in blocks:
        if "CODE:" not in b:
            continue

        try:
            path = b.split("\n")[0].strip()
            code = b.split("CODE:")[1].strip()

            # 🔒 SAFE MODE (preview dulu)
            if SAFE_MODE:
                print("\n🧠 SAFE MODE ON")
                print("FILE:", path)
                print("PREVIEW PATCH:\n")
                print(code[:500])
                print("\n-----------------\n")
                continue

            # 🔥 backup sebelum overwrite
            backup_file(path)

            # tulis file fix
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)

            print("✔ FIXED:", path)

        except Exception as e:
            print("PATCH ERROR:", e)
