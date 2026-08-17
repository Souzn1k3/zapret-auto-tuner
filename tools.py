import subprocess
import os
import sys
import time
import configparser

def get_base_path():
    """Returns the base path, works for both Python script and compiled PyInstaller executable."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(get_base_path(), "config.ini")

def load_zapret_dir():
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        config['SETTINGS'] = {
            'ZapretDir': r'C:\Path\To\Your\Zapret\Folder'
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
        print(f"[!] Файл конфигурации не найден. Был создан новый файл: {CONFIG_FILE}")
        print("[!] Пожалуйста, откройте config.ini, укажите правильный путь к папке Zapret и запустите программу снова.")
        sys.exit(1)
        
    config.read(CONFIG_FILE, encoding='utf-8')
    return config['SETTINGS'].get('ZapretDir', '')

ZAPRET_DIR = load_zapret_dir()

ALLOWED_PRESETS = [
    "general.bat", "general (ALT).bat", "general (ALT2).bat", "general (ALT3).bat",
    "general (ALT4).bat", "general (ALT5).bat", "general (ALT6).bat", "general (ALT7).bat",
    "general (ALT8).bat", "general (ALT9).bat", "general (ALT10).bat", "general (ALT11).bat",
    "general (SIMPLE FAKE).bat", "general (SIMPLE FAKE ALT).bat", "general (SIMPLE FAKE ALT2).bat",
    "general (FAKE TLS AUTO).bat", "general (FAKE TLS AUTO ALT).bat", 
    "general (FAKE TLS AUTO ALT2).bat", "general (FAKE TLS AUTO ALT3).bat"
]

def switch_zapret_preset(preset_name: str) -> str:
    """
    Kills any running Zapret (winws.exe) and starts the specified batch file.
    Includes STRICT security measures to prevent path traversal and arbitrary execution.
    """
    if not os.path.exists(ZAPRET_DIR):
        print(f"[!] Ошибка: Папка Zapret не найдена по пути: {ZAPRET_DIR}")
        print("[!] Проверьте путь в файле config.ini!")
        sys.exit(1)

    # 1. SECURITY: Check against strict whitelist
    if preset_name not in ALLOWED_PRESETS:
        return f"SECURITY ERROR: '{preset_name}' is not in the allowed presets list."
        
    # 2. SECURITY: Prevent path traversal (e.g. ../../)
    safe_preset_name = os.path.basename(preset_name)
    if safe_preset_name != preset_name:
         return "SECURITY ERROR: Path traversal attempt detected."
         
    preset_path = os.path.abspath(os.path.join(ZAPRET_DIR, safe_preset_name))
    
    # 3. SECURITY: Ensure the final path is strictly inside the ZAPRET_DIR
    if not preset_path.startswith(os.path.abspath(ZAPRET_DIR)):
        return "SECURITY ERROR: Attempted to access files outside Zapret directory."

    if not os.path.exists(preset_path):
        return f"Error: Preset '{preset_name}' does not exist."

    try:
        print(f"[*] Stopping existing winws.exe instances...")
        subprocess.run(["taskkill", "/F", "/IM", "winws.exe"], capture_output=True)
        time.sleep(1) # Give it time to terminate
        
        print(f"[*] Starting Zapret preset: {preset_name}")
        subprocess.Popen(
            ["cmd.exe", "/c", preset_name], 
            cwd=ZAPRET_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE # Start in a new window so it doesn't block
        )
        
        time.sleep(3)
        return f"Successfully switched Zapret to preset: {preset_name}."
    except Exception as e:
        return f"Error switching Zapret preset: {str(e)}"
