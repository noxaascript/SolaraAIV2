import shutil
import time

def backup_file(path):
    try:
        backup_path = path + ".bak_" + str(int(time.time()))
        shutil.copy(path, backup_path)
        return backup_path
    except:
        return None
