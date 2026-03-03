import os
import sys
import subprocess
import shutil
import time

# --- UI COLORS ---
G = "\033[92m" 
Y = "\033[93m" 
C = "\033[96m" 
M = "\033[95m" 
W = "\033[0m"  
R = "\033[91m" 
B = "\033[1m"

def banner():
    os.system('clear')
    print(f"{M}{B}##############################################################")
    print(f"#                                                            #")
    print(f"#   ███╗   ██╗ █████╗ ██╗    ██╗ █████╗ ██████╗              #")
    print(f"#   ████╗  ██║██╔══██╗██║    ██║██╔══██╗██╔══██╗             #")
    print(f"#   ██╔██╗ ██║███████║██║ █╗ ██║███████║██████╔╝             #")
    print(f"#   ██║╚██╗██║██╔══██║██║███╗██║██╔══██║██╔══██╗             #")
    print(f"#   ██║ ╚████║██║  ██║╚███╔███╔╝██║  ██║██████╔╝             #")
    print(f"#   ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═════╝              #")
    print(f"#                                                            #")
    print(f"#           {Y}NAWAB HUNTER SINGLE v0.0.0{M}                       #")
    print(f"#               {C}MODE: MASTER ELITE{M}                           #")
    print(f"##############################################################{W}\n")

def setup_alias():
    """Sets up the global alias 'nawab-run2' to point to this specific script."""
    script_path = os.path.abspath(__file__)
    home = os.path.expanduser("~")
    alias_line = f"alias nawab-run2='python3 {script_path}'"
    
    for rc_file in [".bashrc", ".zshrc"]:
        path = os.path.join(home, rc_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            # Clean old aliases and add the new one
            if "alias nawab-run2=" not in content:
                with open(path, "a") as f:
                    f.write(f"\n{alias_line}\n")
    
    print(f"{G}[+] Welcome to 'thenawabx' world's (Single Mode).{W}")

def run_step(step_name, command):
    """Executes a command and maintains its original visual output."""
    print(f"\n{B}{M}[{step_name}] Starting...{W}")
    print(f"{C}[RUNNING]: {W}{command}")
    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        print(f"\n{R}[!] {step_name} skipped by user (Ctrl+C). Moving forward...{W}")
        time.sleep(1)
    except Exception as e:
        print(f"{R}[!] Error in {step_name}: {e}{W}")

def process_recon(domain, extra_flags):
    # Folder naming: single_domain_com
    folder_name = f"single_{domain.replace('.', '_')}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    abs_path = os.path.abspath(folder_name)
    original_dir = os.getcwd()
    os.chdir(abs_path)

    print(f"\n{G}{B}>>> TARGET: {domain} <<<{W}")
    print(f"{Y}>>> FOLDER: {abs_path}/ <<<{W}")
    print(f"{Y}>>> PRESS Ctrl+C TO SKIP ANY STEP <<<{W}\n")

    # --- POINT 1 & 2: DIRECT PROBING (Skipping Sub-enumeration) ---
    run_step("POINT 1 & 2: Resolve Target", 
             f"echo {domain} | dnsx {extra_flags} -o dnsx_resolved.txt")

    # --- POINT 3: LIVE PROBING ---
    run_step("POINT 3: Live Probing", f"cat dnsx_resolved.txt | httpx-toolkit {extra_flags} -o live_sub.txt")

    # --- POINT 5: ARCHIVE URLs ---
    run_step("POINT 5: Wayback URLs", f"cat live_sub.txt | waybackurls | tee wayback_urls.txt")

    # --- POINT 5.1: ACTIVE CRAWLING ---
    run_step("POINT 5.1: Katana Crawling", f"katana -list live_sub.txt | tee katana_urls.txt")

    # --- POINT 6: URLS FILTERING ---
    run_step("POINT 6: Filtering", 
           f"cat wayback_urls.txt katana_urls.txt | sort -u | uro | tee all_urls.txt; "
           f"cat all_urls.txt | grep '=' | tee Equal_parameters.txt; "
           f"cat all_urls.txt | grep '\\.js' | tee js_file.txt; "
           f"cat all_urls.txt | grep 'api' | tee api_Information.txt; "
           f"cat all_urls.txt | grep 'robots.txt' | httpx-toolkit -mc 200 -o robots_files.txt; "
           f"cat all_urls.txt | grep -E '.env|.log|.sql|.conf' | tee information_Disc.txt"
)

    # --- NUCLEI CONFIGURATION ---
    template_path = os.path.expanduser("~/Downloads/NawabHunter-Ultimate/Nuclei_Templates")
    
    # --- POINT 7: NUCLEI (LIVE SUBS) ---
    run_step("POINT 7: Nuclei Sniper", 
             f"nuclei -l live_sub.txt -t {template_path} -fuzz -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_live_results.txt")

    # --- POINT 8: NUCLEI (EQUAL PARAMETERS) ---
    run_step("POINT 8: Nuclei Sniper", 
             f"nuclei -l Equal_parameters.txt -t {template_path} -fuzz -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_Equal_parameters_results.txt")

    # --- POINT 9: NUCLEI (JS FILES) ---
    run_step("POINT 9: Nuclei Sniper", 
             f"nuclei -l js_file.txt -t {template_path} -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_js_results.txt")

    # --- POINT 10: NUCLEI (API INFORMATION) ---
    run_step("POINT 10: Nuclei Sniper", 
             f"nuclei -l api_Information.txt -t {template_path} -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_api_results.txt")

    # --- POINT 11: NUCLEI (INFORMATION DISCOVERY) ---
    run_step("POINT 11: Nuclei Sniper", 
             f"nuclei -l information_Disc.txt -t {template_path} -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_information_results.txt")
    
    # --- POINT 12: NUCLEI (KATANA URLS) ---
    run_step("POINT 12: Nuclei Sniper (Katana URLs)", 
             f"nuclei -l katana_urls.txt -t {template_path} -fuzz -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_katana_results.txt")
    
    # --- POINT 13: FINAL RESULTS CONSOLIDATION ---
    master_results = "FINAL_RESULT_BY_THENAWABX.txt"
    subprocess.run(f"cat nuclei_*.txt 2>/dev/null | sort -u > {master_results}", shell=True)

    print("\n" + "="*50)
    if os.path.exists(master_results) and os.path.getsize(master_results) > 0:
        print(f"{G}[+] VULNERABILITY DETECTED! Check: {master_results}{W}")
    else:
        print(f"{R}[!] NOT FOUND VULNERABILITY{W}")
    print("="*50 + "\n")
    
    os.chdir(original_dir)
    print(f"\n{G}{B}[+] MISSION COMPLETED FOR: {domain}{W}")

def main():
    banner()
    setup_alias()

    extra_flags = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    print(f"{Y}[?] Enter Single Target (e.g., example.com): {W}", end="")
    try:
        target = input().strip()
        if target:
            process_recon(target, extra_flags)
                
    except KeyboardInterrupt:
        print(f"\n{R}[!] Nawab Hunter shut down.{W}")
        sys.exit(0)

    print(f"\n{G}{B}--- ALL TASKS FINISHED ---{W}")

if __name__ == "__main__":
    main()
