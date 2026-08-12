#!/usr/bin/env python3
import os
import sys
import subprocess
import time
import select
import signal
import json

G, Y, C, M, W, R, B = "\033[92m", "\033[93m", "\033[96m", "\033[95m", "\033[0m", "\033[91m", "\033[1m"

last_interrupt_time = 0
current_step_proc = None

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
    current_dir = os.getcwd()
    for item in os.listdir(current_dir):
        if item.startswith("recon_wildcard_") and os.path.isdir(item):
            prog_path = os.path.join(current_dir, item, ".nawab_progress.json")
            if os.path.exists(prog_path):
                data = load_progress(prog_path)
                if data and len(data.get("scanned_indices", [])) > 0:
                    return prog_path, data, item
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
    print(f"#           {Y}NAWAB HUNTER ULTIMATE v0.0.0{M}                     #")
    print(f"#             {C}MODE: ADVANCED RECON & INTEL{M}                   #")
    print(f"##############################################################{W}\n")
    print(f"{G}{B}          --- Welcome to 'thenawabx' world! ---{W}")
    print(f"{R}{B}   >>> PRESS Ctrl+C TO SKIP STEP | DOUBLE PRESS TO EXIT <<<{W}\n")

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
    global last_interrupt_time, current_step_proc
    current_time = time.time()
    if current_time - last_interrupt_time < 3:
        print(f"\n{R}[!] Emergency Shutdown Initiated. Exiting...{W}")
        sys.exit(0)
    else:
        last_interrupt_time = current_time
        print(f"\n{Y}[!] Step Skipped. Press again quickly to exit.{W}")
        if current_step_proc:
            try:
                os.killpg(os.getpgid(current_step_proc.pid), signal.SIGTERM)
            except Exception:
                pass

def run_step(name, target_info, cmd):
    global current_step_proc
    print("\n" + "-" * 70)
    print(f"{B}{C}┌──[{W}{M}{name}{W}{B}{C}] Target: {W}{G}{target_info}{W}")
    print(f"{B}{C}└─╼ {W}{Y}[ {cmd} ]{W}\n")

    try:
        current_step_proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
        current_step_proc.wait()
        print(f"\n{G}{B}[✓] {name} - COMPLETE{W}")
    except KeyboardInterrupt:
        if current_step_proc:
            try:
                os.killpg(os.getpgid(current_step_proc.pid), signal.SIGTERM)
            except Exception:
                pass
        handle_interrupt()
    finally:
        current_step_proc = None
    print("-" * 70 + "\n")

def write_to_master_report(master_file, target, step_label, file_source):
    if os.path.exists(file_source) and os.path.getsize(file_source) > 0:
        with open(master_file, "a") as f_master:
            f_master.write(f"TARGET: {target}\n")
            f_master.write(f"LINK/STEP: {step_label}\n")
            f_master.write("FINDINGS:\n")
            with open(file_source, "r") as f_out:
                f_master.write(f_out.read())
            f_master.write("\n------------------------------------------------------------\n")
        return True
    return False

def configure_tools():
    print(f"\n{C}[=== Tool Configuration Menu ===]{W}")
    print(f"{G}1.{W} RUN ALL TOOLS (Httpx, Katana, Wayback, Nmap, Nuclei)")
    print(f"{G}2.{W} RUN ESSENTIALS (Httpx, Katana, Nuclei - Recommended)")
    print(f"{G}3.{W} Custom Select (Manually pick each)")
    print(f"{Y}[?] Choice (Default '1' in 15s): {W}", end="", flush=True)

    try:
        rlist, _, _ = select.select([sys.stdin], [], [], 15)
        if rlist:
            choice = sys.stdin.readline().strip().lower()
        else:
            print(f"\n{M}[!] Timeout (15s). Auto-selecting Option 1.{W}")
            choice = "1"
    except Exception:
        choice = "1"

    tools = {'httpx': True, 'katana': True, 'waybackurls': True, 'nmap': True, 'nuclei': True}

    if choice == "2":
        tools['waybackurls'] = False
        tools['nmap'] = False
    elif choice == "3" or choice == "all":
        for tool in tools:
            ans = input(f"{G}Enable {tool}? [y/n]: {W}").lower()
            tools[tool] = (ans != 'n')

    print(f"\n{C}[+] Tool Configuration Saved!{W}\n")
    return tools

def filter_clean_urls(input_file, output_file):
    if not os.path.exists(input_file):
        return
    filtered_lines = []
    skip_exts = (
        '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.css', '.woff', 
        '.woff2', '.ttf', '.eot', '.pdf', '.mp4', '.mp3', '.avi', '.webp', 
        '.bmp', '.swf', '.json', '.xml'
    )
    with open(input_file, "r") as f:
        for line in f:
            l = line.strip()
            if not l:
                continue
            lower_l = l.lower()
            if any(lower_l.split('?')[0].endswith(ext) for ext in skip_exts):
                continue
            filtered_lines.append(l)
    
    with open(output_file, "w") as f:
        f.write("\n".join(filtered_lines) + "\n" if filtered_lines else "")

def process_single_recon(target, extra_flags, parent_dir, master_vuln_file, tools):
    clean_target = target.replace('https://', '').replace('http://', '').strip('/')
    folder_name = f"sub_{clean_target.replace('.', '_')}"
    sub_path = os.path.join(parent_dir, folder_name)

    if not os.path.exists(sub_path):
        os.makedirs(sub_path)

    orig_dir = os.getcwd()
    os.chdir(sub_path)

    t_path = os.path.expanduser("~/Downloads/NawabHunter-Ultimate/Nuclei_Templates")

    if tools.get('httpx', True):
        run_step("POINT 1: Live Probing", clean_target, f"echo {clean_target} | httpx-toolkit {extra_flags} -o live_sub.txt")

    if tools.get('katana', True):
        run_step("POINT 2: Katana Crawling", clean_target, f"katana -u {clean_target} -rl 10 -o katana_urls.txt")

    if tools.get('waybackurls', True):
        run_step("POINT 3: Wayback URLs", clean_target, f"echo {clean_target} | waybackurls | tee wayback_urls.txt")

    run_step("POINT 4: Smart Intel & Parameter Filtering", clean_target,
           f"cat wayback_urls.txt katana_urls.txt 2>/dev/null | sort -u > all_urls.txt; "
           f"grep '=' all_urls.txt > Equal_parameters.txt; "
           f"grep '\\.js' all_urls.txt > js_file.txt; "
           f"grep 'api' all_urls.txt > api_Information.txt; "
           f"grep -E 'package\\.json|composer\\.json|requirements\\.txt' all_urls.txt > dependency_files.txt; "
           f"grep -E '.env|.log|.sql|.conf' all_urls.txt > information_Disc.txt")

    filter_clean_urls("all_urls.txt", "filtered_clean_urls.txt")

    run_step("POINT 4.1: PAC & Config Detection", clean_target,
           f"grep -iE '\\.pac|\\.conf|\\.config' all_urls.txt > pac_config_files.txt; "
           f"if [ -s pac_config_files.txt ]; then "
           f"cat pac_config_files.txt | xargs -I{{}} curl -s -k \"{{}}\" | grep -iE 'FindProxyForURL|PROXY|DIRECT' > proxy_pac_findings.txt; "
           f"fi")

    run_step("POINT 4.2: JS Secrets Extraction", clean_target,
           f"if [ -s js_file.txt ]; then "
           f"cat js_file.txt | httpx-toolkit -silent | mantra -s > js_secrets.txt 2>/dev/null; "
           f"fi")

    run_step("POINT 4.3: Traceroute & IP Range Expansion", clean_target,
           f"traceroute -n {clean_target} 2>/dev/null | grep -E -o '([0-9]{{1,3}}\\.)[0-9]{{1,3}}\\.[0-9]{{1,3}}\\.[0-9]{{1,3}}' | sort -u > traceroute_ips.txt")

    if tools.get('nmap', True):
        run_step("POINT 4.4: Single Target Nmap Scan", clean_target,
           f"nmap -Pn -n -sV --top-ports 100 --open -T4 {clean_target} -oN nmap_result.txt > /dev/null 2>&1")

    found_in_target = False
    if tools.get('nuclei', True):
        nuclei_base = f"nuclei -t {t_path} -severity low,medium,high,critical -stats -rl 6 -c 3 {extra_flags}"

        n_tasks = [
            ("POINT 5: Nuclei (Dependency Confusion Check)", "dependency_files.txt", "nuclei_dependency.txt"),
            ("POINT 6: Nuclei (JS Intel)", "js_file.txt", "nuclei_js.txt"),
            ("POINT 7: Nuclei (API Intel)", "api_Information.txt", "nuclei_api.txt"),
            ("POINT 8: Nuclei (Info Disclosure)", "information_Disc.txt", "nuclei_info.txt"),
            ("POINT 9: Nuclei (LFI Check)", "Equal_parameters.txt", "nuclei_lfi.txt"),
            ("POINT 10: Nuclei (Sensitive Backup Check)", "filtered_clean_urls.txt", "nuclei_backup.txt")
        ]

        for label, src, out in n_tasks:
            if os.path.exists(src) and os.path.getsize(src) > 0:
                run_step(label, clean_target, f"{nuclei_base} -l {src} -o {out}")
                if write_to_master_report(master_vuln_file, clean_target, label, out):
                    found_in_target = True

    print("\n" + "="*60)
    os.chdir(orig_dir)

    if found_in_target:
        print(f"{G}{B}[+] INTEL / ASSETS FOUND on {clean_target}! Check Report: {master_vuln_file}{W}")
    else:
        print(f"{R}{B}[!] NO SIGNIFICANT INTEL FOUND on {clean_target}.{W}")
    print("="*60 + "\n")

def process_single_domain_mode(target_list, extra_flags, root_dir, tools):
    for target in target_list:
        clean_target = target.replace('https://', '').replace('http://', '').strip('/')
        folder_name = f"sub_{clean_target.replace('.', '_')}"
        abs_folder = os.path.abspath(folder_name)
        if not os.path.exists(abs_folder):
            os.makedirs(abs_folder)
        master_vuln_file = os.path.join(abs_folder, "Vulnerability_Report.txt")
        print(f"\n{G}[+] Processing Single Domain: {target}{W}")
        process_single_recon(target, extra_flags, os.path.abspath("recon_single_targets"), master_vuln_file, tools)

def process_wildcard(domain, extra_flags, root_dir, tools, resume_indices=None):
    base_folder = f"recon_wildcard_{domain.replace('.', '_')}"
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    abs_base = os.path.abspath(base_folder)
    master_vuln_file = os.path.join(abs_base, "Vulnerability_Report.txt")
    progress_file_path = os.path.join(abs_base, ".nawab_progress.json")

    orig_dir = os.getcwd()
    os.chdir(abs_base)

    if not os.path.exists("live_sub.txt") or os.path.getsize("live_sub.txt") == 0:
        run_step("POINT 1: Subdomain Enumeration", domain,
                 f"subfinder -d {domain} -o subfinder.txt; "
                 f"assetfinder --subs-only {domain} | tee assetfinder.txt;")

        run_step("POINT 2: Merge & Unique", domain, f"cat subfinder.txt assetfinder.txt 2>/dev/null | sort -u > all_subs.txt")
        run_step("POINT 3: DNS Resolution", domain, f"dnsx -l all_subs.txt {extra_flags} -o dnsx_resolved.txt")
        run_step("POINT 4: Web Probing", domain, f"cat dnsx_resolved.txt | httpx-toolkit -o live_sub.txt")
    else:
        print(f"\n{G}[+] Existing 'live_sub.txt' found. Skipping Subdomain Enumeration!{W}\n")

    scanned_indices = set(resume_indices) if resume_indices is not None else set()
    save_progress(progress_file_path, {
        "mode": "1",
        "target_domain": domain,
        "scanned_indices": list(scanned_indices)
    })

    if os.path.exists("live_sub.txt") and os.path.getsize("live_sub.txt") > 0:
        with open("live_sub.txt", "r") as f:
            domains = [l.strip().replace('https://', '').replace('http://', '').strip('/') for l in f if l.strip()]

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

            print(f"\n{Y}[?] Enter numbers (e.g: 1,2,5), '3' (All), or wait [Auto-Next in 15s]: {W}", end="", flush=True)

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
            elif choice == '3' or choice == 'all':
                targets_to_scan = [(idx, d) for idx, d in enumerate(domains) if idx not in scanned_indices]
            else:
                try:
                    indices = [int(x.strip()) - 1 for x in choice.split(',')]
                    for i in indices:
                        if 0 <= i < len(domains) and i not in scanned_indices:
                            targets_to_scan.append((i, domains[i]))
                    if not targets_to_scan:
                        targets_to_scan = [(idx, domains[idx]) for idx in range(len(domains)) if idx not in scanned_indices]
                except ValueError:
                    print(f"{R}[!] Invalid input. Defaulting to auto-select next.{W}")
                    for idx, d in enumerate(domains):
                        if idx not in scanned_indices:
                            targets_to_scan = [(idx, d)]
                            break

            for idx, t in targets_to_scan:
                process_single_recon(t, extra_flags, abs_base, master_vuln_file, tools)
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
    root_dir = os.getcwd()
    extra_flags = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    tools = configure_tools()

    prog_file, saved_data, found_folder = check_existing_sessions()
    if saved_data and prog_file:
        target_domain = saved_data.get("target_domain")
        print(f"{Y}[!] Unfinished session detected in '{C}{found_folder}{Y}' for target: {C}{target_domain}{W}")
        scanned_indices = saved_data.get("scanned_indices", [])
        print(f"\n{G}[+] Automatically resuming scan for {target_domain} from stopped session...{W}")
        process_wildcard(target_domain, extra_flags, root_dir, tools, resume_indices=scanned_indices)
        return

    clear_input_buffer()
    print(f"{C}{B}Select Operation Mode:{W}")
    print(f"{G}1.{W} Wildcard Mode (Multi Deep Recon / Subdomains)")
    print(f"{G}2.{W} Domain Mode (Single Deep Recon - Comma separated)")
    print(f"{C}{B}└─╼ {W}{Y}Choice [Default '1' in 15s] {B}{C}>> {W}", end="", flush=True)

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
    print(f"\n{Y}[?] Enter Target(s) Here (comma separated for multiple): {W}", end="")

    try:
        user_input = sys.stdin.readline().strip()
        if not user_input:
            return
        targets = [t.strip() for t in user_input.split(',')]

        if mode == "2":
            process_single_domain_mode(targets, extra_flags, root_dir, tools)
        else:
            for t in targets:
                print(f"\n{G}[+] Processing Wildcard Domain: {t}{W}")
                process_wildcard(t, extra_flags, root_dir, tools)

    except KeyboardInterrupt:
        handle_interrupt()

if __name__ == '__main__':
    main()
