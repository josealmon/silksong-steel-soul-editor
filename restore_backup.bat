@echo off
setlocal enabledelayedexpansion

:: =============================================================================
:: Backup restoration script for Hollow Knight Silksong
:: =============================================================================

title Hollow Knight Silksong - Backup Restorer

echo.
echo ================================================================
echo     BACKUP RESTORER - HOLLOW KNIGHT SILKSONG
echo ================================================================
echo.
echo This script helps you restore your original save file
echo from a backup in case something went wrong.
echo.

:: Define script directory
set "SCRIPT_DIR=%~dp0"

:: Try to get save path from config
echo Checking for saved configuration...
python -c "
import configparser
import os
config = configparser.ConfigParser()
config_file = os.path.join(r'%SCRIPT_DIR%', 'save_editor_config.ini')
if os.path.exists(config_file):
    config.read(config_file)
    if 'Settings' in config and 'save_path' in config['Settings']:
        print(config['Settings']['save_path'])
    else:
        print('NO_CONFIG')
else:
    print('NO_CONFIG')
" > temp_path.txt 2>nul

set /p SAVE_FILE=<temp_path.txt
del temp_path.txt

if "%SAVE_FILE%"=="NO_CONFIG" (
    echo No saved configuration found.
    echo.
    echo Please enter the full path to your save file:
    echo Example: C:\Users\YourName\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\123456789\userX.dat
    echo Note: X can be 1, 2, 3, etc. depending on your save slot
    echo.
    set /p "SAVE_FILE=Enter path: "
    set "SAVE_FILE=!SAVE_FILE:"=!"
)

if not exist "%SAVE_FILE%" (
    echo ERROR: Save file not found at: %SAVE_FILE%
    echo.
    echo Please make sure:
    echo 1. The path is correct
    echo 2. You have run the modifier at least once
    echo 3. The save file exists
    pause
    exit /b 1
)

:: Get directory from file path
for %%F in ("%SAVE_FILE%") do set "SAVE_DIR=%%~dpF"

echo Save file found: %SAVE_FILE%
echo.

:: Search for available backup files
echo Searching for backup files...
echo.

set "backup_count=0"
set "backup_files="
set "BACKUP_FILE=%SAVE_FILE%.backup"

:: Main backup
if exist "%BACKUP_FILE%" (
    set /a backup_count+=1
    echo [!backup_count!] user2.dat.backup
    for %%A in ("%BACKUP_FILE%") do (
        echo     Size: %%~zA bytes
        echo     Date: %%~tA
    )
    echo.
    set "backup_files=!backup_files! 1:%BACKUP_FILE%"
)

:: Manual backups with timestamp
for %%F in ("%SAVE_FILE%.backup_*") do (
    set /a backup_count+=1
    echo [!backup_count!] %%~nxF
    for %%A in ("%%F") do (
        echo     Size: %%~zA bytes
        echo     Date: %%~tA
    )
    echo.
    set "backup_files=!backup_files! !backup_count!:%%F"
)

:: Pre-restore backups
for %%F in ("%SAVE_FILE%.pre_restore_*") do (
    set /a backup_count+=1
    echo [!backup_count!] %%~nxF (pre-restore backup)
    for %%A in ("%%F") do (
        echo     Size: %%~zA bytes
        echo     Date: %%~tA
    )
    echo.
    set "backup_files=!backup_files! !backup_count!:%%F"
)

if %backup_count%==0 (
    echo ❌ No backup files found
    echo.
    echo There are no available backups to restore.
    echo Make sure you have run the modifier at least once.
    pause
    exit /b 1
)

echo ================================================================
echo.
echo Found %backup_count% available backup file(s)
echo.

:: Show current status
if exist "%SAVE_FILE%" (
    echo CURRENT FILE:
    for %%A in ("%SAVE_FILE%") do (
        echo user2.dat - %%~zA bytes - %%~tA
    )
    echo.
) else (
    echo ⚠️  WARNING: No current user2.dat file exists
    echo.
)

:: Select backup to restore
if %backup_count%==1 (
    echo Only 1 backup available. Restore this backup? (Y/N): 
    set /p "choice="
    if /i not "!choice!"=="Y" (
        echo Operation cancelled
        pause
        exit /b 0
    )
    set "selected=1"
) else (
    echo Select the number of the backup you want to restore (1-%backup_count%): 
    set /p "selected="
    
    :: Validate selection
    if "!selected!"=="" goto invalid_selection
    if !selected! LSS 1 goto invalid_selection
    if !selected! GTR %backup_count% goto invalid_selection
    goto valid_selection
    
    :invalid_selection
    echo Invalid selection. Must be a number between 1 and %backup_count%
    pause
    exit /b 1
    
    :valid_selection
)

:: Get the selected file
set "counter=0"
for %%B in (%backup_files%) do (
    set /a counter+=1
    if !counter!==!selected! (
        for /f "tokens=2 delims=:" %%P in ("%%B") do set "selected_backup=%%P"
    )
)

echo.
echo ================================================================
echo.
echo SELECTED RESTORATION:
echo File to restore: !selected_backup!
for %%A in ("!selected_backup!") do (
    echo Size: %%~zA bytes
    echo Date: %%~tA
)
echo.
echo ⚠️  IMPORTANT: This will overwrite your current user2.dat file
echo.

:: Final confirmation
set /p "confirm=Are you sure you want to continue? (Y/N): "
if /i not "!confirm!"=="Y" (
    echo Operation cancelled by user
    pause
    exit /b 0
)

echo.
echo Restoring backup...

:: Create backup of current file if it exists
if exist "%SAVE_FILE%" (
    set "timestamp=%date:~6,4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
    set "timestamp=!timestamp: =0!"
    copy "%SAVE_FILE%" "%SAVE_FILE%.pre_restore_!timestamp!" >nul
    if not errorlevel 1 (
        echo ✅ Backup of current file created: user2.dat.pre_restore_!timestamp!
    )
)

:: Restore the selected backup
copy "!selected_backup!" "%SAVE_FILE%" >nul
if errorlevel 1 (
    echo ❌ ERROR: Could not restore backup
    pause
    exit /b 1
)

echo ✅ Backup restored successfully!
echo.
echo ================================================================
echo.
echo RESTORATION COMPLETED
echo.
echo Your save file has been restored from backup.
echo.
echo File restored from: !selected_backup!
echo Destination file: %SAVE_FILE%
echo.
echo You can now play Hollow Knight Silksong again!
echo.

pause