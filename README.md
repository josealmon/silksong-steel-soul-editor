# Hollow Knight Silksong - Save File Modifier

This set of tools allows you to modify your Hollow Knight Silksong save file to change the `permadeathMode` value.

## What does it do?

The script automatically modifies your save file (`userX.dat` where X is your save slot number) to change the `permadeathMode` parameter, keeping all other data intact.

### Available Modes:

- **0** - Normal mode (regular gameplay)
- **1** - Steel Soul mode (one life, but can continue after death with this mod)
- **2** - Steel Soul mode (original permadeath behavior)

## Features

- ✅ **Interactive mode** - Guides you through the process
- ✅ **Flexible paths** - Works with any user and profile ID
- ✅ **Saves configuration** - Remembers your save file location
- ✅ **Multiple modes** - Choose between Normal, Steel Soul (modded), or Steel Soul (original)
- ✅ **Automatic backups** - Always creates backups before modifying
- ✅ **Easy restoration** - Simple backup restore functionality

## Included files

- `modify_silksong.bat` - Main script that automates the entire process
- `silksong_save_editor.py` - Python tool that handles encryption/decryption
- `restore_backup.bat` - Backup restoration script
- `example_config.ini` - Example configuration file format
- `README.md` - This instruction file

**Auto-generated files:**

- `save_editor_config.ini` - Your saved configuration (created automatically)## Requirements

1. **Python 3.x** installed on your system

   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **cryptography library** (installed automatically)

## Usage

### Simple Method (Recommended)

1. **Close Hollow Knight Silksong** completely
2. **Double-click on `modify_silksong.bat`**
3. **Follow the interactive prompts**:
   - On first run, enter your save file path
   - Choose your desired permadeath mode (0, 1, or 2)
   - The script will handle everything else automatically

### Manual Method (Advanced)

For command line usage:

```cmd
# Interactive mode (recommended)
python silksong_save_editor.py

# Direct command line mode
python silksong_save_editor.py "path\to\userX.dat" <mode>
```

Where `<mode>` is:

- `0` for Normal mode
- `1` for Steel Soul mode (modded)
- `2` for Steel Soul mode (original)

## Save file location

The script will ask for your save file location on first run. The typical path structure is:

```
C:\Users\{USERNAME}\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\{PROFILE_ID}\userX.dat
```

**Examples:**

- `C:\Users\john\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\123456789\user1.dat`
- `C:\Users\maria\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\987654321\user2.dat`
- `C:\Users\alex\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\555666777\user3.dat`

**Where:**

- `{USERNAME}` = Your Windows username
- `{PROFILE_ID}` = Your unique profile ID (varies per user)
- `X` = Your save slot number (1, 2, 3, etc.)

**To find your profile ID and save file:**

1. Navigate to `C:\Users\{USERNAME}\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\`
2. Look for folders with numbers (like `114294607`)
3. Inside each folder, look for files like `user1.dat`, `user2.dat`, `user3.dat`
4. Choose the save file that corresponds to your game save slot

**Configuration:** Once entered, your path is saved and will be remembered for future use.

## Additional Tools

- **`restore_backup.bat`** - Use this if you need to restore the original file

## Security

- **An automatic backup is ALWAYS created** as `userX.dat.backup`
- If something goes wrong, you can restore by copying the backup back to the original file
- The script verifies the integrity of all files before proceeding

## Restore backup

If you need to restore your original save:

1. Go to the save folder
2. Delete or rename `userX.dat` (where X is your save slot)
3. Rename `userX.dat.backup` to `userX.dat`

## Troubleshooting

### Error: "Python is not installed"

- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### Error: "Cannot find save file"

- Verify that Hollow Knight Silksong is installed
- Confirm that you have played at least once
- Check that the path you entered is correct
- Look for the correct profile ID folder

### Error: "cryptography is not installed"

- The script tries to install it automatically
- If it fails, run manually: `pip install cryptography`

### Error: "permadeathMode not found"

- The save file may be corrupted
- Try with a previous backup
- Verify that it's really a Silksong file and not classic Hollow Knight

### "I can't find my save file"

1. Press `Windows + R`
2. Type: `%APPDATA%\..\LocalLow\Team Cherry\Hollow Knight Silksong`
3. Look for numbered folders
4. Check each folder for `user1.dat`, `user2.dat`, `user3.dat`, etc.
5. Choose the file that corresponds to your active save slot

## How it works

The process uses the same encryption algorithm that Hollow Knight Silksong uses:

1. **Configuration**: Saves your file path for future use
2. **Decryption**: Remove headers → Decode Base64 → Decrypt AES-ECB → Get JSON
3. **Modification**: Change `"permadeathMode"` to your selected value (0, 1, or 2)
4. **Encryption**: JSON → Encrypt AES-ECB → Encode Base64 → Add headers
5. **Backup**: Always creates `.backup` files before modification

### Permadeath Mode Details:

- **Mode 0 (Normal)**: Standard gameplay with respawning
- **Mode 1 (Steel Soul - Modded)**: One life mode, but this mod allows continuing after death
- **Mode 2 (Steel Soul - Original)**: True permadeath - game over on death

## Credits

Based on the work of:

- [@bloodorca](https://github.com/bloodorca/hollow) - Web encryption algorithm
- [@KayDeeTee](https://github.com/KayDeeTee/Hollow-Knight-SaveManager) - Original encryption algorithm

## Disclaimer

- **Use at your own risk**
- **Always backup your important files**
- This script modifies game files, although safely
- We are not responsible for data loss (although it's very unlikely)

---

Enjoy your modified Hollow Knight Silksong playthrough! 🦋
