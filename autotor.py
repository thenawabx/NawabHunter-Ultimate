import os

def setup_alias():
    """Sets up a global alias 'start-tor' to automate TorNet with a virtual environment."""
    
    # 1. Configuration: Shortcut name and specific project path
    alias_name = "startor"
    
    # 2. Build the command: Enter directory, Activate Venv, and Run TorNet
    # The command uses '&&' to ensure each step succeeds before the next one runs.
    automation_command = f"source ~/Downloads/NawabHunter-Ultimate/my_venv/bin/activate && tornet --interval 3 --count 0"
    
    # 3. Locate the user's home directory and shell config files
    home = os.path.expanduser("~")
    alias_line = f"alias {alias_name}='{automation_command}'"

    # 4. Inject the alias into .bashrc or .zshrc if they exist
    updated = False
    for rc_file in [".bashrc", ".zshrc"]:
        path = os.path.join(home, rc_file)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            
            # Check if the alias is already present to avoid duplicates
            if f"alias {alias_name}=" not in content:
                with open(path, "a") as f:
                    f.write(f"\n# TorNet Automation Setup\n{alias_line}\n")
                print(f"✅ Success: {alias_name} shortcut added to {rc_file}")
                updated = True
            else:
                print(f"ℹ️ Info: Shortcut '{alias_name}' already exists in {rc_file}")

    # 5. Instructions for the user to apply changes
    if updated:
        print("\n" + "="*50)
        print("Setup completed successfully!")
        print("Run the following command to refresh your terminal:")
        print("source ~/.zshrc (or source ~/.bashrc)")
        print(f"\nThen, simply type '{alias_name}' from anywhere to start.")
        print("="*50)

# Main entry point with corrected dunder variable
if __name__ == "__main__":
    setup_alias()
