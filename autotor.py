import os

def setup_tornet_automation():
    # Shortcut command name
    alias_name = "start-tor"
    
    # TorNet command with 3-second interval and unlimited count
    tornet_command = "tornet --interval 3 --count 0"
    
    home = os.path.expanduser("~")
    alias_line = f"alias {alias_name}='{tornet_command}'"

    # Checking .bashrc and .zshrc files
    for rc_file in [".bashrc", ".zshrc"]:
        path = os.path.join(home, rc_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            
            # Add alias if it doesn't already exist
            if f"alias {alias_name}=" not in content:
                with open(path, "a") as f:
                    f.write(f"\n# TorNet Automation\n{alias_line}\n")
                print(f"✅ {alias_name} setup successful in {rc_file}.")
            else:
                print(f"ℹ️ {alias_name} is already configured.")

if __name__ == "__main__":
    setup_tornet_automation()
