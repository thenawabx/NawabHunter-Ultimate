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
    print(f"#           {Y}NAWAB HUNTER MULTI-SINGLE v2.0.0{M}                 #")
    print(f"#               {C}MODE: MASTER ELITE (DEEP){M}                  #")
    print(f"##############################################################{W}\n")

def setup_alias():
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
    print(f"{G}[+] Welcome to Nawab's Multi-Single Deep Recon Mode.{W}")

def run_step(step_name, command):
    print(f"\n{B}{M}[{step_name}] Starting...{W}")
    print(f"{C}[RUNNING]: {W}{command}")
    try:
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        print(f"\n{R}[!] {step_name} skipped by user.{W}")
        time.sleep(1)
    except Exception as e:
        print(f"{R}[!] Error: {e}{W}")

def process_recon(domain, extra_flags):
    folder_name = f"recon_single_{domain.replace('.', '_')}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    abs_path = os.path.abspath(folder_name)
    original_dir = os.getcwd()
    os.chdir(abs_path)

    print(f"\n{G}{B}>>> TARGET: {domain} <<<{W}")
    print(f"{Y}>>> FOLDER: {abs_path}/ <<<{W}\n")

    # --- STEP 1: DEEP PROBING & CRAWLING ---
    run_step("POINT 1: Live Probing", f"echo {domain} | httpx-toolkit {extra_flags} -o live_target.txt")
    run_step("POINT 2: URL Discovery", f"echo {domain} | waybackurls | tee wayback_urls.txt; gau {domain} --threads 10 | tee gau_urls.txt")
    # Katana with Deep Scan and JS Crawling enabled
    run_step("POINT 3: Katana Deep Crawling", f"katana -u {domain} -d 5 -jc -kf all -o katana_urls.txt")

    # --- STEP 2: SMART FILTERING (The Wildcard Logic) ---
    run_step("POINT 4: Intelligent Filtering", 
           f"cat wayback_urls.txt gau_urls.txt katana_urls.txt 2>/dev/null | sort -u | uro | tee all_urls.txt; "
           f"cat all_urls.txt | grep '=' | tee Equal_parameters.txt; "
           f"cat all_urls.txt | grep '\\.js' | tee js_file.txt; "
           f"cat all_urls.txt | grep 'api' | tee api_Information.txt; "
           f"cat all_urls.txt | grep -E '.env|.log|.sql|.conf|.bak' | tee information_Disc.txt; "
           f"echo {domain}/robots.txt | httpx-toolkit -mc 200 -o robots_files.txt"
    )

    # --- STEP 3: NUCLEI TARGETED ATTACK ---
    template_path = os.path.expanduser("~/Downloads/NawabHunter-Ultimate/Nuclei_Templates")
    
    # Logic: Only run if the file is not empty (-s check)
    nuclei_base = f"nuclei -t {template_path} -severity low,medium,high,critical -stats -rl 10 -c 5 {extra_flags}"

    run_step("POINT 5: Nuclei Sniper (Live Target)", f"{nuclei_base} -l live_target.txt -fuzz -o nuclei_live_results.txt")
    
    run_step("POINT 6: Nuclei Sniper (Parameters)", f"if [ -s Equal_parameters.txt ]; then {nuclei_base} -l Equal_parameters.txt -fuzz -o nuclei_params_results.txt; fi")
    
    run_step("POINT 7: Nuclei Sniper (JS Secrets)", f"if [ -s js_file.txt ]; then {nuclei_base} -l js_file.txt -o nuclei_js_results.txt; fi")
    
    run_step("POINT 8: Nuclei Sniper (API)", f"if [ -s api_Information.txt ]; then {nuclei_base} -l api_Information.txt -o nuclei_api_results.txt; fi")
    
    run_step("POINT 9: Nuclei Sniper (Sensitive Files)", f"if [ -s information_Disc.txt ]; then {nuclei_base} -l information_Disc.txt -o nuclei_info_results.txt; fi")

    # --- STEP 4: CONSOLIDATION ---
    master_results = "FINAL_REPORT_SINGLE.txt"
    subprocess.run(f"cat nuclei_*.txt 2>/dev/null | sort -u > {master_results}", shell=True)

    print("\n" + "="*60)
    if os.path.exists(master_results) and os.path.getsize(master_results) > 0:
        print(f"{G}[+] SUCCESS! Vulnerabilities found in {domain}. Check: {master_results}{W}")
    else:
        print(f"{R}[!] NO VULNERABILITIES FOUND ON THIS TARGET.{W}")
    print("="*60 + "\n")
    
    os.chdir(original_dir)

def main():
    banner()
    setup_alias()
    extra_flags = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    print(f"{Y}[?] Enter Single/Multiple Targets (e.g., target.com, site.sh): {W}", end="")
    try:
        user_input = input().strip()
        if not user_input: sys.exit(0)
        targets = [t.strip() for t in user_input.split(',')]
        for target in targets:
            if target: process_recon(target, extra_flags)
    except KeyboardInterrupt:
        print(f"\n{R}[!] Nawab Hunter Terminated.{W}")
        sys.exit(0)
    print(f"\n{G}{B}--- ALL MISSIONS COMPLETED ---{W}")

if __name__ == "__main__":
    main()
