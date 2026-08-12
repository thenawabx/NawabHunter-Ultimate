# NOTE : Automation recon scritp Only for testing purpose.

## NawabHunter-Ultimate
​⚠️ Disclaimer: This tool is for educational purposes and authorized security testing only. The developer (thenawabx) is not responsible for any misuse or damage caused by this tool. Always obtain written permission before scanning any target.
​
### 🦅 NAWAB HUNTER ULTIMATE v0.0.0
Nawab Hunter Ultimate is a powerful automated reconnaissance tool designed for comprehensive subdomain enumeration and advanced Nuclei vulnerability scanning. It streamlines the bug bounty workflow by integrating multiple industry-standard tools into a single execution.

​### 📥 Installation & Setup & Usage.
Follow these steps to set up the tool on your Kali Linux or NetHunter environment:

**​1. Navigate to the Downloads directory:**
```bash
cd ~/Downloads
```
​**2. Install required reconnaissance tools:**
**Note : If a tool is not installed this way, install it manually.**
```bash
sudo apt update --fix-missing -y && sudo apt install -y golang python3 git python3-pip curl pv jq traceroute nmap httpx-toolkit assetfinder && GOSUMDB=off go install github.com/projectdiscovery/katana/cmd/katana@latest && GOSUMDB=off go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest && GOSUMDB=off go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest && GOSUMDB=off go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest && GOSUMDB=off go install github.com/tomnomnom/waybackurls@latest && GOSUMDB=off go install github.com/brosck/mantra@latest && echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.zshrc 2>/dev/null; echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc 2>/dev/null; sudo cp ~/go/bin/* /usr/local/bin/ 2>/dev/null; source ~/.bashrc 2>/dev/null || source ~/.zshrc 2>/dev/null && sudo apt upgrade -y
```
​**3. Clone the core NawabHunter-Ultimate repository:**
```bash
git clone https://github.com/thenawabx/NawabHunter-Ultimate
```
**4. Now Here is an example of a custom template in the Nuclei_Templates folder. However, you can place your own nuclei templates or custom templates in the Nuclei_Templates folder by copying or moving them. Otherwise, that one template will work.**

**​5.Change Directory**
```bash
cd NawabHunter-Ultimate
```
**Configure and initialize the tool:**
```bash
chmod +x scanner.py
python3 scanner.py
```
## ⚠️IMPORTANT: Press Ctrl + C after the banner appears to stop the script and activate the shortcut command.
**​6. Activate the shortcut command (Alias):**
```bash
source ~/.bashrc
```

### 🚀 How to Use:
**Once the setup is complete, you can launch the tool from anywhere in your terminal by simply typing the following command and entering your target:**

**Run This Tools Every Times**
```bash
runawab
```

### 🛠 Key Features in v0.0.0:
**1. ​Original Tool Output: Displays the raw, colorful UI and progress bars of Subfinder, Nuclei, and Httpx as they run.**

**2. ​Smart Skipping: Press Ctrl + C during any step to skip that specific tool and immediately move to the next point without stopping the entire process.**

**3. ​Organized Storage: Automatically creates a results folder named recon_example_example... for every scan.**

​**4. Global Access: The Runawab command works system-wide after the initial configuration.**

# END...
