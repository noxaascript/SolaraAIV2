import os

PLUGIN_FOLDER = "V2/plugins"

def load_plugins():
    print("[V2] Loading plugins...")

    try:
        files = os.listdir(PLUGIN_FOLDER)

        for f in files:
            if f.endswith(".py") and f != "plugin_loader.py":
                print("[PLUGIN LOADED]", f)

    except Exception as e:
        print("[PLUGIN ERROR]", str(e))
