@echo off
rem = """
setlocal enabledelayedexpansion

:: Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

:: Install dependencies if missing (optional but helpful for standalone feel)
:: python -m pip install PyQt6 opencv-python numpy moviepy pygame html2text requests --quiet

:: Run this file as a Python script
python "%~f0" %*
exit /b %errorlevel%

:: Python code starts here
"""

import sys
import os

# Re-importing the core logic from main.py if available, 
# or we can embed the entire main.py content here for a truly single-file experience.
# For a professional repo, we'll keep the src/main.py but make this BAT a "smart launcher".

try:
    # Add src to path to find main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(script_dir, "src"))
    
    from main import main
    if __name__ == "__main__":
        main()
except ImportError:
    print("[ERROR] Could not find src/main.py. Please ensure you are running this from the repository root.")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] An unexpected error occurred: {e}")
    sys.exit(1)
