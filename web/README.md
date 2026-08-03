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
- Set `HF_API_KEY=hf_...` in `.env` or export it in the same shell that starts
  the app. `HF_TOKEN` and `HUGGINGFACEHUB_API_TOKEN` are also supported.
- All seven listed models use the shared `HF_API_KEY=hf_...` flow.
- The model IDs can be overridden with their corresponding model environment
  variables, such as `KIMI_MODEL`, `LLAMA_MODEL`, or `DEEPSEEK_MODEL`.
- Hugging Face keys must be active and have Inference Providers permission.
