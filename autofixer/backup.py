import shutil
import os
import time

BACKUP_DIR = "AutoFixer/backups"

def backup_file(path):
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    if not os.path.exists(path):
        return

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = path.replace("/", "_")

    backup_path = f"{BACKUP_DIR}/{filename}_{timestamp}.bak"

    shutil.copy2(path, backup_path)

    return backup_path
