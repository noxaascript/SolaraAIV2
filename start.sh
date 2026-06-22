#!/usr/bin/env bash
# ─────────────────────────────────────────────
#  Solara AI V2 — Launcher
#  Works on Termux, Linux, macOS
#  Just run:  bash start.sh
# ─────────────────────────────────────────────

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# ── Load .env file if it exists (takes priority) ──
if [ -f "$DIR/.env" ]; then
    set -a
    source "$DIR/.env"
    set +a
fi

# ── Fallback: use built-in key if .env didn't set one ──
if [ -z "$HF_API_KEY" ]; then
    export HF_API_KEY="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"
fi

# ── Activate venv if present ──
if [ -f "$DIR/venv/bin/activate" ]; then
    source "$DIR/venv/bin/activate"
fi

# ── Find Python ──
if command -v python &>/dev/null; then
    PYTHON="python"
elif command -v python3 &>/dev/null; then
    PYTHON="python3"
else
    echo "[ERROR] Python not found."
    echo "  Termux: pkg install python"
    echo "  Linux:  sudo apt install python3"
    exit 1
fi

# ── Install deps on first run ──
if [ -f "$DIR/requirements.txt" ]; then
    $PYTHON -m pip install -q -r "$DIR/requirements.txt" 2>/dev/null || true
fi

# ── Launch ──
$PYTHON "$DIR/main.py" "$@"
