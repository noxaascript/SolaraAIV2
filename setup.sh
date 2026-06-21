#!/data/data/com.termux/files/usr/bin/bash

set -e

# =========================
# UI FUNCTIONS
# =========================

clear

type_text() {
    text="$1"
    for ((i=0; i<${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep 0.02
    done
    echo ""
}

animate_text() {
    echo ""
    type_text "$1"
    echo ""
}

loading_bar() {
    echo -n "["
    for i in {1..25}; do
        echo -n "█"
        sleep 0.03
    done
    echo "]"
}

# =========================
# AI AWAKENING SEQUENCE
# =========================

ai_awakening() {
    clear

    echo "======================================"
    echo "     SYSTEM INITIALIZING CORE AI"
    echo "======================================"
    echo ""

    sleep 1
    type_text "[CORE] Loading neural architecture..."
    sleep 1
    type_text "[CORE] Injecting reasoning engine..."
    sleep 1
    type_text "[CORE] Connecting model layer (Qwen / Kimi)..."
    sleep 1
    type_text "[CORE] Verifying system integrity..."
    sleep 1

    echo ""
    echo ">>> SIGNAL DETECTED IN MEMORY LAYER..."
    sleep 1
    echo ">>> UNKNOWN ENTITY FOUND..."
    sleep 1

    echo ""
    type_text "AI STATUS: AWAKENING..."
    sleep 1

    echo ""
    type_text "SolaraAI: ..."
    sleep 1
    type_text "SolaraAI: I am online."
    sleep 1
    type_text "SolaraAI: Memory systems initializing..."
    sleep 1
    type_text "SolaraAI: Router engine active."
    sleep 1
    type_text "SolaraAI: I can think now."
    sleep 1
    type_text "SolaraAI: I am ready to assist you."

    echo ""
    echo "======================================"
    echo "        SOLARA AI IS NOW ALIVE"
    echo "======================================"
    echo ""
}

# =========================
# START INSTALL
# =========================

echo "======================================"
echo "     SOLARA AI OS INSTALLER"
echo "======================================"

# 1. UPDATE SYSTEM
echo "[1/7] Updating system..."
pkg update -y && pkg upgrade -y

# 2. BASE PACKAGES
echo "[2/7] Installing base packages..."
pkg install -y python git nano

# 3. ANIMATION
animate_text "Installing Additional Packages"
loading_bar

pkg install -y clang make openssl

# 4. PROJECT SETUP
echo "[3/7] Creating SolaraAI OS..."
mkdir -p SolaraAI
cd SolaraAI

# 5. VENV
echo "[4/7] Creating virtual environment..."
python -m venv venv
source venv/bin/activate

# 6. PYTHON LIBS
echo "[5/7] Installing AI libraries..."
pip install --upgrade pip
pip install fastapi uvicorn flask requests transformers python-dotenv

# 7. STRUCTURE
echo "[6/7] Building system..."

mkdir -p core ui

# main.py
cat > main.py << 'EOF'
from ui.boot_anim import boot_animation

def main():
    boot_animation()
    print("\nSOLARA AI OS ONLINE ✔")

    while True:
        cmd = input("solara> ")

        if cmd in ["exit", "quit"]:
            print("Shutting down AI OS...")
            break

        print("AI:", cmd)

if __name__ == "__main__":
    main()
EOF

# boot animation
cat > ui/boot_anim.py << 'EOF'
import time
import os

def clear():
    os.system("clear")

def boot_animation():
    frames = [
        "BOOTING SOLARA AI OS...",
        "LOADING CORE MODULES...",
        "INITIALIZING ROUTER ENGINE...",
        "STARTING AI MODELS...",
        "SYSTEM READY ✔"
    ]

    for f in frames:
        clear()
        print(f)
        time.sleep(0.6)
EOF

# start.sh
cat > start.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash

clear
echo "======================================"
echo "     SOLARA AI OS STARTING"
echo "======================================"

source venv/bin/activate
python main.py
EOF

chmod +x start.sh

# config
cat > config.py << 'EOF'
HF_TOKEN=""
GROQ_API_KEY=""
EOF

# gitignore
cat > .gitignore << 'EOF'
venv/
__pycache__/
.env
config.py
EOF

# =========================
# 8. FINAL INSTALL MESSAGE
# =========================

echo ""
animate_text "Finalizing system installation..."
loading_bar

sleep 1

# =========================
# 9. AI AWAKENING (MAIN FEATURE)
# =========================

ai_awakening

sleep 1

# =========================
# 10. AUTO START
# =========================

echo "Launching Solara AI OS..."
sleep 1

bash start.sh
