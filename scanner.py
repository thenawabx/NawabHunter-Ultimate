import os
import sys
import subprocess
import shutil
import time

# --- UI COLORS ---
G, Y, C, M, W, R, B = "\033[92m", "\033[93m", "\033[96m", "\033[95m", "\033[0m", "\033[91m", "\033[1m"

last_interrupt_time = 0

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
    print(f"#           {Y}NAWAB HUNTER ULTIMATE v0.0.0{M}                     #")
    print(f"#             {C}MODE: FINAL ELITE MASTER{M}                       #")
    print(f"##############################################################{W}\n")
    print(f"{G}{B}          --- Welcome to 'thenawabx' world! ---{W}")
    print(f"{R}{B}   >>> PRESS Ctrl+C TO SKIP | DOUBLE PRESS TO EXIT <<<{W}\n")

def setup_alias():
    """Sets up the global alias 'Runawab' to point to this specific script."""
    script_path = os.path.abspath(__file__)
    home = os.path.expanduser("~")
    alias_line = f"alias Runawab='python3 {script_path}'"
    
    for rc_file in [".bashrc", ".zshrc"]:
        path = os.path.join(home, rc_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            if "alias Runawab=" not in content:
                with open(path, "a") as f:
                    f.write(f"\n# Nawab Hunter Alias\n{alias_line}\n")
    print(f"{G}[+] Alias 'Runawab' configured. Restart terminal to use it.{W}")

def handle_interrupt():
    global last_interrupt_time
    current_time = time.time()
    if current_time - last_interrupt_time < 3:
        print(f"\n{R}[!] Emergency Shutdown Initiated. Exiting...{W}")
        sys.exit(0)
    else:
        last_interrupt_time = current_time
        print(f"\n{Y}[!] Step Skipped. Press again quickly to exit.{W}")

def run_step(name, target_info, cmd):
    print(f"{B}{C}┌──[{W}{M}{name}{W}{B}{C}] Target: {W}{G}{target_info}{W}")
    print(f"{B}{C}└─╼ {W}{Y}[ {cmd} ]{W}")
    try:
        subprocess.run(cmd, shell=True)
        print(f"\n{G}[✔] {name} DONE for {target_info}!{W}\n")
    except KeyboardInterrupt:
        handle_interrupt()

def process_single_recon(target, extra_flags, parent_dir, is_single_mode=False):
    clean_target = target.replace('https://', '').replace('http://', '').strip('/')
    suffix = "single_" if is_single_mode else ""
    folder_name = f"recon_{suffix}{clean_target.replace('.', '_')}"
    target_path = os.path.join(parent_dir, folder_name)
    
    if not os.path.exists(target_path): os.makedirs(target_path)
    
    orig_dir = os.getcwd()
    os.chdir(target_path)

    t_path = os.path.expanduser("~/Downloads/NawabHunter-Ultimate/Nuclei_Templates")
    vuln_master = os.path.join(orig_dir, "Vulnerability_By_Thenawabx-Tools")

    run_step("POINT 1: Live Probing", clean_target, f"echo {clean_target} | httpx-toolkit {extra_flags} -o live_sub.txt")
    run_step("POINT 2: Katana Crawling", clean_target, f"katana -u {clean_target} -rl 10 -o katana_urls.txt")
    run_step("POINT 3: Wayback URLs", clean_target, f"echo {clean_target} | waybackurls | tee wayback_urls.txt")

    run_step("POINT 4: Filtering", clean_target, 
           f"cat wayback_urls.txt katana_urls.txt 2>/dev/null | sort -u > all_urls.txt; "
           f"grep '=' all_urls.txt > Equal_parameters.txt; "
           f"grep '\\.js' all_urls.txt > js_file.txt; "
           f"grep 'api' all_urls.txt > api_Information.txt; "
           f"grep -E '.env|.log|.sql|.conf' all_urls.txt > information_Disc.txt")

    nuclei_base = f"nuclei -t {t_path} -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags}"
    
    n_tasks = [
        ("POINT 7: Nuclei sniper (Live)", "live_sub.txt", "nuclei_live.txt"),
        ("POINT 8: Nuclei sniper (Params)", "Equal_parameters.txt", "nuclei_params.txt"),
        ("POINT 9: Nuclei sniper (JS)", "js_file.txt", "nuclei_js.txt"),
        ("POINT 10: Nuclei sniper (API)", "api_Information.txt", "nuclei_api.txt"),
        ("POINT 11: Nuclei sniper (Info)", "information_Disc.txt", "nuclei_info.txt"),
        ("POINT 12: Nuclei sniper (Katana)", "katana_urls.txt", "nuclei_katana.txt")
    ]

    found_in_target = False
    for label, src, out in n_tasks:
        if os.path.exists(src) and os.path.getsize(src) > 0:
            run_step(label, clean_target, f"{nuclei_base} -l {src} -o {out}")
            if os.path.exists(out) and os.path.getsize(out) > 0:
                found_in_target = True
                os.system(f"cat {out} 2>/dev/null >> {vuln_master}")

    print("\n" + "="*60)
    if found_in_target:
        print(f"{G}{B}[+] VULNERABILITY FOUND on {clean_target}! Check: {vuln_master}{W}")
    else:
        print(f"{R}{B}[!] NO VULNERABILITY FOUND on {clean_target}.{W}")
    print("="*60 + "\n")

    os.chdir(orig_dir)

def process_wildcard(domain, extra_flags):
    base_folder = f"recon_wildcard_{domain.replace('.', '_')}"
    if not os.path.exists(base_folder): os.makedirs(base_folder)
    
    abs_base = os.path.abspath(base_folder)
    orig_dir = os.getcwd()
    os.chdir(abs_base)

    run_step("POINT 1: Subdomain Enumeration", domain, 
             f"subfinder -d {domain} -o subfinder.txt; "
             f"assetfinder --subs-only {domain} > assetfinder.txt; "
             f"sublist3r -d {domain} -o sublist3r.txt")

    run_step("POINT 2: Merge & Resolve", domain, 
             f"cat subfinder.txt assetfinder.txt sublist3r.txt 2>/dev/null | sort -u > all_subs.txt; "
             f"dnsx -l all_subs.txt {extra_flags} -o dnsx_resolved.txt")

    run_step("POINT 3: Live Probing", domain, f"cat dnsx_resolved.txt | httpx-toolkit -o live_sub.txt")

    if os.path.exists("live_sub.txt") and os.path.getsize("live_sub.txt") > 0:
        with open("live_sub.txt", "r") as f:
            domains = [l.strip().replace('https://', '').replace('http://', '') for l in f if l.strip()]
        
        print(f"\n{G}[+] Discovered Live Domains:{W}")
        for idx, d in enumerate(domains, 1):
            print(f"{C}{idx}.{W} {d}")
        
        print(f"\n{Y}[?] Enter indices to scan (e.g: 1,2,5) or 'all': {W}", end="")
        choice = input().strip().lower()
        
        targets_to_scan = []
        if choice == 'all':
            targets_to_scan = domains
        else:
            try:
                indices = [int(x.strip()) - 1 for x in choice.split(',')]
                targets_to_scan = [domains[i] for i in indices if 0 <= i < len(domains)]
            except:
                print(f"{R}[!] Invalid input. Skipping deep scan.{W}")

        for t in targets_to_scan:
            process_single_recon(t, extra_flags, abs_base, is_single_mode=False)
    
    os.chdir(orig_dir)

def main():
    setup_alias()
    banner()
    extra_flags = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    print(f"{C}{B}Select Operation Mode:{W}")
    print(f"{G}1.{W} Wildcard Mode (Subdomain Discovery)")
    print(f"{G}2.{W} Single Mode (Deep Recon)")
    print(f"{C}{B}└─╼ {W}{Y}Input Choice {B}{C}>> {W}", end="")
    
    mode = input().strip()
    print(f"\n{Y}[?] Enter Target(s) (comma separated): {W}", end="")
    
    try:
        user_input = input().strip()
        if not user_input: return
        targets = [t.strip() for t in user_input.split(',')]
        
        open("Vulnerability_By_Thenawabx-Tools", "a").close()

        for t in targets:
            if mode == "1":
                process_wildcard(t, extra_flags)
            elif mode == "2":
                process_single_recon(t, extra_flags, os.getcwd(), is_single_mode=True)
                
    except KeyboardInterrupt:
        handle_interrupt()

if __name__ == "__main__":
    main()
