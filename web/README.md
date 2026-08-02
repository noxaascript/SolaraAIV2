# SolaraAI Web Workspace

This folder contains the Flask web workspace for SolaraAI.

Run locally:

1. Install the project dependencies:
   `python -m pip install -r requirements.txt`

2. Start the web server:
   `python -m web.app`

3. Open `http://localhost:5000` in your browser.

Notes:
- The endpoint POST /api/chat forwards messages to the existing router (core/router.py).
- `GET /healthz` is available for health checks.
- Set `WEB_ALLOWED_ORIGIN` only when a separate frontend needs browser CORS access.
- Set `HF_API_KEY` in `.env` or the environment to use remote HF inference.
