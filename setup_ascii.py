import os
import sys
import subprocess

def package_ascii():
    """
    Package the ASCII Video Player into a standalone Windows EXE.
    """
    print("=" * 60)
    print("  ASCII Video Player - EXE Packager")
    print("=" * 60)

    # 1. Install PyInstaller and dependencies
    print("\n[1/3] Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller", "PyQt6", "opencv-python", "numpy", "moviepy", "pygame"])
        print("  Packages installed successfully.")
    except Exception as e:
        print(f"  Error: {e}")
        return False

    # 2. Build EXE
    print("\n[2/3] Building ASCIIPlayer.exe...")
    script_path = os.path.join("src", "main.py")
    
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "ASCIIPlayer",
        script_path
    ]

    try:
        subprocess.check_call(cmd)
        print("  Build successful!")
    except Exception as e:
        print(f"  Build failed: {e}")
        return False

    # 3. Finalize
    print("\n[3/3] Finalizing...")
    exe_path = os.path.join("dist", "ASCIIPlayer.exe")
    if os.path.exists(exe_path):
        print(f"  Your standalone program is ready at: {exe_path}")
    
    print("\nDone!")
    return True

if __name__ == "__main__":
    package_ascii()
