# NOTE : Only for wildcard(web) Target.

## NawabHunter-Ultimate
​⚠️ Disclaimer: This tool is for educational purposes and authorized security testing only. The developer (thenawabx) is not responsible for any misuse or damage caused by this tool. Always obtain written permission before scanning any target.
​
### 🦅 NAWAB HUNTER ULTIMATE v0.0.0
Nawab Hunter Ultimate is a powerful automated reconnaissance tool designed for comprehensive subdomain enumeration and advanced Nuclei vulnerability scanning. It streamlines the bug bounty workflow by integrating multiple industry-standard tools into a single execution.

​### 📥 Installation & Setup & Usage.
Follow these steps to set up the tool on your Kali Linux or NetHunter environment:

**​১. Navigate to the Downloads directory:**
```bash
cd ~/Downloads
```
​**২. Install required reconnaissance tools:**
```bash
sudo apt update
```
```bash
sudo apt install subfinder -y
```
```bash
sudo apt install assetfinder -y
```
```bash
sudo apt install sublist3r -y
```
```bash
sudo apt install dnsx -y
```
```bash
sudo apt install httpx-toolkit -y
```
```bash
sudo apt install subzy -y
```
```bash
sudo apt install waybackurls -y
```
```bash
sudo apt install python3 -y
```
```bash
sudo apt install git -y
```
​**৩. Clone the custom Nuclei templates:**
( Note: You can later move or copy your own custom templates into the Templates folder )
```bash
git clone https://github.com/thenawabx/Thenawabx_Nuclei_Templates.git
```
​**৪. Clone the core NawabHunter-Ultimate repository:**
```bash
git clone https://github.com/thenawabx/NawabHunter-Ultimate
```
**​৫. Configure and initialize the tool:**
```bash
cd NawabHunter-Ultimate
chmod +x scanner.py
python3 scanner.py
```
## ⚠️IMPORTANT: Press Ctrl + C after the banner appears to stop the script and activate the shortcut command.
**​৬. Activate the shortcut command (Alias):**
```bash
source ~/.bashrc
```

### 🚀 How to Use:
**Once the setup is complete, you can launch the tool from anywhere in your terminal by simply typing the following command and entering your target wildcard:**
```bash
nawab-run
```

### 🛠 Key Features in v0.0.0:
**1. ​Original Tool Output: Displays the raw, colorful UI and progress bars of Subfinder, Nuclei, and Httpx as they run.**
**2. ​Smart Skipping: Press Ctrl + C during any step to skip that specific tool and immediately move to the next point without stopping the entire process.**
**3. ​Organized Storage: Automatically creates a results folder named recon_target_com for every scan.**
​**4. Global Access: The nawab-run command works system-wide after the initial configuration.**
