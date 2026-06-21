import os
import shutil

def rollback_latest():
    backup_dir = "AutoFixer/backups"

    files = sorted(os.listdir(backup_dir))

    if not files:
        print("[ROLLBACK] No backup found")
        return

    latest = files[-1]
    backup_path = os.path.join(backup_dir, latest)

    original_name = latest.split("_")[0].replace("_", "/")

    shutil.copy2(backup_path, original_name)

    print("[ROLLBACK DONE]", original_name)
