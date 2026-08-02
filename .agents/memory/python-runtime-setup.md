---
name: Python runtime setup
description: The web app needs the full Python tools module and declared dependencies to run in Replit workflows.
---

Use the standard Python tools runtime rather than a minimal base-only runtime when starting the Flask web app. The app depends on Flask, requests, python-dotenv, and beautifulsoup4.

**Why:** The minimal runtime has no usable pip/package environment, which makes an otherwise valid workflow fail before importing the app.

**How to apply:** If the web workflow reports a missing Python package, verify the active runtime module before changing application code.