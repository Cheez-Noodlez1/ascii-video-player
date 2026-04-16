@echo off
setlocal enabledelayedexpansion

title ASCII Video Player - Professional Administrative Installer
echo ============================================================
echo   ASCII Video Player - Installation Wizard (Admin Mode)
echo ============================================================
echo.

:: 1. Check for Administrative Privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] This installer is not running with Administrative privileges.
    echo To install to System PATH (Global), please run this script as Administrator.
    echo Proceeding with User-level installation...
    set "IS_ADMIN=0"
) else (
    echo [OK] Running with Administrative privileges.
    set "IS_ADMIN=1"
)
echo.

:: 2. Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

:: 3. Install dependencies
echo [1/4] Installing required Python packages...
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies. Check your internet connection.
    pause
    exit /b 1
)
echo [OK] Dependencies installed.

:: 4. Create a permanent installation directory
if "%IS_ADMIN%"=="1" (
    set "INSTALL_DIR=%ProgramFiles%\ASCII-Video-Player"
) else (
    set "INSTALL_DIR=%USERPROFILE%\.ascii-video-player"
)

echo [2/4] Setting up installation directory at %INSTALL_DIR%...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
copy /Y "src\main.py" "%INSTALL_DIR%\ascii-player.py" >nul

:: 5. Create a launcher batch file
echo [3/4] Creating system launcher...
:: We use a temporary file to avoid issues with nested parentheses in echo
set "LAUNCHER_PATH=%INSTALL_DIR%\ascii-player.bat"
echo @echo off > "%LAUNCHER_PATH%"
echo python "%INSTALL_DIR%\ascii-player.py" %%* >> "%LAUNCHER_PATH%"

:: 6. Add to PATH
echo [4/4] Adding to PATH...
if "%IS_ADMIN%"=="1" (
    set "PATH_SCOPE=Machine"
) else (
    set "PATH_SCOPE=User"
)

:: Use PowerShell for robust PATH modification, avoiding batch syntax pitfalls
powershell -Command ^
    "$dir = '%INSTALL_DIR%'; " ^
    "$scope = '%PATH_SCOPE%'; " ^
    "$currentPath = [Environment]::GetEnvironmentVariable('Path', $scope); " ^
    "if ($currentPath -notlike '*'+$dir+'*') { " ^
    "    [Environment]::SetEnvironmentVariable('Path', $currentPath + ';' + $dir, $scope); " ^
    "    Write-Host '[OK] ' $scope ' PATH updated successfully.' -ForegroundColor Green; " ^
    "} else { " ^
    "    Write-Host '[INFO] Directory already in ' $scope ' PATH.' -ForegroundColor Cyan; " ^
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
echo    ascii-player ^<video_file_or_url^> [--terminal]
echo.
echo Note: You MUST restart your terminal for PATH changes to take effect.
echo.
pause
