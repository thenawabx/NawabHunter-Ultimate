import os
import sys
import subprocess
import shutil
import time
import select
import signal
import json

G, Y, C, M, W, R, B = "\033[92m", "\033[93m", "\033[96m", "\033[95m", "\033[0m", "\033[91m", "\033[1m"

last_interrupt_time = 0

def clear_input_buffer():
    try:
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except Exception:
        while select.select([sys.stdin], [], [], 0.0)[0]:
            sys.stdin.read(1)

def save_progress(progress_file_path, data):
    try:
        with open(progress_file_path, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

def load_progress(progress_file_path):
    if os.path.exists(progress_file_path):
        try:
            with open(progress_file_path, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def clear_progress(progress_file_path):
    if os.path.exists(progress_file_path):
        try:
            os.remove(progress_file_path)
        except Exception:
            pass

def check_existing_sessions():
    for item in os.listdir("."):
        if os.path.isdir(item) and item.startswith("recon_"):
            prog_file = os.path.join(item, ".nawab_progress.json")
            if os.path.exists(prog_file):
                data = load_progress(prog_file)
                if data:
                    return prog_file, data, item
    return None, None, None

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
    print(f"#           {Y}NAWAB HUNTER ULTIMATE v0.1.1{M}                     #")
    print(f"#             {C}MODE: FINAL ELITE MASTER{M}                       #")
    print(f"##############################################################{W}\n")
    print(f"{G}{B}          --- Welcome to 'thenawabx' world! ---{W}")
    print(f"{R}{B}   >>> PRESS Ctrl+C TO SKIP | DOUBLE PRESS TO EXIT <<<{W}\n")

def setup_alias():
    script_path = os.path.abspath(__file__)
    home = os.path.expanduser("~")
    alias_line = f"alias runawab='python3 {script_path}'"
    
    for rc_file in [".bashrc", ".zshrc"]:
        path = os.path.join(home, rc_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            if alias_line not in content:
                with open(path, "a") as f:
                    f.write(f"\n# Nawab Hunter Alias\n{alias_line}\n")

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
        proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
        proc.wait()
    except KeyboardInterrupt:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except Exception:
            pass
        handle_interrupt()

def process_single_recon(target, extra_flags, parent_dir, master_vuln_file):
    clean_target = target.replace('https://', '').replace('http://', '').strip('/')
    folder_name = f"sub_{clean_target.replace('.', '_')}"
    sub_path = os.path.join(parent_dir, folder_name)
    
    if not os.path.exists(sub_path): 
        os.makedirs(sub_path)
    
    orig_dir = os.getcwd()
    os.chdir(sub_path)

    t_path = os.path.expanduser("~/Downloads/NawabHunter-Ultimate/Nuclei_Templates")

    run_step("POINT 1: Live Probing", clean_target, f"echo {clean_target} | httpx-toolkit {extra_flags} -o live_sub.txt")
    run_step("POINT 2: Katana Crawling", clean_target, f"katana -u {clean_target} -rl 10 -o katana_urls.txt")
    run_step("POINT 3: Wayback URLs", clean_target, f"echo {clean_target} | waybackurls | tee wayback_urls.txt")

    run_step("POINT 4: Filtering", clean_target, 
           f"cat wayback_urls.txt katana_urls.txt 2>/dev/null | sort -u > all_urls.txt; "
           f"grep '=' all_urls.txt > Equal_parameters.txt; "
           f"grep '\\.js' all_urls.txt > js_file.txt; "
           f"grep 'api' all_urls.txt > api_Information.txt; "
           f"grep -E '.env|.log|.sql|.conf' all_urls.txt > information_Disc.txt")

    run_step("POINT 5: FFUF Fuzzing", clean_target, f"ffuf -u http://{clean_target}/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .php,.txt,.html,.json -mc 200,204,301,302,307,401,403 -o ffuf_results.txt -of md")

    nuclei_base = f"nuclei -t {t_path} -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags}"
    
    n_tasks = [
        ("POINT 6: Nuclei (Live)", "live_sub.txt", "nuclei_live.txt", True),
        ("POINT 7: Nuclei (Params)", "Equal_parameters.txt", "nuclei_params.txt", True),
        ("POINT 8: Nuclei (JS)", "js_file.txt", "nuclei_js.txt", False),
        ("POINT 9: Nuclei (API)", "api_Information.txt", "nuclei_api.txt", False),
        ("POINT 10: Nuclei (Info)", "information_Disc.txt", "nuclei_info.txt", False)
    ]

    found_in_target = False
    for label, src, out, use_fuzz in n_tasks:
        if os.path.exists(src) and os.path.getsize(src) > 0:
            cmd_fuzz_flag = " -fuzz" if use_fuzz else ""
            run_step(label, clean_target, f"{nuclei_base}{cmd_fuzz_flag} -l {src} -o {out}")
            
            if os.path.exists(out) and os.path.getsize(out) > 0:
                found_in_target = True
                with open(master_vuln_file, "a") as f_master:
                    f_master.write(f"\n========================================\n")
                    f_master.write(f"TARGET SUBDOMAIN: {clean_target}\n")
                    f_master.write(f"SCAN STEP: {label}\n")
                    f_master.write(f"========================================\n")
                    with open(out, "r") as f_out:
                        f_master.write(f_out.read())
                    f_master.write("\n")

    print("\n" + "="*60)
    os.chdir(orig_dir)

    if found_in_target:
        print(f"{G}{B}[+] VULNERABILITY DETECTED on {clean_target}! Check Report: {master_vuln_file}{W}")
    else:
        print(f"{R}{B}[!] NO VULNERABILITY DETECTED on {clean_target}.{W}")
    print("="*60 + "\n")

def process_single_domain_mode(target, extra_flags):
    clean_target = target.replace('https://', '').replace('http://', '').strip('/')
    folder_name = f"recon_single_{clean_target.replace('.', '_')}"
    
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        
    abs_folder = os.path.abspath(folder_name)
    master_vuln_file = os.path.join(abs_folder, "Vulnerability_Report.txt")
    
    process_single_recon(clean_target, extra_flags, abs_folder, master_vuln_file)

def process_wildcard(domain, extra_flags, resume_indices=None):
    base_folder = f"recon_wildcard_{domain.replace('.', '_')}"
    if not os.path.exists(base_folder): 
        os.makedirs(base_folder)
        
    abs_base = os.path.abspath(base_folder)
    master_vuln_file = os.path.join(abs_base, "Vulnerability_Report.txt")
    progress_file_path = os.path.join(abs_base, ".nawab_progress.json")
    
    orig_dir = os.getcwd()
    os.chdir(abs_base)

    if not resume_indices:
        run_step("POINT 1: Subdomain Enumeration", domain, 
                 f"subfinder -d {domain} -o subfinder.txt; "
                 f"assetfinder --subs-only {domain} | tee assetfinder.txt; "
                 f"sublist3r -d {domain} -o sublist3r.txt")

        run_step("POINT 2: Merge & Unique", domain, f"cat subfinder.txt assetfinder.txt sublist3r.txt 2>/dev/null | sort -u > all_subs.txt")
        run_step("POINT 3: DNS Resolution", domain, f"dnsx -l all_subs.txt {extra_flags} -o dnsx_resolved.txt")

        run_step("POINT 4: Takeover Check", domain, 
                 f"cat all_subs.txt | httpx-toolkit -mc 404,403,500,502,503 {extra_flags} -o takeover_for_sub.txt; "
                 f"if [ -s takeover_for_sub.txt ]; then subzy run --targets takeover_for_sub.txt {extra_flags} | tee sub_take_result.txt; fi")

        run_step("POINT 5: Web Probing", domain, f"cat dnsx_resolved.txt | httpx-toolkit -o live_sub.txt")

    if os.path.exists("live_sub.txt") and os.path.getsize("live_sub.txt") > 0:
        with open("live_sub.txt", "r") as f:
            domains = [l.strip().replace('https://', '').replace('http://', '').strip('/') for l in f if l.strip()]
        
        scanned_indices = set(resume_indices) if resume_indices is not None else set()
        
        while len(scanned_indices) < len(domains):
            clear_input_buffer()

            print(f"\n{G}[+] Remaining Active Targets ({len(domains) - len(scanned_indices)} left):{W}")
            available_this_round = False
            for idx, d in enumerate(domains):
                if idx not in scanned_indices:
                    print(f"{C}{idx + 1}.{W} {d}")
                    available_this_round = True
            
            if not available_this_round: 
                break

            print(f"\n{Y}[?] Enter indices to scan (e.g: 1,2,5), 'all' or 'exit' [Auto-Next in 15s]: {W}", end="", flush=True)
            
            is_auto_select = False
            try:
                rlist, _, _ = select.select([sys.stdin], [], [], 15)
                if rlist:
                    choice = sys.stdin.readline().strip().lower()
                else:
                    is_auto_select = True
                    choice = ""
            except Exception:
                is_auto_select = True
                choice = ""
            
            if choice == 'exit': 
                break
            
            targets_to_scan = []
            
            if is_auto_select:
                for idx, d in enumerate(domains):
                    if idx not in scanned_indices:
                        targets_to_scan = [(idx, d)]
                        print(f"\n{M}[!] Timeout (15s). Auto-selecting next target: {C}{d}{W}")
                        break
            elif choice == 'all':
                targets_to_scan = [(idx, d) for idx, d in enumerate(domains) if idx not in scanned_indices]
            else:
                try:
                    indices = [int(x.strip()) - 1 for x in choice.split(',')]
                    for i in indices:
                        if 0 <= i < len(domains) and i not in scanned_indices:
                            targets_to_scan.append((i, domains[i]))
                except ValueError:
                    print(f"{R}[!] Invalid input.{W}")
                    continue

            for idx, t in targets_to_scan:
                save_progress(progress_file_path, {
                    "mode": "1",
                    "target_domain": domain,
                    "scanned_indices": list(scanned_indices)
                })
                process_single_recon(t, extra_flags, abs_base, master_vuln_file)
                scanned_indices.add(idx)
                save_progress(progress_file_path, {
                    "mode": "1",
                    "target_domain": domain,
                    "scanned_indices": list(scanned_indices)
                })

    clear_progress(progress_file_path)
    os.chdir(orig_dir)

def main():
    setup_alias()
    banner()
    extra_flags = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    prog_file, saved_data, found_folder = check_existing_sessions()
    if saved_data and prog_file:
        target_domain = saved_data.get("target_domain")
        print(f"{Y}[!] Unfinished session detected in '{C}{found_folder}{Y}' for target: {C}{target_domain}{W}")
        print(f"{Y}[?] Do you want to resume from where you left off? (y/n): {W}", end="")
        try:
            choice = input().strip().lower()
            if choice == 'y':
                scanned_indices = saved_data.get("scanned_indices", [])
                print(f"\n{G}[+] Resuming scan for {target_domain}...{W}")
                process_wildcard(target_domain, extra_flags, resume_indices=scanned_indices)
                return
            else:
                clear_progress(prog_file)
        except Exception:
            clear_progress(prog_file)

    clear_input_buffer()
    print(f"{C}{B}Select Operation Mode:{W}")
    print(f"{G}1.{W} Wildcard Mode (Multi Deep Scanning)")
    print(f"{G}2.{W} Domain Mode (Single Deep Scanning)")
    print(f"{C}{B}└─╼ {W}{Y}Choice {B}{C}>> {W}", end="", flush=True)
    
    try:
        rlist, _, _ = select.select([sys.stdin], [], [], 15)
        if rlist:
            mode = sys.stdin.readline().strip()
        else:
            print(f"\n{M}[!] Timeout. Selecting default Mode 1...{W}")
            mode = "1"
    except Exception:
        mode = "1"
        
    clear_input_buffer()
    print(f"\n{Y}[?] Enter Target Here (comma separated): {W}", end="")
    
    try:
        user_input = input().strip()
        if not user_input: 
            return
        targets = [t.strip() for t in user_input.split(',')]

        for t in targets:
            if mode == "1":
                process_wildcard(t, extra_flags)
            elif mode == "2":
                process_single_domain_mode(t, extra_flags)
                
    except KeyboardInterrupt:
        handle_interrupt()

if __name__ == "__main__":
    main()
