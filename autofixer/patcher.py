from backup import backup_file

def apply_patch(output):
    blocks = output.split("FILE:")

    for b in blocks:
        if "CODE:" not in b:
            continue

        try:
            path = b.split("\n")[0].strip()
            code = b.split("CODE:")[1].strip()

            # 🔥 BACKUP DULU
            backup_file(path)

            # lalu patch
            with open(path, "w", encoding="utf-8") as f:
                f.write(code)

            print("✔ FIXED:", path)

        except Exception as e:
            print("PATCH ERROR:", e)
