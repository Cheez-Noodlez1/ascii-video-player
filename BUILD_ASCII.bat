@echo off
title ASCII Video Player - EXE Builder
echo ============================================================
echo   ASCII Video Player - EXE Builder
echo ============================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo.
    echo Please install Python 3.8 or later from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found. Starting build...
echo.

:: Run the packager script
python "%~dp0setup_ascii.py"

if errorlevel 1 (
    echo.
    echo Build encountered an error. See messages above.
    pause
    exit /b 1
)

echo.
echo Done! Your standalone ASCIIPlayer.exe is in the 'dist' folder.
echo.
pause >nul
