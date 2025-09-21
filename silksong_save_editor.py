#!/usr/bin/env python3
"""
Hollow Knight Silksong Save File Editor
Based on the algorithm from repository: https://github.com/bloodorca/hollow

Permadeath Mode Values:
- 0: Normal mode (regular gameplay)
- 1: Steel Soul mode (one life, but can continue after death with this mod)
- 2: Current mode (varies by save file)
"""

import json
import base64
import struct
import sys
import os
import configparser
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Encryption algorithm constants
CSHARP_HEADER = bytes([0, 1, 0, 0, 0, 255, 255, 255, 255, 1, 0, 0, 0, 0, 0, 0, 0, 6, 1, 0, 0, 0])
AES_KEY = b'UKu52ePUBwetZ9wNX88o54dnfKRu0T1l'
ENDING_BYTE = bytes([11])

# Configuration file path
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'save_editor_config.ini')

# Default save path template
DEFAULT_SAVE_PATH = r"C:\Users\{USERNAME}\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\{PROFILE_ID}\userX.dat"

def load_config():
    """Load configuration from file"""
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    return config

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)

def get_save_path_from_config():
    """Get the saved path from config, or return None if not set"""
    config = load_config()
    if 'Settings' in config and 'save_path' in config['Settings']:
        return config['Settings']['save_path']
    return None

def save_path_to_config(path):
    """Save the path to config file"""
    config = load_config()
    if 'Settings' not in config:
        config['Settings'] = {}
    config['Settings']['save_path'] = path
    save_config(config)

def get_save_path_interactive():
    """Get save path from user input or config"""
    # Check if we have a saved path
    saved_path = get_save_path_from_config()
    
    if saved_path and os.path.exists(saved_path):
        print(f"Found saved path: {saved_path}")
        use_saved = input("Use this path? (Y/n): ").strip()
        if use_saved.lower() != 'n':
            return saved_path
    
    print("\nPlease enter your save file path.")
    print(f"Default template: {DEFAULT_SAVE_PATH}")
    print("Where:")
    print("  {USERNAME} = Your Windows username")
    print("  {PROFILE_ID} = Your profile ID (numbers like 114294607)")
    print("  X = Your save slot number (1, 2, 3, etc.)")
    print("\nExamples:")
    print(r"  C:\Users\john\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\123456789\user1.dat")
    print(r"  C:\Users\maria\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\987654321\user2.dat")
    print(r"  C:\Users\alex\AppData\LocalLow\Team Cherry\Hollow Knight Silksong\555666777\user3.dat")
    print()
    
    while True:
        path = input("Enter the full path to your userX.dat file: ").strip().strip('"')
        
        if os.path.exists(path):
            # Save for future use
            save_path_to_config(path)
            return path
        else:
            print(f"Error: File not found at {path}")
            print("Please check the path and try again.")
            retry = input("Try again? (Y/n): ").strip()
            if retry.lower() == 'n':
                return None

def generate_length_prefixed_string(length):
    """Generates a LengthPrefixedString according to Microsoft standard"""
    length = min(0x7FFFFFFF, length)
    result = []
    
    for i in range(4):
        if length >> 7 != 0:
            result.append((length & 0x7F) | 0x80)
            length >>= 7
        else:
            result.append(length & 0x7F)
            length >>= 7
            break
    
    if length != 0:
        result.append(length)
    
    return bytes(result)

def add_header(data):
    """Adds the necessary header to the file"""
    length_data = generate_length_prefixed_string(len(data))
    result = bytearray()
    result.extend(CSHARP_HEADER)
    result.extend(length_data)
    result.extend(data)
    result.extend(ENDING_BYTE)
    return bytes(result)

def remove_header(data):
    """Removes the header from the file"""
    # Remove fixed C# header and final byte 11
    data = data[len(CSHARP_HEADER):-1]
    
    # Remove LengthPrefixedString header
    length_count = 0
    for i in range(5):
        length_count += 1
        if (data[i] & 0x80) == 0:
            break
    
    return data[length_count:]

def aes_decrypt(data):
    """Decrypts using AES-ECB and removes PKCS7 padding"""
    cipher = Cipher(algorithms.AES(AES_KEY), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(data) + decryptor.finalize()
    
    # Remove PKCS7 padding
    padding_length = decrypted[-1]
    return decrypted[:-padding_length]

def aes_encrypt(data):
    """Adds PKCS7 padding and encrypts using AES-ECB"""
    # Add PKCS7 padding
    pad_value = 16 - (len(data) % 16)
    padded_data = data + bytes([pad_value] * pad_value)
    
    cipher = Cipher(algorithms.AES(AES_KEY), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padded_data) + encryptor.finalize()

def decode_save_file(file_path):
    """Decrypts a Hollow Knight Silksong save file"""
    try:
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
        
        # Step 1: Remove headers
        data = remove_header(encrypted_data)
        
        # Step 2: Decode Base64
        decoded_data = base64.b64decode(data)
        
        # Step 3: Decrypt AES
        decrypted_data = aes_decrypt(decoded_data)
        
        # Step 4: Convert to JSON string
        json_string = decrypted_data.decode('utf-8')
        
        return json_string
    
    except Exception as e:
        print(f"Error decrypting file: {e}")
        return None

def encode_save_file(json_string, output_path):
    """Encrypts and saves a Hollow Knight Silksong save file"""
    try:
        # Step 1: Convert JSON string to bytes
        data = json_string.encode('utf-8')
        
        # Step 2: Encrypt with AES
        encrypted_data = aes_encrypt(data)
        
        # Step 3: Encode in Base64
        encoded_data = base64.b64encode(encrypted_data)
        
        # Step 4: Add headers
        final_data = add_header(encoded_data)
        
        # Save file
        with open(output_path, 'wb') as f:
            f.write(final_data)
        
        return True
    
    except Exception as e:
        print(f"Error encrypting file: {e}")
        return False

def modify_permadeath_mode(json_string, new_value):
    """Modifies the permadeathMode value in the JSON"""
    try:
        save_data = json.loads(json_string)
        
        if 'playerData' in save_data and 'permadeathMode' in save_data['playerData']:
            old_value = save_data['playerData']['permadeathMode']
            save_data['playerData']['permadeathMode'] = new_value
            
            mode_names = {
                0: "Normal mode",
                1: "Steel Soul mode (modded - can continue after death)",
                2: "Steel Soul mode (original - permadeath)"
            }
            
            old_name = mode_names.get(old_value, f"Unknown mode ({old_value})")
            new_name = mode_names.get(new_value, f"Unknown mode ({new_value})")
            
            print(f"permadeathMode changed from {old_value} ({old_name}) to {new_value} ({new_name})")
            return json.dumps(save_data, indent=2)
        else:
            print("permadeathMode not found in save file")
            return None
    
    except Exception as e:
        print(f"Error modifying JSON: {e}")
        return None

def get_target_mode_interactive():
    """Get target permadeath mode from user input"""
    print("\nSelect the desired permadeath mode:")
    print("  0 - Normal mode (regular gameplay)")
    print("  1 - Steel Soul mode (one life, but can continue after death with this mod)")
    print("  2 - Steel Soul mode (original permadeath behavior)")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (0, 1, or 2): ").strip()
            mode = int(choice)
            if mode in [0, 1, 2]:
                return mode
            else:
                print("Please enter 0, 1, or 2")
        except ValueError:
            print("Please enter a valid number (0, 1, or 2)")

def main():
    """Main function"""
    # Check command line arguments
    if len(sys.argv) == 1:
        # Interactive mode
        print("=" * 60)
        print("  HOLLOW KNIGHT SILKSONG - SAVE FILE EDITOR")
        print("=" * 60)
        print()
        
        # Get save file path
        input_file = get_save_path_interactive()
        if not input_file:
            print("Operation cancelled.")
            return
        
        # Get target mode
        target_mode = get_target_mode_interactive()
        
    elif len(sys.argv) == 3:
        # Command line mode
        input_file = sys.argv[1]
        try:
            target_mode = int(sys.argv[2])
            if target_mode not in [0, 1, 2]:
                print("Error: Mode must be 0, 1, or 2")
                print("Usage: python silksong_save_editor.py <path_to_user2.dat> <mode>")
                print("Modes: 0=Normal, 1=Steel Soul (modded), 2=Steel Soul (original)")
                return
        except ValueError:
            print("Error: Mode must be a number (0, 1, or 2)")
            return
    else:
        print("Usage:")
        print("  Interactive mode: python silksong_save_editor.py")
        print("  Command line mode: python silksong_save_editor.py <path_to_userX.dat> <mode>")
        print("\nModes:")
        print("  0 - Normal mode")
        print("  1 - Steel Soul mode (modded - can continue after death)")
        print("  2 - Steel Soul mode (original permadeath)")
        print("\nNote: userX.dat where X is your save slot (1, 2, 3, etc.)")
        return
    
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} does not exist")
        return
    
    # Create backup
    backup_file = input_file + ".backup"
    try:
        with open(input_file, 'rb') as src, open(backup_file, 'wb') as dst:
            dst.write(src.read())
        print(f"\nBackup created: {backup_file}")
    except Exception as e:
        print(f"Error creating backup: {e}")
        return
    
    # Decrypt file
    print("Decrypting file...")
    json_string = decode_save_file(input_file)
    
    if json_string is None:
        print("Error decrypting file")
        return
    
    # Modify permadeathMode
    print(f"\nModifying permadeathMode to {target_mode}...")
    modified_json = modify_permadeath_mode(json_string, target_mode)
    
    if modified_json is None:
        print("Error modifying file")
        return
    
    # Encrypt and save modified file
    print("Encrypting and saving modified file...")
    if encode_save_file(modified_json, input_file):
        print(f"\n" + "="*50)
        print("FILE MODIFIED SUCCESSFULLY!")
        print(f"Backup saved in: {backup_file}")
        print("="*50)
    else:
        print("Error saving modified file")

if __name__ == "__main__":
    main()