#!/bin/bash

# ASCII Video Player - Professional Linux Installer (Sudo Mode)
# Usage: sudo ./install_linux.sh

set -e

echo "============================================================"
echo "  ASCII Video Player - Installation Wizard (Linux Sudo)"
echo "============================================================"
echo.

# 1. Check for Sudo
if [ "$EUID" -ne 0 ]; then
    echo "[WARNING] This installer is not running with sudo/root privileges."
    echo "To install system-wide (Global), please run this script with sudo."
    echo "Proceeding with User-level installation..."
    IS_SUDO=0
else
    echo "[OK] Running with administrative privileges."
    IS_SUDO=1
fi

# 2. Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed. Please install it first."
    exit 1
fi

# 3. Install dependencies
echo "[1/4] Installing required Python packages..."
python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies. Check your internet connection."
    exit 1
fi
echo "[OK] Dependencies installed."

# 4. Set Installation Paths
if [ "$IS_SUDO" -eq 1 ]; then
    INSTALL_DIR="/usr/local/bin"
    SHARE_DIR="/usr/local/share/ascii-video-player"
else
    INSTALL_DIR="$HOME/.local/bin"
    SHARE_DIR="$HOME/.local/share/ascii-video-player"
fi

echo "[2/4] Setting up installation directories..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$SHARE_DIR"

# 5. Create a system-wide launcher
echo "[3/4] Creating system launcher..."
cat <<EOF > "$INSTALL_DIR/ascii-player"
#!/bin/bash
python3 "$SHARE_DIR/main.py" "\$@"
EOF
chmod +x "$INSTALL_DIR/ascii-player"

# Copy the source code to a permanent location
cp src/main.py "$SHARE_DIR/main.py"

# 6. Verify PATH
echo "[4/4] Verifying PATH..."
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    if [ "$IS_SUDO" -eq 0 ]; then
        echo "Adding $INSTALL_DIR to PATH in your .bashrc/.zshrc..."
        echo "export PATH=\$PATH:$INSTALL_DIR" >> "$HOME/.bashrc"
        if [ -f "$HOME/.zshrc" ]; then
            echo "export PATH=\$PATH:$INSTALL_DIR" >> "$HOME/.zshrc"
        fi
        echo "[OK] User PATH updated. Please restart your terminal."
    else
        echo "[INFO] System PATH should already include $INSTALL_DIR."
    fi
else
    echo "[OK] $INSTALL_DIR is already in your PATH."
fi

echo.
echo "============================================================"
echo "  INSTALLATION COMPLETE!"
echo "============================================================"
echo.
echo "You can now run the player from ANY terminal using:"
echo "   ascii-player <video_file_or_url> [--terminal] [--stream]"
echo.
echo "Enjoy the retro vibes!"
echo.
