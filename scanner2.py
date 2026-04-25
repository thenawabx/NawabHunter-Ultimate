import os
import sys
import subprocess
import shutil
import time

# --- UI COLORS ---
G, Y, C, M, W, R, B = "\033[92m", "\033[93m", "\033[96m", "\033[95m", "\033[0m", "\033[91m", "\033[1m"

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
    print(f"{G}{B}          --- Welcome to 'thenawabx' world! ---{W}")
    print(f"{R}{B}          >>> PRESS Ctrl+C TO SKIP ANY STEP <<<{W}\n")

def check_dependencies():
    tools = ["httpx-toolkit", "katana", "waybackurls", "uro", "nuclei"]
    missing = [t for t in tools if shutil.which(t) is None]
    if missing:
        print(f"{R}[!] Missing tools: {', '.join(missing)}{W}")
        time.sleep(1)

def run_step(name, cmd):
    print(f"{B}{C}┌──[{W}{M}{name}{W}{B}{C}] Execution started...{W}")
    print(f"{B}{C}└─╼ {W}{Y}[ {cmd} ]{W}")
    try:
        subprocess.run(cmd, shell=True)
        print(f"\n{G}[✔] {name} DONE!{W}\n")
    except KeyboardInterrupt:
        print(f"\n{R}[!] Skipped by User.{W}\n")
    except Exception as e:
        print(f"\n{R}[!] Error: {e}{W}\n")

def print_section(title):
    styled_title = f"<< {title} >>"
    print(f"\n{G}{B}{styled_title.center(60)}{W}\n")

def process_recon(target, flags):
    clean_name = target.replace('.', '_').replace('https://', '').replace('http://', '').replace('/', '')
    base = f"recon_single_{clean_name}"
    
    dirs = ["urls", "vulnerability"]
    for d in dirs:
        path = os.path.join(base, d)
        if not os.path.exists(path): os.makedirs(path)

    abs_path = os.path.abspath(base)
    orig_dir = os.getcwd()
    os.chdir(abs_path)

    print(f"\n{Y}{B}>>> STARTING MISSION: {target} <<<{W}\n")

    # --- 1. Probing ---
    print_section("1 Probing Target")
    run_step("1.1 Live Check", f"echo {target} | httpx-toolkit {flags} -o live_target.txt")

    # --- 2. URL Collection ---
    print_section("2 Urls Collecting")
    run_step("2.1 Waybackurls", f"echo {target} | waybackurls | tee urls/wayback_urls.txt")
    run_step("2.2 Katana Crawling", f"katana -u {target} -d 5 -jc -kf all -rl 10 -o urls/katana_urls.txt")

    # --- 3. Uro Filtering & Sorting ---
    print_section("3 Uro Filtering & Sorting")
    filter_cmd = (
        f"cat urls/wayback_urls.txt urls/katana_urls.txt 2>/dev/null | sort -u | uro | tee urls/all_urls.txt; "
        f"cat urls/all_urls.txt | grep '=' | tee urls/Equal_parameters.txt; "
        f"cat urls/all_urls.txt | grep '\\.js' | tee urls/js_file.txt; "
        f"cat urls/all_urls.txt | grep 'api' | tee urls/api_Information.txt; "
        f"cat urls/all_urls.txt | grep -E '.env|.log|.sql|.conf' | tee urls/information_Disc.txt"
    )
    run_step("3.1 URL Filtering", filter_cmd)

    # --- 4. Nuclei Scanning ---
    print_section("4 Nuclei Scanning")
    t_path = os.path.expanduser("~/Downloads/NawabHunter-Ultimate/Nuclei_Templates")
    nuclei_base = f"nuclei -t {t_path} -rl 6 -c 3 {flags}"

    tasks = [
        ("4.1 Live Target", "live_target.txt", "vulnerability/nuclei_live.txt", True),
        ("4.2 Equal Parameters", "urls/Equal_parameters.txt", "vulnerability/nuclei_params.txt", True),
        ("4.3 JS Files", "urls/js_file.txt", "vulnerability/nuclei_js.txt", False),
        ("4.4 API Info", "urls/api_Information.txt", "vulnerability/nuclei_api.txt", False),
        ("4.5 Info Discovery", "urls/information_Disc.txt", "vulnerability/nuclei_info.txt", False)
    ]

    for label, src, out, fuzz in tasks:
        if os.path.exists(src) and os.path.getsize(src) > 0:
            f_opt = "-fuzz" if fuzz else ""
            run_step(label, f"{nuclei_base} -l {src} {f_opt} -severity low,medium,high,critical -o {out}")

    # --- FINAL RESULTS ---
    master = "FINAL_REPORT_SINGLE.txt"
    subprocess.run(f"cat vulnerability/nuclei_*.txt 2>/dev/null | sort -u > {master}", shell=True)

    print("\n" + "═"*60)
    if os.path.exists(master) and os.path.getsize(master) > 0:
        print(f"{G}{B}[+] VULNERABILITIES FOUND!\n[+] Location: {abs_path}/{master}{W}")
    else: 
        print(f"{R}[!] NO VULNERABILITIES FOUND.{W}")
    print("═"*60 + "\n")
    
    os.chdir(orig_dir)

def main():
    banner()
    check_dependencies()
    flags = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    print(f"\n{C}{B}┌──({W}{G}Target Input{W}{B}{C})")
    print(f"└─╼ {Y}Please Enter Single/Multiple Targets (e.g., target.com, site.sh) {B}{C}>> {W}", end="")
    
    try:
        user_input = input().strip()
        if not user_input:
            sys.exit(0)
        
        targets = [t.strip() for t in user_input.split(',')]
        for t in targets:
            if t:
                process_recon(t, flags)
                
    except KeyboardInterrupt:
        print(f"\n{R}[!] Nawab Hunter Terminated.{W}")
        sys.exit(0)
    
    print(f"\n{G}{B}--- ALL MISSIONS COMPLETED ---{W}")

if __name__ == "__main__":
    main()
