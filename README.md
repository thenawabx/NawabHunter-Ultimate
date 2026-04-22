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
sudo apt install amass -y
```
```bash
sudo apt install findomain -y
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
sudo apt install ffuf -y
```
```bash
sudo apt install naabu -y
```
```bash
sudo apt install waybackurls -y
```
```bash
sudo apt install gau -y
```
```bash
sudo apt install ParamSpider -y
```
```bash
sudo apt install katana -y
```
```bash
sudo apt install nuclei -y
```
```bash
sudo apt install python3 -y
```
```bash
sudo apt update --fix-missing && sudo apt install python3-pip -y && pip3 install uro --break-system-packages
```
```bash
sudo apt install git -y
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
**Press Ctrl + C and again:**
```bash
chmod +x scanner2.py
python3 scanner2.py
```
## ⚠️IMPORTANT: Press Ctrl + C after the banner appears to stop the script and activate the shortcut command.
**​6. Activate the shortcut command (Alias):**
```bash
source ~/.bashrc
```

### 🚀 How to Use:
**Once the setup is complete, you can launch the tool from anywhere in your terminal by simply typing the following command and entering your target:**

**For Wildcard**
```bash
nawab-run
```
**For Single Domain/Subdomain**
```bash
nawab-run2
```

### 🛠 Key Features in v0.0.0:
**1. ​Original Tool Output: Displays the raw, colorful UI and progress bars of Subfinder, Nuclei, and Httpx as they run.**
**2. ​Smart Skipping: Press Ctrl + C during any step to skip that specific tool and immediately move to the next point without stopping the entire process.**
**3. ​Organized Storage: Automatically creates a results folder named recon_target_com for every scan.**
​**4. Global Access: The nawab-run command works system-wide after the initial configuration.**


# NOTE: TorNet Automation - NawabHunter Ultimate

This script automates the process of changing your IP address every 3 seconds using **TorNet** on Kali Linux. It automatically configures your environment and sets up a global alias for easy access from any directory.

---

## 📋 Prerequisites
* Kali Linux 2026 or later.
* Python 3 and Pip installed.
* Active internet connection.

---

## 📥 Installation & Setup

Follow these steps to install and configure the automation tool:

**1. Navigate to the Directory**
**First, move to your Downloads folder:**
```bash
cd ~/Downloads
```
**2. Install Required Tools**
**​Install and start the Tor service, and set up the environment:**

```bash
sudo apt install tor -y
```
```bash

sudo systemctl start tor
```
```bash
sudo systemctl status tor
```
```bash
sudo apt install python3-pip -y
```

```bash
python3 -m venv ~/Downloads/NawabHunter-Ultimate/my_venv
```
```bash
source ~/Downloads/NawabHunter-Ultimate/my_venv/bin/activate
```
```bash
pip install tornet
```
**3. Run Automation Script**
**​Grant permission and execute the Python script to set up the global alias:**
```bash
chmod +x ~/Downloads/NawabHunter-Ultimate/autotor.py
```
```bash
python3 ~/Downloads/NawabHunter-Ultimate/autotor.py
```
**4. Apply Changes**
**​To make the shortcut work globally, refresh your shell configuration:**

**For Zsh**
```bash
source ~/.zshrc
```
**OR**

**For Bash**
```bash
source ~/.bashrc
```
### 🚀 Usage
**​Once the setup is complete, you can start the automatic IP changer from any terminal window by typing:**
```bash
start-tor
```
​### ⚙️ Browser Configuration
​To route your traffic through Tor, configure your browser (e.g., Firefox):
​Go to Settings > Network Settings.
​Select Manual Proxy Configuration.
​SOCKS Host: 127.0.0.1 | Port: 9050.
​Check the box: "Proxy DNS when using SOCKS v5".
​⚠️ Important Note
​Educational Purpose Only: This tool is created for ethical hacking and penetration testing purposes. Misusing it for illegal activities is strictly prohibited.


