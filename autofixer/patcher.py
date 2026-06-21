from backup import backup_file

SAFE_MODE = True

def apply_patch(output):
    blocks = output.split("FILE:")

    for b in blocks:
        if "CODE:" not in b:
            continue

        path = b.split("\n")[0].strip()
        code = b.split("CODE:")[1].strip()

        print("[PATCH TARGET]", path)

        # 🛡 backup dulu
        backup = backup_file(path)
        print("[BACKUP CREATED]", backup)

        # 🧪 SAFE MODE (tidak langsung overwrite kalau ON)
        if SAFE_MODE:
            print("\n[SAFE MODE ACTIVE]")
            print("PREVIEW ONLY:\n")
            print(code[:600])
            print("\n--------------------")
            continue

        # kalau OFF baru nulis
        with open(path, "w", encoding="utf-8") as f:
            f.write(code)

        print("[FIXED]", path)
