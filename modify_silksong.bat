@echo off
setlocal enabledelayedexpansion

:: =============================================================================
:: Script to modify Hollow Knight Silksong save file
:: Supports multiple permadeath modes: 0 (Normal), 1 (Steel Soul - modded), 2 (Steel Soul - original)
:: =============================================================================

title Hollow Knight Silksong - Save File Modifier

echo.
echo ================================================================
echo     HOLLOW KNIGHT SILKSONG - SAVE FILE MODIFIER
echo ================================================================
echo.
echo This script will modify your save file to change the permadeath mode.
echo.
echo Available modes:
echo   0 - Normal mode (regular gameplay)
echo   1 - Steel Soul mode (original permadeath behavior, can be used even after death)
echo   2 - Steel Soul mode (dead state)
echo.
echo IMPORTANT: An automatic backup of your original file will be created
echo.

:: Define script directory
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%silksong_save_editor.py"

:: Verify that the script directory exists
if not exist "%SCRIPT_DIR%" (
    echo ERROR: Cannot find script directory
    echo Expected directory: %SCRIPT_DIR%
    pause
    exit /b 1
)

:: Verify that the Python script exists
if not exist "%PYTHON_SCRIPT%" (
    echo ERROR: Cannot find Python script
    echo Expected file: %PYTHON_SCRIPT%
    echo.
    echo Make sure the silksong_save_editor.py file is in the same folder as this .bat
    pause
    exit /b 1
)

echo Script found: silksong_save_editor.py
echo.

:: Confirm before proceeding
set /p "confirm=Do you want to continue with the modification? (Y/N): "
if /i not "%confirm%"=="Y" if /i not "%confirm%"=="y" (
    echo Operation cancelled by user
    pause
    exit /b 0
)

echo.
echo ================================================================
echo                    STARTING MODIFICATION
echo ================================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in system PATH
    echo.
    echo To install Python:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download and install Python 3.x
    echo 3. Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python detected correctly
echo.

:: Check if cryptography library is installed
python -c "import cryptography" >nul 2>&1
if errorlevel 1 (
    echo The 'cryptography' library is not installed
    echo Installing it automatically...
    echo.
    pip install cryptography
    if errorlevel 1 (
        echo ERROR: Could not install cryptography library
        echo.
        echo Try manually with:
        echo pip install cryptography
        pause
        exit /b 1
    )
    echo.
    echo cryptography library installed correctly
    echo.
)

:: Execute Python script in interactive mode
echo Starting save file modifier in interactive mode...
echo The script will guide you through the process.
echo.
python "%PYTHON_SCRIPT%"

if errorlevel 1 (
    echo.
    echo ERROR: Python script failed during execution
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo ================================================================
echo                    MODIFICATION COMPLETED
echo ================================================================
echo.
echo The save file modification process has finished.
echo Check the messages above for details.
echo.
echo IMPORTANT: If something goes wrong, you can restore the backup
echo by using the restore_backup.bat script.
echo.
echo Enjoy your modified Hollow Knight Silksong playthrough!
echo.

pause