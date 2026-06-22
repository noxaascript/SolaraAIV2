#!/usr/bin/env bash
# ─────────────────────────────────────────────
#  Solara AI V2 — Launcher
#  Works on Termux, Linux, macOS
#  Just run:  bash start.sh
# ─────────────────────────────────────────────

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# ── Load .env file if it exists ──
if [ -f "$DIR/.env" ]; then
    set -a
    source "$DIR/.env"
    set +a
fi

# ── Check key is set ──
if [ -z "$HF_API_KEY" ]; then
    echo ""
    echo "  ✖  HF_API_KEY not set."
    echo ""
    echo "  Run this once to save your key:"
    echo "    echo 'HF_API_KEY=your_key_here' > .env"
    echo ""
    echo "  Get a free key at: huggingface.co/settings/tokens"
    echo ""
    exit 1
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
