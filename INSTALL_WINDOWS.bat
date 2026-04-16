@echo off
setlocal enabledelayedexpansion

title ASCII Video Player - Professional Installer
echo ============================================================
echo   ASCII Video Player - Installation Wizard
echo ============================================================
echo.

:: 1. Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

:: 2. Install dependencies
echo [1/4] Installing required Python packages...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies. Check your internet connection.
    pause
    exit /b 1
)
echo [OK] Dependencies installed.

:: 3. Create a permanent installation directory
set "INSTALL_DIR=%USERPROFILE%\.ascii-video-player"
echo [2/4] Setting up installation directory at %INSTALL_DIR%...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
copy /Y "src\main.py" "%INSTALL_DIR%\ascii-player.py" >nul

:: 4. Create a launcher batch file
echo [3/4] Creating system launcher...
(
echo @echo off
echo python "%%USERPROFILE%%\.ascii-video-player\ascii-player.py" %%*
) > "%INSTALL_DIR%\ascii-player.bat"

:: 5. Add to User PATH
echo [4/4] Adding to User PATH...
:: Use PowerShell to safely check and add the directory to the user's PATH
powershell -Command ^
    "$currentPath = [Environment]::GetEnvironmentVariable('Path', 'User'); " ^
    "if ($currentPath -notlike '*%INSTALL_DIR%*') { " ^
    "    [Environment]::SetEnvironmentVariable('Path', $currentPath + ';%INSTALL_DIR%', 'User'); " ^
    "    Write-Host '[OK] PATH updated successfully.' -ForegroundColor Green; " ^
    "} else { " ^
    "    Write-Host '[INFO] Directory already in PATH.' -ForegroundColor Cyan; " ^
    "}"

if errorlevel 1 (
    echo [WARNING] Could not automatically update PATH. 
    echo Please manually add %INSTALL_DIR% to your environment variables.
)

echo.
echo ============================================================
echo   INSTALLATION COMPLETE!
echo ============================================================
echo.
echo You can now run the player from ANY terminal using:
echo    ascii-player <video_file_or_url> [--terminal]
echo.
echo Note: You MUST restart your terminal for PATH changes to take effect.
echo.
pause
