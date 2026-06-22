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

# ── If key still missing, ask once and save it ──
if [ -z "$HF_API_KEY" ]; then
    echo ""
    echo "  First-time setup — enter your HuggingFace API key."
    echo "  Get a free key at: huggingface.co/settings/tokens"
    echo ""
    read -r -p "  HF_API_KEY: " INPUT_KEY
    if [ -z "$INPUT_KEY" ]; then
        echo ""
        echo "  No key entered. Exiting."
        exit 1
    fi
    echo "HF_API_KEY=$INPUT_KEY" > "$DIR/.env"
    export HF_API_KEY="$INPUT_KEY"
    echo ""
    echo "  Key saved to .env — you won't be asked again."
    echo ""
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
