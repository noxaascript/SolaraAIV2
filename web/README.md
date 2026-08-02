# Minimal Web UI for SolaraAI

This folder contains a small Flask app that serves a clean, minimalist web chat UI.

Run locally:

1. Install Flask (if not already):
   pip install Flask

2. Start the web server:
   python web/app.py

3. Open http://localhost:5000 in your browser.

Notes:
- The endpoint POST /api/chat forwards messages to the existing router (core/router.py).
- The web UI prefers local models (transformers) if available; set HF_API_KEY in .env to use remote HF inference.
