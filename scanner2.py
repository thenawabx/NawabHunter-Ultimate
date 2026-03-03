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
    print(f"#           {Y}NAWAB HUNTER MULTI-SINGLE v0.0.0{M}                 #")
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
            if "alias nawab-run2=" not in content:
                with open(path, "a") as f:
                    f.write(f"\n{alias_line}\n")
    
    print(f"{G}[+] Welcome to 'thenawabx' world's (Multi-Single Mode).{W}")

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
    # Folder naming with recon_
    folder_name = f"recon_{domain.replace('.', '_')}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    abs_path = os.path.abspath(folder_name)
    original_dir = os.getcwd()
    os.chdir(abs_path)

    print(f"\n{G}{B}>>> TARGET: {domain} <<<{W}")
    print(f"{Y}>>> FOLDER: {abs_path}/ <<<{W}")
    print(f"{Y}>>> PRESS Ctrl+C TO SKIP ANY STEP <<<{W}\n")

    # --- ENUMERATION & PROBING ---
    run_step("POINT 1: Live Probing", f"echo {domain} | httpx-toolkit {extra_flags} -o live_target.txt")
    run_step("POINT 2: Wayback URLs", f"echo {domain} | waybackurls | tee wayback_urls.txt")
    run_step("POINT 3: Katana Crawling", f"katana -u {domain} -d 5 | tee katana_urls.txt")

    # --- URLS FILTERING ---
    run_step("POINT 4: Filtering", 
           f"cat wayback_urls.txt katana_urls.txt | sort -u | uro | tee all_urls.txt; "
           f"cat all_urls.txt | grep '=' | tee Equal_parameters.txt; "
           f"cat all_urls.txt | grep '\\.js' | tee js_file.txt; "
           f"cat all_urls.txt | grep 'api' | tee api_Information.txt; "
           f"cat all_urls.txt | grep 'robots.txt' | httpx-toolkit -mc 200 -o robots_files.txt; "
           f"cat all_urls.txt | grep -E '.env|.log|.sql|.conf' | tee information_Disc.txt"
    )

    # --- NUCLEI CONFIGURATION ---
    template_path = os.path.expanduser("~/Downloads/NawabHunter-Ultimate/Nuclei_Templates")
    
    # Nuclei Steps
    run_step("POINT 5: Nuclei Sniper (Live Target)", f"nuclei -l live_target.txt -t {template_path} -fuzz -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_live_results.txt")
    run_step("POINT 6: Nuclei Sniper (Parameters)", f"if [ -s Equal_parameters.txt ]; then nuclei -l Equal_parameters.txt -t {template_path} -fuzz -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_Equal_parameters_results.txt; fi")
    run_step("POINT 7: Nuclei Sniper (JS Files)", f"if [ -s js_file.txt ]; then nuclei -l js_file.txt -t {template_path} -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_js_results.txt; fi")
    run_step("POINT 8: Nuclei Sniper (API)", f"if [ -s api_Information.txt ]; then nuclei -l api_Information.txt -t {template_path} -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_api_results.txt; fi")
    run_step("POINT 9: Nuclei Sniper (Info Discovery)", f"if [ -s information_Disc.txt ]; then nuclei -l information_Disc.txt -t {template_path} -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_information_results.txt; fi")
    run_step("POINT 10: Nuclei Sniper (Katana URLs)", f"if [ -s katana_urls.txt ]; then nuclei -l katana_urls.txt -t {template_path} -fuzz -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags} -o nuclei_katana_results.txt; fi")
    
    # --- FINAL RESULTS CONSOLIDATION ---
    master_results = "FINAL_RESULT_BY_THENAWABX.txt"
    subprocess.run(f"cat nuclei_*.txt 2>/dev/null | sort -u > {master_results}", shell=True)

    # --- OUTPUT LOGIC (SAME AS ORIGINAL) ---
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

    print(f"{Y}[?] Enter Targets (comma separated): {W}", end="")
    try:
        user_input = input().strip()
        if not user_input:
            sys.exit(0)
        
        targets = [t.strip() for t in user_input.split(',')]
        for target in targets:
            if target:
                process_recon(target, extra_flags)
                
    except KeyboardInterrupt:
        print(f"\n{R}[!] Nawab Hunter shut down.{W}")
        sys.exit(0)

    print(f"\n{G}{B}--- ALL TASKS FINISHED ---{W}")

if __name__ == "__main__":
    main()
