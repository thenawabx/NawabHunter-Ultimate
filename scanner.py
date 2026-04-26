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
    print(f"#           {Y}NAWAB HUNTER ULTIMATE v0.0.0{M}                     #")
    print(f"#               {C}MODE: MASTER ELITE{M}                           #")
    print(f"##############################################################{W}\n")
    print(f"{G}{B}          --  Welcome to 'Thenawabx' world!  --{W}")
    print(f"{R}{B}          >>> PRESS Ctrl+C TO SKIP ANY STEP <<<{W}\n")

def setup_alias():
    """Sets up the global alias 'nawab-run' to point to this specific script."""
    script_path = os.path.abspath(file)
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
                    
def check_dependencies():
    tools = ["subfinder", "assetfinder", "sublist3r", "dnsx", "httpx-toolkit", "subzy", "katana", "waybackurls", "naabu", "uro", "nuclei", "ffuf"]
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
    base = f"recon_{target.replace('.', '_')}"
    dirs = ["subdomains", "urls", "vulnerability", "ports_fuzz"]
    for d in dirs:
        path = os.path.join(base, d)
        if not os.path.exists(path): os.makedirs(path)

    abs_path = os.path.abspath(base)
    orig_dir = os.getcwd()
    os.chdir(abs_path)

    print(f"\n{Y}{B}>>> STARTING MISSION: {target} <<<{W}\n")

    # --- 1. Recon ---
    print_section("1 Recon")
    run_step("1.1 subfinder", f"subfinder -d {target} -rl 10 {flags} -o subdomains/subfinder.txt")
    run_step("1.2 assetfinder", f"assetfinder --subs-only {target} | tee subdomains/assetfinder.txt")
    run_step("1.3 sublist3r", f"sublist3r -d {target} -o subdomains/sublist3r.txt")

    # --- 2. Merging ---
    print_section("2 Merging All Subdomains")
    run_step("2.1 Merging", f"cat subdomains/*.txt 2>/dev/null | sort -u > subdomains/all_subs.txt")

    # --- 3. Live Checkup ---
    print_section("3 Live Checkup")
    run_step("3.1 Dnsx", f"dnsx -l subdomains/all_subs.txt -rl 50 {flags} -o subdomains/dnsx_resolved.txt")
    run_step("3.2 httpx-toolkit", f"cat subdomains/dnsx_resolved.txt | httpx-toolkit -rl 20 {flags} -o subdomains/live_sub.txt")

    # --- 4. Takeover Check ---
    print_section("4 Takeover Check")
    run_step("4.1 code cheaker", f"cat subdomains/all_subs.txt | httpx-toolkit -mc 404,403,500,502,503 -rl 10 {flags} -o vulnerability/takeover_probe.txt")
    run_step("4.2 subzy", f"if [ -s vulnerability/takeover_probe.txt ]; then subzy run --targets vulnerability/takeover_probe.txt {flags} | tee vulnerability/sub_take_result.txt; fi")

    # --- 5. URL Collection ---
    print_section("5 Urls Collecting")
    run_step("5.1 katana crawling", f"katana -list subdomains/live_sub.txt -rl 10 | tee urls/katana_urls.txt")
    run_step("5.2 waybackurls", f"cat subdomains/live_sub.txt | waybackurls | tee urls/wayback_urls.txt")

    # --- 6. Scanning & Fuzzing ---
    print_section("6 Ports Scanning & Fuzzing")
    run_step("6.1 Naabu", f"naabu -host {target} -top-ports 100 -rate 500 -o ports_fuzz/open_ports.txt")
    wordlist = "/usr/share/dict/wordlist-probable.txt"
    if os.path.exists(wordlist):
        run_step("6.2 FFUF Fuzzing", f"ffuf -w {wordlist} -u https://{target}/FUZZ -mc 200,301,302,403 -t 10 -r -o ports_fuzz/ffuf_results.txt -or")

    # --- 7. Uro Filtering & Sorting ---
    print_section("7 Uro Filtering & Sorting")
    filter_cmd = (
        f"cat urls/wayback_urls.txt urls/katana_urls.txt 2>/dev/null | sort -u | uro | tee urls/all_urls.txt; "
        f"cat urls/all_urls.txt | grep '=' | tee urls/Equal_parameters.txt; "
        f"cat urls/all_urls.txt | grep '\\.js' | tee urls/js_file.txt; "
        f"cat urls/all_urls.txt | grep 'api' | tee urls/api_Information.txt; "
        f"cat urls/all_urls.txt | grep -E '.env|.log|.sql|.conf' | tee urls/information_Disc.txt"
    )
    run_step("7.1 URL Filtering", filter_cmd)

    # --- 8. Nuclei Scanning ---
    print_section("8 Nuclei Scanning")
    t_path = os.path.expanduser("~/Downloads/NawabHunter-Ultimate/Nuclei_Templates")
    nuclei_base = f"nuclei -t {t_path} -rl 6 -c 3 -stats {flags}" if os.path.exists(t_path) else f"nuclei -rl 6 -c 3 {flags}"

    tasks = [
        ("8.1 Live Subdomain", "subdomains/live_sub.txt", "vulnerability/nuclei_live.txt", True),
        ("8.2 Equal Parameters", "urls/Equal_parameters.txt", "vulnerability/nuclei_params.txt", True),
        ("8.3 JS Files", "urls/js_file.txt", "vulnerability/nuclei_js.txt", False),
        ("8.4 API Info", "urls/api_Information.txt", "vulnerability/nuclei_api.txt", False),
        ("8.5 Info Discovery", "urls/information_Disc.txt", "vulnerability/nuclei_info.txt", False),
        ("8.6 Katana Urls", "urls/katana_urls.txt", "vulnerability/katana_urls.txt", False)
    ]

    for label, src, out, fuzz in tasks:
        if os.path.exists(src) and os.path.getsize(src) > 0:
            f_opt = "-fuzz" if fuzz else ""
            run_step(label, f"{nuclei_base} -l {src} {f_opt} -o {out}")

    # --- FINAL RESULTS ---
    master = "FINAL_RESULT_BY_THENAWABX.txt"
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
    print(f"\n{C}{B}┌──({W}{G}Target Input{W}{B}{C})\n└─╼ {Y}Please Enter your Target (wildcard) Comma separated {B}{C}>> {W}", end="")
    try:
        user_input = input().strip()
        if not user_input: sys.exit(0)
        targets = [t.strip() for t in user_input.split(',')]
        for t in targets:
            if t: process_recon(t, flags)
    except KeyboardInterrupt:
        print(f"\n{R}[!] System Interrupted. Exiting...{W}")
        sys.exit(0)

if __name__ == "__main__":
    main()
