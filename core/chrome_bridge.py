import requests


def send_to_chrome(action, data=None):
    """
    Bridge ke Chrome Extension Local Server
    """

    try:
        payload = {
            "action": action,
            "data": data
        }

        # Chrome extension local endpoint (harus dibuat extension sendiri)
        res = requests.post(
            "http://localhost:8765/chrome",
            json=payload,
            timeout=5
        )

        return res.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
