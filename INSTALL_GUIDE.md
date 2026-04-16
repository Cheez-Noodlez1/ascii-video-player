# 🛠️ ASCII Video Player: Installation & Troubleshooting Guide

Welcome to the official installation guide for the **ASCII Video Player**. This document provides detailed instructions for setting up the tool on various platforms, using different methods, and resolving common issues.

---

## 🚀 Installation Methods

### 1. Windows Installation (Recommended)
The Windows installer is designed to be a "one-click" solution that handles dependency management and system integration.

**Steps:**
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Cheez-Noodlez1/ascii-video-player.git
    cd ascii-video-player
    ```
2.  **Run the Installer:**
    Double-click `INSTALL_WINDOWS.bat` or run it from your terminal.
3.  **Verification:**
    Open a **new** terminal window (CMD or PowerShell) and type:
    ```bash
    ascii-player --version
    ```

### 2. Linux Installation
The Linux installer supports both `bash` and `zsh` environments and sets up a local binary for global access.

**Steps:**
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Cheez-Noodlez1/ascii-video-player.git
    cd ascii-video-player
    ```
2.  **Make the Script Executable:**
    ```bash
    chmod +x install_linux.sh
    ```
3.  **Run the Installer:**
    ```bash
    ./install_linux.sh
    ```
4.  **Verification:**
    Restart your terminal or run `source ~/.bashrc` (or `source ~/.zshrc`), then type:
    ```bash
    ascii-player --version
    ```

### 3. Universal Python Installation (`--install` flag)
If you already have Python and the repository cloned, you can trigger the installation directly from the script.

**Steps:**
```bash
python src/main.py --install
```
*Note: This will automatically detect your OS and launch the appropriate installer script.*

### 4. Zero-Installation Method (`curl`)
Perfect for quick previews or when you don't want to clone the repository.

**Steps:**
```bash
curl -sSL https://raw.githubusercontent.com/Cheez-Noodlez1/ascii-video-player/master/run_ascii.sh | bash -s -- <file_or_url>
```

---

## 🛠️ Troubleshooting

### 1. `ascii-player` command not found
**Symptoms:** You receive an error stating `'ascii-player' is not recognized as an internal or external command`.

**Solutions:**
-   **Restart your terminal:** Changes to the `PATH` variable only take effect in new terminal sessions.
-   **Manual PATH Check (Windows):** Ensure `%USERPROFILE%\.ascii-video-player` is in your User Environment Variables.
-   **Manual PATH Check (Linux):** Ensure `$HOME/.local/bin` is in your `PATH`. Check your `.bashrc` or `.zshrc` for the export line.

### 2. Missing Dependencies (OpenCV, PyQt6, etc.)
**Symptoms:** The tool fails to start with an `ImportError`.

**Solutions:**
-   **Re-run the installer:** The installers are designed to be idempotent and will attempt to fix missing dependencies.
-   **Manual Install:**
    ```bash
    pip install -r requirements.txt
    ```
-   **Linux Specific:** Some Linux distributions require additional system libraries for OpenCV. You may need to install `libgl1`:
    ```bash
    sudo apt-get update && sudo apt-get install libgl1
    ```

### 3. Audio is not playing
**Symptoms:** Video plays in ASCII, but there is no sound.

**Solutions:**
-   **Check `moviepy` and `pygame`:** These are required for audio extraction and playback.
-   **Permissions:** Ensure the tool has permission to write a temporary `temp_audio.wav` file in its execution directory.

### 4. `curl` method fails on Windows
**Symptoms:** Running the `curl` command in CMD or PowerShell results in errors.

**Solutions:**
-   The `curl | bash` method is primarily designed for **Linux** and **macOS** (or Windows with Git Bash/WSL).
-   For native Windows users, please use the `INSTALL_WINDOWS.bat` method.

---

## 📞 Further Support
If you encounter an issue not covered here, please [open an issue](https://github.com/Cheez-Noodlez1/ascii-video-player/issues) on GitHub with a detailed description of your problem and your system environment.
