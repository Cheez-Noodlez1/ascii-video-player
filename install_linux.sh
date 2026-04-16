#!/bin/bash

# ASCII Video Player - Professional Linux Installer
# Usage: ./install_linux.sh

set -e

echo "============================================================"
echo "  ASCII Video Player - Installation Wizard (Linux)"
echo "============================================================"
echo.

# 1. Check for Python
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed. Please install it first."
    exit 1
fi

# 2. Install dependencies
echo "[1/4] Installing required Python packages..."
python3 -m pip install --upgrade pip --quiet
python3 -m pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies. Check your internet connection."
    exit 1
fi
echo "[OK] Dependencies installed."

# 3. Create a permanent installation directory
INSTALL_DIR="$HOME/.local/bin"
echo "[2/4] Setting up installation directory at $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

# 4. Create a system-wide launcher
echo "[3/4] Creating system launcher..."
cat <<EOF > "$INSTALL_DIR/ascii-player"
#!/bin/bash
python3 "$HOME/.local/share/ascii-video-player/main.py" "\$@"
EOF
chmod +x "$INSTALL_DIR/ascii-player"

# Copy the source code to a permanent location
mkdir -p "$HOME/.local/share/ascii-video-player"
cp src/main.py "$HOME/.local/share/ascii-video-player/main.py"

# 5. Add to User PATH
echo "[4/4] Verifying PATH..."
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "Adding $INSTALL_DIR to PATH in your .bashrc/.zshrc..."
    echo "export PATH=\$PATH:$INSTALL_DIR" >> "$HOME/.bashrc"
    if [ -f "$HOME/.zshrc" ]; then
        echo "export PATH=\$PATH:$INSTALL_DIR" >> "$HOME/.zshrc"
    fi
    echo "[OK] PATH updated. Please restart your terminal or run 'source ~/.bashrc'."
else
    echo "[OK] $INSTALL_DIR is already in your PATH."
fi

echo.
echo "============================================================"
echo "  INSTALLATION COMPLETE!"
echo "============================================================"
echo.
echo "You can now run the player from ANY terminal using:"
echo "   ascii-player <video_file_or_url> [--terminal]"
echo.
echo "Enjoy the retro vibes!"
echo.
