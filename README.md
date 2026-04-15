# ASCII Video Player — Standalone Windows App

A retro-style Windows application that converts any video file into real-time ASCII art. Watch your favorite movies, clips, or home videos rendered in a grid of text characters!

---

## Features

- **Real-time ASCII Conversion:** Converts video frames into a grid of ASCII characters based on brightness levels.
- **Multiple Color Modes:** Toggle between:
  - **Matrix Green:** Classic hacker aesthetic.
  - **Grayscale:** Traditional black and white.
  - **Full Color:** For a more modern look.
- **Drag and Drop:** Simply drag any video file onto the window to start playing.
- **Supported Formats:** Works with `.mp4`, `.avi`, `.mov`, `.mkv`, and more.
- **Standalone EXE:** Once built, it's a single file you can move anywhere.

---

## How to Build the EXE

1.  Extract this folder on your Windows machine.
2.  Ensure **Python 3.8 or later** is installed ([python.org](https://www.python.org/downloads/)).
3.  Double-click **`BUILD_ASCII.bat`**.
4.  Wait for the build process to complete (this will install `PyQt6`, `OpenCV`, and `PyInstaller` automatically).
5.  Once finished, your standalone program will be in the **`dist/`** folder as `ASCIIPlayer.exe`.

---

## How to Use

- **Drag and Drop:** Drag a video file into the app.
- **"Open Video" Button:** Select a file using the Windows file explorer.
- **"Switch Color" Button:** Toggle through the different color modes.

---

## Pro Command Line Usage 💻

You can launch the player directly from your terminal (CMD or PowerShell) using the built-in command line arguments:

```bash
# Basic usage (defaults to Matrix Green)
ASCIIPlayer.exe movie.mp4

# Full Color mode (just add 'true')
ASCIIPlayer.exe movie.mp4 true
```

### **To use it as `ascii-stream` from anywhere:**
1.  Open the folder containing your built `ASCIIPlayer.exe`.
2.  Rename the file to `ascii-stream.exe`.
3.  Add the folder to your **Windows Environment Variables (PATH)**.
4.  Now you can type `ascii-stream video.mp4 true` from any terminal!

---

## Requirements (for building only)

- **Windows 10 or 11**
- **Python 3.8+**
- **Internet Connection** (to download `OpenCV` and `PyQt6` during the build)

---

## Privacy

All processing is done **100% locally** on your machine. No videos are ever uploaded to any server.

---

## Credits

- Built with **PyQt6** and **OpenCV**.
- Packaged with **PyInstaller**.
