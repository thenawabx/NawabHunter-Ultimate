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
    print(f"#   ███╗   ██╗ █████╗ ██╗    ██╗ █████╗ ██████╗            #")
    print(f"#   ████╗  ██║██╔══██╗██║    ██║██╔══██╗██╔══██╗           #")
    print(f"#   ██╔██╗ ██║███████║██║ █╗ ██║███████║██████╔╝           #")
    print(f"#   ██║╚██╗██║██╔══██║██║███╗██║██╔══██║██╔══██╗           #")
    print(f"#   ██║ ╚████║██║  ██║╚███╔███╔╝██║  ██║██████╔╝           #")
    print(f"#   ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝╚═════╝            #")
    print(f"#                                                            #")
    print(f"#           {Y}NAWAB HUNTER ULTIMATE v0.0.0{M}                 #")
    print(f"#               {C}MODE: MASTER ELITE{M}                     #")
    print(f"##############################################################{W}\n")

def setup_alias():
    """Sets up the global alias 'nawab-run' to point to this specific script."""
    script_path = os.path.abspath(__file__)
    home = os.path.expanduser("~")
    alias_line = f"alias nawab-run='python3 {script_path}'"
    
    for rc_file in [".bashrc", ".zshrc"]:
        path = os.path.join(home, rc_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            # Clean old aliases and add the new one
            if "alias nawab-run=" not in content:
                with open(path, "a") as f:
                    f.write(f"\n{alias_line}\n")
    
    print(f"{G}[+] Welcome to 'thenawabx' world's .{W}")

def run_step(step_name, command):
    """Executes a command and maintains its original visual output."""
    print(f"\n{B}{M}[{step_name}] Starting...{W}")
    print(f"{C}[RUNNING]: {W}{command}")
    try:
        # subprocess.run ensures the tool's original UI/Colors are displayed
        subprocess.run(command, shell=True)
    except KeyboardInterrupt:
        print(f"\n{R}[!] {step_name} skipped by user (Ctrl+C). Moving forward...{W}")
        time.sleep(1)
    except Exception as e:
        print(f"{R}[!] Error in {step_name}: {e}{W}")

def process_recon(domain, extra_flags):
    # Folder naming: recon_domain_com
    folder_name = f"recon_{domain.replace('.', '_')}"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Use Absolute Path for stability
    abs_path = os.path.abspath(folder_name)
    original_dir = os.getcwd()
    os.chdir(abs_path)

    print(f"\n{G}{B}>>> TARGET: {domain} <<<{W}")
    print(f"{Y}>>> FOLDER: {abs_path}/ <<<{W}")
    print(f"{Y}>>> PRESS Ctrl+C TO SKIP ANY STEP <<<{W}\n")

    # --- POINT 1: ENUMERATION ---
    # Removed -silent to show original output
    run_step("POINT 1: Subdomain Enumeration", 
             f"subfinder -d {domain} {extra_flags} -o subfinder.txt; "
             f"assetfinder --subs-only {domain} | tee assetfinder.txt; "
             f"sublist3r -d {domain} -o sublist3r.txt")

    # --- POINT 2: MERGE & RESOLVE ---
    run_step("POINT 2: Merge & Resolve", 
             f"cat subfinder.txt assetfinder.txt sublist3r.txt 2>/dev/null | sort -u > all_subs.txt; "
             f"dnsx -l all_subs.txt {extra_flags} -o dnsx_resolved.txt")

    # --- POINT 3: LIVE PROBING ---
    run_step("POINT 3: Live Probing", f"cat dnsx_resolved.txt | httpx-toolkit {extra_flags} -o live_sub.txt")

    # --- POINT 4: TAKEOVER CHECK ---
    run_step("POINT 4: Takeover Check", 
             f"cat all_subs.txt | httpx-toolkit -mc 404,403,500,502,503 {extra_flags} -o takeover_for_sub.txt; "
             f"if [ -s takeover_for_sub.txt ]; then subzy run --targets takeover_for_sub.txt {extra_flags} | tee sub_take.txt; fi")

    # --- POINT 5: ARCHIVE URLs ---
    run_step("POINT 5: Wayback URLs", f"cat live_sub.txt | waybackurls | tee wayback_urls.txt")

    # --- POINT 5.1: ACTIVE CRAWLING ---
    run_step("POINT 5.1: Katana Crawling", f"katana -list live_sub.txt | tee katana_urls.txt")

    # --- POINT 6: URLS FILTERING ---
    run_step("POINT 6: Filtering", 
           f"cat wayback_urls.txt katana_urls.txt | sort -u > all_urls.txt; "
           f"cat all_urls.txt | grep '=' | tee Equal_parameters.txt; "
           f"cat all_urls.txt | grep '\\.js' | tee js_file.txt; "
           f"cat all_urls.txt | grep 'api' | tee api_Information.txt; "
           f"cat all_urls.txt | grep -E '.env|.log|.sql|.conf' | tee information_Disc.txt"
)

    # --- NUCLEI CONFIGURATION ---
    template_path = os.path.expanduser("~/Downloads/NawabHunter-Ultimate/Nuclei_Templates")
    
    # --- POINT 7: NUCLEI (LIVE SUBS) ---
    nuclei_cmd_7 = (
        f"nuclei -l live_sub.txt -t {template_path} "
        f"-severity low,medium,high,critical -stats -rl 6 -c 3 "
        f"{extra_flags} -o nuclei_live_results.txt"
    )
    run_step("POINT 7: Nuclei Sniper", nuclei_cmd_7)

    # --- POINT 8: NUCLEI (EQUAL PARAMETERS) ---
    nuclei_cmd_8 = (
        f"nuclei -l Equal_parameters.txt -t {template_path} "
        f"-severity low,medium,high,critical -stats -rl 6 -c 3 "
        f"{extra_flags} -o nuclei_Equal_parameters_results.txt"
    )
    run_step("POINT 8: Nuclei Sniper", nuclei_cmd_8)

    # --- POINT 9: NUCLEI (JS FILES) ---
    nuclei_cmd_9 = (
        f"nuclei -l js_file.txt -t {template_path} "
        f"-severity low,medium,high,critical -stats -rl 6 -c 3 "
        f"{extra_flags} -o nuclei_js_results.txt"
    )
    run_step("POINT 9: Nuclei Sniper", nuclei_cmd_9)

    # --- POINT 10: NUCLEI (API INFORMATION) ---
    nuclei_cmd_10 = (
        f"nuclei -l api_Information.txt -t {template_path} "
        f"-severity low,medium,high,critical -stats -rl 6 -c 3 "
        f"{extra_flags} -o nuclei_api_results.txt"
    )
    run_step("POINT 10: Nuclei Sniper", nuclei_cmd_10)

    # --- POINT 11: NUCLEI (INFORMATION DISCOVERY) ---
    nuclei_cmd_11 = (
        f"nuclei -l information_Disc.txt -t {template_path} "
        f"-severity low,medium,high,critical -stats -rl 6 -c 3 "
        f"{extra_flags} -o nuclei_information_results.txt"
    )
    run_step("POINT 11: Nuclei Sniper", nuclei_cmd_11)

    
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
