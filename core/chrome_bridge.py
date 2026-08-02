"""Optional bridge for a local Chrome companion.

The bridge is deliberately best-effort: the main assistant remains usable when
the browser companion is not installed or running.
"""

import json
import os
import urllib.request

from core.error_utils import format_error


def send_to_chrome(action, data=None):
    url = os.environ.get("SOLARAAI_CHROME_BRIDGE_URL", "http://127.0.0.1:8765/action")
    payload = json.dumps({"action": action, "data": data or {}}).encode("utf-8")
    request = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return {"status": "error", "message": format_error(502, str(exc))}