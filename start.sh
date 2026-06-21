#!/usr/bin/env bash
# ─────────────────────────────────────────────
#  Solara AI V2 — Launcher
#  Works on Termux, Linux, macOS
#  Just run:  bash start.sh
# ─────────────────────────────────────────────

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# ── HuggingFace API key (pre-configured) ──
export HF_API_KEY="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"

# ── activate venv if present ──
if [ -f "$DIR/venv/bin/activate" ]; then
    source "$DIR/venv/bin/activate"
fi

# ── find Python ──
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

# ── install deps on first run ──
if [ -f "$DIR/requirements.txt" ]; then
    $PYTHON -m pip install -q -r "$DIR/requirements.txt" 2>/dev/null || true
fi

# ── launch ──
$PYTHON "$DIR/main.py" "$@"
