import subprocess
import os
import time

ZAPRET_DIR = r"C:\Users\damic\Desktop\vpn\Запретик\zapret-discord-youtube-1.9.7b"

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
        # 1. Kill any existing winws.exe processes
        print(f"[*] Stopping existing winws.exe instances...")
        subprocess.run(["taskkill", "/F", "/IM", "winws.exe"], capture_output=True)
        time.sleep(1) # Give it time to terminate
        
        # 2. Start the new preset script
        # Since these scripts often use 'start "" winws.exe', running them directly via cmd /c is appropriate.
        print(f"[*] Starting Zapret preset: {preset_name}")
        subprocess.Popen(
            ["cmd.exe", "/c", preset_name], 
            cwd=ZAPRET_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE # Start in a new window so it doesn't block
        )
        
        # Wait a bit for winws.exe to initialize
        time.sleep(3)
        return f"Successfully switched Zapret to preset: {preset_name}."
    except Exception as e:
        return f"Error switching Zapret preset: {str(e)}"
