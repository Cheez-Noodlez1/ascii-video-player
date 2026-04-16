#!/bin/bash

# ASCII Video Player - Remote Runner
# Usage: curl -sSL https://raw.githubusercontent.com/Cheez-Noodlez1/ascii-video-player/master/run_ascii.sh | bash -s -- <video_url_or_file>

set -e

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

# Temporary directory for execution
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo "--- Setting up ASCII Video Player ---"

# Download the main script and requirements
curl -sSL -O https://raw.githubusercontent.com/Cheez-Noodlez1/ascii-video-player/master/src/main.py
curl -sSL -O https://raw.githubusercontent.com/Cheez-Noodlez1/ascii-video-player/master/requirements.txt

# Install dependencies (using --user to avoid sudo issues)
echo "Installing dependencies..."
pip3 install -r requirements.txt --quiet

# Execute the player in terminal mode
echo "Starting playback..."
python3 main.py "$@" --terminal

# Cleanup
rm -rf "$TEMP_DIR"
