#!/data/data/com.termux/files/usr/bin/bash

set -e

# =========================
# UI FUNCTION (ANIMATION)
# =========================
animate_text() {
    text="$1"
    echo ""
    for ((i=0; i<${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep 0.03
    done
    echo ""
}

loading_bar() {
    echo -n "["
    for i in {1..20}; do
        echo -n "█"
        sleep 0.05
    done
    echo "]"
}

# =========================
# START
# =========================
clear
echo "======================================"
echo "      SOLARA AI OS INSTALLER"
echo "======================================"

# =========================
# 1. UPDATE SYSTEM
# =========================
echo "[1/6] Updating system..."
pkg update -y && pkg upgrade -y

# =========================
# 2. INSTALL PACKAGES
# =========================
echo "[2/6] Installing base packages..."
pkg install -y python git nano

# =========================
# ANIMATED TEXT (REQUESTED)
# =========================
animate_text "Installing Additional Packages"
loading_bar

pkg install -y clang make openssl

# =========================
# 3. PROJECT SETUP
# =========================
echo "[3/6] Setting up SolaraAI OS..."
mkdir -p SolaraAI
cd SolaraAI

# =========================
# 4. VENV
# =========================
echo "[4/6] Creating environment..."
python -m venv venv
source venv/bin/activate

# =========================
# 5. PYTHON LIBS
# =========================
echo "[5/6] Installing AI libraries..."
pip install --upgrade pip
pip install fastapi uvicorn flask requests transformers python-dotenv

# =========================
# 6. CREATE STRUCTURE
# =========================
echo "[6/6] Building system files..."

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

# boot anim
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
        time.sleep(0.7)
EOF

# start.sh (AUTO RUN TARGET)
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
# FINAL BOOT SEQUENCE
# =========================
echo ""
animate_text "Finalizing Installation..."
loading_bar

sleep 1

clear
echo "======================================"
echo "     SOLARA AI OS INSTALL COMPLETE"
echo "======================================"
echo ""

# =========================
# AUTO RUN start.sh (REQUESTED)
# =========================
animate_text "Launching Solara AI OS..."
sleep 1

bash start.sh
