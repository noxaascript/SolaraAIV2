"""Runtime-only Hugging Face credentials for interactive users.

Project-wide persistence belongs in Replit Secrets. User-entered keys are kept
only in memory so they are not written to users.json or chat history.
"""

_USER_KEYS = {}


def set_user_key(user_id, key):
    key = str(key or "").strip()
    if not key.startswith("hf_") or len(key) < 10:
        return False
    _USER_KEYS[str(user_id)] = key
    return True


def get_user_key(user_id):
    return _USER_KEYS.get(str(user_id), "")


def has_user_key(user_id):
    return bool(get_user_key(user_id))


def clear_user_key(user_id):
    _USER_KEYS.pop(str(user_id), None)