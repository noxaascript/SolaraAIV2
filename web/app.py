from flask import Flask, render_template, request, jsonify
import os

from core.error_utils import format_error
from core.router import handle_input as route

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.after_request
def add_cors_headers(response):
    allowed_origin = os.environ.get("WEB_ALLOWED_ORIGIN", "").strip()
    if allowed_origin:
        response.headers["Access-Control-Allow-Origin"] = allowed_origin
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok", "service": "solaraai-web"})


@app.route("/api/chat", methods=["POST"])
def api_chat():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": format_error(400, "Invalid JSON payload")}), 400
        message = data.get("message", "")
        if not isinstance(message, str) or message.strip() == "":
            return jsonify({"error": format_error(400, "Empty message")}), 400

        try:
            result = route(message)
        except Exception as e:
            return jsonify({"error": format_error(500, str(e))}), 500

        # Handle exit sentinel
        if result == "__EXIT__":
            return jsonify({"message": "Goodbye.", "exit": True})

        return jsonify({
            "message": str(result),
            "exit": False,
            "command": message.startswith("/"),
        })

    except Exception as e:
        return jsonify({"error": format_error(502, str(e))}), 502


if __name__ == "__main__":
    port = int(os.environ.get("WEB_PORT", 5000))
    debug = os.environ.get("WEB_DEBUG", "0").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)
