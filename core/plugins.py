import os
import importlib

PLUGINS = {}

def load_plugins():
    for file in os.listdir("plugins"):
        if file.endswith(".py"):
            name = file[:-3]
            module = importlib.import_module(f"plugins.{name}")

            if hasattr(module, "run"):
                PLUGINS[name] = module.run

def run_plugin(name, text):
    if name in PLUGINS:
        return PLUGINS[name](text)
    return None
