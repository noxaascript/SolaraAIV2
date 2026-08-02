#!/usr/bin/env bash
# SolaraAI V2 — Launcher (non-interactive by default)
# Works on Termux, Linux, macOS
# Just run:  bash start.sh

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# ── Load .env file if it exists ──
if [ -f "$DIR/.env" ]; then
    set -a
    source "$DIR/.env"
    set +a
fi

# ── Optional interactive HF_API_KEY setup ──
# If HF_API_KEY is missing and we're running in a TTY, ask the user once.
if [ -z "$HF_API_KEY" ] && [ -t 0 ]; then
    echo ""
    echo "If you want run this ai, We reccomended to use HF API Key, YES/NO"
    read -r -p "Configure HF_API_KEY now? [y/N]: " ANSWER
    case "$ANSWER" in
        [Yy]* )
            read -r -p "Enter HF_API_KEY: " INPUT_KEY
            if [ -n "$INPUT_KEY" ]; then
                echo "HF_API_KEY=$INPUT_KEY" > "$DIR/.env"
                export HF_API_KEY="$INPUT_KEY"
                echo "HF_API_KEY saved to .env"
            else
                echo "No key entered — continuing without HF_API_KEY."
            fi
            ;;
        * )
            echo "Continuing without HF_API_KEY..."
            ;;
    esac
fi

# If still missing, show a non-fatal warning
if [ -z "$HF_API_KEY" ]; then
    echo ""
    echo "  [WARN] HF_API_KEY is not set — the system will prefer local transformers if available."
    echo "         To use the Hugging Face Inference API set HF_API_KEY in .env or the environment."
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

# ── Install / update dependencies ──
# First try normally (works on WiFi / fixed SSL).
# If that fails (common on Termux mobile data with broken SSL certs),
# retry with --trusted-host to bypass SSL verification for pip itself.
if [ -f "$DIR/requirements.txt" ]; then
    echo "  Checking dependencies..."
    if $PYTHON -m pip install -q -r "$DIR/requirements.txt"; then
        echo "  Dependencies OK."
    else
        echo "  Normal install failed — retrying with SSL bypass (Termux fix)..."
        $PYTHON -m pip install -q \
            --trusted-host pypi.org \
            --trusted-host pypi.python.org \
            --trusted-host files.pythonhosted.org \
            -r "$DIR/requirements.txt" \
        && echo "  Dependencies installed (SSL bypassed)." \
        || echo "  [warn] Could not install all packages. If chat fails, run:"
        echo "         pip install requests --trusted-host pypi.org --trusted-host files.pythonhosted.org"
    fi
fi

# ── Launch ──
echo ""
$PYTHON "$DIR/main.py" "$@"
