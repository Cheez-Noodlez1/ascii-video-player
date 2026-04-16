# ASCII Video Player 🎬

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

A retro-style Windows application that converts any video file or HTML file into real-time ASCII art. Watch your favorite movies, clips, or home videos rendered in a grid of text characters with synchronized audio support, or view HTML content directly in your terminal.

---

## ✨ Features

- **Real-time ASCII Conversion:** High-performance conversion of video frames into ASCII characters based on luminance.
- **HTML Support:** Render HTML files directly into ASCII text for a unique terminal viewing experience.
- **Terminal Mode:** Run the tool entirely in the terminal without a GUI for quick previews.
- **Multiple Color Modes:**
  - 🟢 **Matrix Green:** The classic "hacker" aesthetic.
  - ⚪ **Grayscale:** Traditional high-contrast black and white.
  - 🌈 **True Color:** Modern full-color rendering using HTML spans.
- **Audio Synchronization:** Integrated audio playback synced with the ASCII stream.
- **User-Friendly Interface:** Drag-and-drop support and a clean, minimalist UI built with PyQt6.
- **Standalone Executable:** Portable single-file EXE for easy distribution.

---

## 🚀 Quick Start & Installation

### 💻 For Windows Users
1. Clone the repository:
   ```bash
   git clone https://github.com/Cheez-Noodlez1/ascii-video-player.git
   cd ascii-video-player
   ```
2. Double-click **`ASCIIPlayer.bat`** to run directly or use **`INSTALL_WINDOWS.bat`** to add it to your system PATH.
3. You can now run the player from any terminal using:
   ```bash
   ASCIIPlayer.bat movie.mp4 --terminal
   ```

### 🐧 For Linux Users
1. Clone the repository:
   ```bash
   git clone https://github.com/Cheez-Noodlez1/ascii-video-player.git
   cd ascii-video-player
   ```
2. Run the installer:
   ```bash
   chmod +x install_linux.sh
   ./install_linux.sh
   ```
3. Alternatively, run the tool with the install flag:
   ```bash
   python3 src/main.py --install
   ```
4. Restart your terminal and type:
   ```bash
   ascii-player movie.mp4 --terminal
   ```

### ⚡ Run Instantly with curl (No Installation)
```bash
curl -sSL https://raw.githubusercontent.com/Cheez-Noodlez1/ascii-video-player/master/run_ascii.sh | bash -s -- https://example.com
```

---

## 📖 Detailed Installation & Troubleshooting
For more in-depth instructions, platform-specific details, and common troubleshooting tips, please refer to our **[Installation & Troubleshooting Guide](INSTALL_GUIDE.md)**.

---

## 🛠️ Building the Standalone EXE

We provide a convenient build script for Windows:

1. Double-click **`BUILD_ASCII.bat`**.
2. The script will automatically:
   - Verify your Python installation.
   - Install required build tools (`PyInstaller`).
   - Package the application into a single file.
3. Find your standalone program in the **`dist/`** folder as `ASCIIPlayer.exe`.

---

## 💻 Command Line Usage

Launch the player directly from your terminal with arguments:

```bash
# Basic usage (defaults to Matrix Green)
ASCIIPlayer.exe movie.mp4

# Full Color mode
ASCIIPlayer.exe movie.mp4 true

# Terminal mode (for videos or HTML)
ASCIIPlayer.exe movie.mp4 --terminal
ASCIIPlayer.exe index.html --terminal

# 🛠️ Install to system PATH automatically
python src/main.py --install

# 🚀 Run instantly with curl (no installation needed)
# For local files:
curl -sSL https://raw.githubusercontent.com/Cheez-Noodlez1/ascii-video-player/master/run_ascii.sh | bash -s -- movie.mp4

# For remote HTML pages:
curl -sSL https://raw.githubusercontent.com/Cheez-Noodlez1/ascii-video-player/master/run_ascii.sh | bash -s -- https://example.com
```

**Pro Tip:** Rename the EXE to `ascii-stream.exe` and add it to your System PATH to use it from anywhere!

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## 🛡️ Privacy & Security

- **100% Local:** All video processing is performed locally on your machine.
- **No Data Collection:** We do not collect, store, or transmit any user data or video content.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Credits

- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - Professional UI framework.
- [OpenCV](https://opencv.org/) - Industry-standard computer vision library.
- [PyInstaller](https://pyinstaller.org/) - Reliable application packaging.
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing and audio extraction.
