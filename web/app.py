from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
import base64
import hashlib
import os
import secrets
import urllib.parse
import requests

from core.code_output import OUTPUT_DIR
from config import hf_key_configured, PROVIDERS
from core.hf_credentials import clear_user_key, has_user_key, set_user_key
from core.error_utils import format_error
from core.router import handle_input as route

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("SESSION_SECRET") or secrets.token_hex(32)


def _web_user_id():
    if session.get("auth_user", {}).get("id"):
        return f"supabase:{session['auth_user']['id']}"
    if "user_id" not in session:
        session["user_id"] = secrets.token_urlsafe(18)
    return session["user_id"]


def _supabase_configured():
    return bool(os.environ.get("SUPABASE_URL", "").strip() and
                _supabase_key())


def _supabase_key():
    return (
        os.environ.get("SUPABASE_ANON_KEY", "").strip()
        or os.environ.get("SUPABASE_PUBLISHABLE_KEY", "").strip()
    )


def _redirect_uri():
    configured = os.environ.get("SUPABASE_REDIRECT_URI", "").strip()
    return configured or url_for("auth_callback", _external=True)


@app.route("/auth/login")
def auth_login():
    if not _supabase_configured():
        return jsonify({"error": "Supabase is not configured"}), 503
    verifier = secrets.token_urlsafe(48)
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).rstrip(b"=").decode()
    state = secrets.token_urlsafe(32)
    session["oauth_verifier"] = verifier
    session["oauth_state"] = state
    params = urllib.parse.urlencode({
        "provider": "google",
        "redirect_to": _redirect_uri(),
        "code_challenge": challenge,
        "code_challenge_method": "s256",
        "state": state,
    })
    return redirect(f"{os.environ['SUPABASE_URL'].rstrip('/')}/auth/v1/authorize?{params}")


@app.route("/auth/callback")
def auth_callback():
    error = request.args.get("error_description") or request.args.get("error")
    if error:
        return redirect(url_for("index", auth_error=error))
    if request.args.get("state") != session.pop("oauth_state", None):
        return jsonify({"error": "Invalid OAuth state"}), 400
    code = request.args.get("code")
    verifier = session.pop("oauth_verifier", None)
    if not code or not verifier or not _supabase_configured():
        return jsonify({"error": "Incomplete Supabase login response"}), 400
    try:
        response = requests.post(
            f"{os.environ['SUPABASE_URL'].rstrip('/')}/auth/v1/token",
            params={"grant_type": "pkce"},
            headers={"apikey": _supabase_key()},
            json={"auth_code": code, "code_verifier": verifier},
            timeout=15,
        )
        if response.status_code != 200:
            return redirect(url_for("index", auth_error="Google login could not be completed"))
        payload = response.json()
        user = payload.get("user") or {}
        if not user.get("id"):
            return redirect(url_for("index", auth_error="Supabase returned no user"))
        session["auth_user"] = {
            "id": user["id"],
            "email": user.get("email", ""),
            "name": (user.get("user_metadata") or {}).get("full_name")
                    or (user.get("user_metadata") or {}).get("name")
                    or user.get("email", "User"),
        }
        return redirect(url_for("index"))
    except requests.RequestException:
        return redirect(url_for("index", auth_error="Supabase is unreachable"))


@app.route("/auth/logout")
def auth_logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/api/me")
def api_me():
    user = session.get("auth_user")
    return jsonify({"authenticated": bool(user), "user": user})

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


@app.route("/api/status")
def api_status():
    return jsonify({
        "status": "ok",
        "supabase_configured": _supabase_configured(),
        "authenticated": bool(session.get("auth_user")),
        "huggingface_key_configured": hf_key_configured() or has_user_key(_web_user_id()),
        "models": [
            {"id": key, "label": value["label"], "model": value["model"]}
            for key, value in PROVIDERS.items()
        ],
    })


@app.route("/api/hf-key", methods=["POST", "DELETE"])
def web_hf_key():
    user_id = _web_user_id()
    if request.method == "DELETE":
        clear_user_key(user_id)
        return jsonify({"ok": True, "message": "Hugging Face key cleared for this session."})

    data = request.get_json(silent=True) or {}
    key = data.get("key", "")
    if not isinstance(key, str) or not set_user_key(user_id, key):
        return jsonify({"ok": False, "error": "Enter a valid Hugging Face token beginning with hf_."}), 400
    return jsonify({"ok": True, "message": "Hugging Face key connected for this session."})


@app.route("/api/generated-files/<path:filename>")
def generated_file(filename):
    """Download only files created under generated_code/."""
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


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
            provider = data.get("provider", "qwen")
            model = data.get("model") or None
            if provider not in PROVIDERS:
                return jsonify({"error": format_error(400, "Unsupported model selection")}), 400
            result = route(message, user_id=_web_user_id(), provider=provider, model=model)
        except Exception as e:
            return jsonify({"error": format_error(500, str(e))}), 500

        # Handle exit sentinel
        if result == "__EXIT__":
            return jsonify({"message": "Goodbye.", "exit": True})

        payload = {
            "message": str(result),
            "exit": False,
            "command": message.startswith("/"),
        }
        marker = "Saved coded file: generated_code/"
        if marker in str(result):
            filename = str(result).split(marker, 1)[1].splitlines()[0].strip()
            payload["generated_file"] = {
                "name": filename,
                "url": f"/api/generated-files/{filename}",
            }
        return jsonify(payload)

    except Exception as e:
        return jsonify({"error": format_error(502, str(e))}), 502


if __name__ == "__main__":
    port = int(os.environ.get("WEB_PORT", 5000))
    debug = os.environ.get("WEB_DEBUG", "0").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug, use_reloader=False)
