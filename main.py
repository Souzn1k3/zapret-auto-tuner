import time
import json
from sensor import test_connection
from tools import switch_zapret_preset, ALLOWED_PRESETS
import concurrent.futures

TARGET_DOMAINS = ["discord.com", "youtube.com", "twitter.com", "instagram.com", "pornhub.com", "linkedin.com"]

def test_all_domains():
    """Tests all domains concurrently and returns a list of failed metrics."""
    failed = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(TARGET_DOMAINS)) as executor:
        futures = [executor.submit(test_connection, domain) for domain in TARGET_DOMAINS]
        for future in concurrent.futures.as_completed(futures):
            metrics = future.result()
            if metrics["http_error"] is not None:
                failed.append(metrics)
    return failed

def main():
    print(f"[*] Starting FAST Network Orchestrator (No AI Edition)")
    print(f"[*] Target domains: {', '.join(TARGET_DOMAINS)}")
    
    # Initial check
    failed_initial = test_all_domains()
    
    if not failed_initial:
        print("[*] Connections are already fine for all domains. No action needed.")
        return
        
    print(f"[!] Block detected on {len(failed_initial)} domain(s). Starting fast preset bruteforce...")
    
    for i, preset in enumerate(ALLOWED_PRESETS, 1):
        print(f"\n--- Attempt {i}/{len(ALLOWED_PRESETS)}: Trying '{preset}' ---")
        
        result = switch_zapret_preset(preset)
        print(f"[*] {result}")
        print("[*] Waiting 2 seconds for connection to stabilize...")
        time.sleep(2)
        
        failed_now = test_all_domains()
        if not failed_now:
            print(f"\n[+] SUCCESS! All connections restored using '{preset}'!")
            print(f"[+] To keep this setup forever, create a shortcut to '{preset}' in your Windows Startup folder.")
            return
        else:
            print(f"[-] Preset '{preset}' failed on {len(failed_now)} domain(s). Moving to next...")
            
    print(f"\n[-] All {len(ALLOWED_PRESETS)} presets exhausted. None were able to unblock all target domains.")

if __name__ == "__main__":
    main()
