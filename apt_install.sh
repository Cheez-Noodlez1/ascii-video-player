#!/bin/bash

# ASCII Video Player - APT Installer Script
# Usage: curl -sSL https://raw.githubusercontent.com/Cheez-Noodlez1/ascii-video-player/master/apt_install.sh | sudo bash

set -e

echo "============================================================"
echo "  ASCII Video Player - APT Installation (Linux)"
echo "============================================================"
echo.

# 1. Check for sudo
if [ "$EUID" -ne 0 ]; then
    echo "[ERROR] Please run this script with sudo."
    exit 1
fi

# 2. Download the Debian package
echo "[1/3] Downloading the latest Debian package..."
PACKAGE_URL="https://github.com/Cheez-Noodlez1/ascii-video-player/raw/master/pkg/ascii-stream_1.2.0_all.deb"
wget -q -O /tmp/ascii-stream.deb "$PACKAGE_URL"

# 3. Install the package using apt
echo "[2/3] Installing ascii-stream via APT..."
apt-get update -qq
apt-get install -y /tmp/ascii-stream.deb

# 4. Clean up
rm /tmp/ascii-stream.deb

echo.
echo "============================================================"
echo "  INSTALLATION COMPLETE!"
echo "============================================================"
echo.
echo "You can now use the following command from any terminal:"
echo "   ascii-stream <video_file_or_url> [--terminal] [--stream]"
echo.
echo "Enjoy the retro vibes!"
echo.
