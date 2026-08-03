SETTINGS = {
    "user_agent": "SolaraAI BrowserOS V2",
    "timeout": 10,
    "max_tabs": 10,
    "download_folder": "downloads",
    "history_limit": 1000,
    "safe_mode": True
}


def get(key):
    return SETTINGS.get(key)


def set(key, value):
    SETTINGS[key] = value
    return f"{key} updated"
