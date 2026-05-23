# SCENARIOS - Module 00: SETUP

> **Purpose:** Real-world troubleshooting and problem-solving
> **Format:** Problem-based learning scenarios
> **Difficulty:** ⭐⭐☆☆☆ to ⭐⭐⭐⭐☆

---

## Scenario 1: The Broken WSL Installation

### Situation

You've just installed WSL2 on your Windows machine, but when you try to run Ubuntu, you get an error:

```
WslRegisterDistribution failed with error: 0x80370102
Error: 0x80370102 The virtual machine could not be started because a required feature is not installed.
```

Your manager needs you to start working on a Linux-based project today.

### Your Task

1. Diagnose the problem
2. Fix the WSL installation
3. Verify Ubuntu works
4. Document the solution for teammates

### Hints

- Check Windows features
- Virtualization settings
- BIOS configuration

### Expected Solution

```powershell
# 1. Check if virtualization is enabled
systeminfo | find "Virtualization"

# 2. Enable required Windows features
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 3. Restart Windows
# 4. Set WSL 2 as default
wsl --set-default-version 2

# 5. If still fails, enable virtualization in BIOS
# Restart → Enter BIOS → Enable Intel VT-x or AMD-V → Save
```

### Learning Outcomes

- Troubleshoot WSL installation issues
- Understand virtualization requirements
- BIOS configuration basics

---

## Scenario 2: Git Configuration Nightmare

### Situation

You're trying to push code to GitHub, but every command fails:

```bash
$ git push
*** Please tell me who you are.

Run
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
```

You fix this, but then:

```bash
$ git push
Permission denied (publickey).
fatal: Could not read from remote repository.
```

Your deadline is in 2 hours!

### Your Task

1. Configure Git properly
2. Set up SSH authentication
3. Successfully push code
4. Create a checklist to avoid this in the future

### Expected Solution

```bash
# Step 1: Configure Git identity
git config --global user.name "John Doe"
git config --global user.email "john@company.com"

# Step 2: Generate SSH key
ssh-keygen -t ed25519 -C "john@company.com"

# Step 3: Start ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Step 4: Copy public key
cat ~/.ssh/id_ed25519.pub
# Add to GitHub: Settings → SSH Keys → New SSH key

# Step 5: Test connection
ssh -T git@github.com

# Step 6: Push code
git push -u origin main
```

### Checklist Created

```markdown
# Git Setup Checklist
- [ ] Git installed
- [ ] User name configured
- [ ] User email configured
- [ ] SSH key generated
- [ ] SSH key added to GitHub
- [ ] SSH connection tested
- [ ] Repository cloned via SSH (not HTTPS)
```

---

## Scenario 3: VS Code Won't Connect to WSL

### Situation

You installed VS Code and the Remote-WSL extension, but when you try to connect to WSL, you get:

```
Could not establish connection to WSL.
Failed to connect to the remote extension host server
```

Your team is waiting for you to review code in WSL environment.

### Your Task

1. Diagnose the connection issue
2. Fix VS Code-WSL integration
3. Verify you can open WSL folders
4. Test terminal works in WSL context

### Troubleshooting Steps

```bash
# 1. Check WSL is running
wsl --list --running

# 2. If not running, start it
wsl

# 3. In VS Code:
# F1 → "WSL: Connect to WSL"

# 4. If still fails, check WSL2
wsl --list --verbose
# If VERSION is 1, convert to 2:
wsl --set-version Ubuntu-22.04 2

# 5. Restart VS Code completely
# Close all windows, restart

# 6. Check extension installed
# Extensions → "Remote - WSL" → Ensure enabled

# 7. Try again
# F1 → "WSL: Connect to WSL"
```

### Verification

```bash
# In VS Code terminal (should show WSL):
uname -a
# Should show: Linux ... WSL2

# Check current directory
pwd
# Should be in WSL filesystem: /home/username

# Create test file
touch vscode-wsl-test.txt
# File should be in WSL, not Windows
```

---

## Scenario 4: The Missing Zsh Theme

### Situation

You installed Oh My Zsh and Powerlevel10k, but your prompt looks ugly and broken. Characters are showing as boxes, colors are wrong, and it looks nothing like the screenshots.

### Your Task

1. Fix the broken prompt
2. Configure Powerlevel10k properly
3. Install required fonts
4. Make it look professional

### Solution

```bash
# 1. Install Powerline fonts
# In Windows PowerShell (Admin):
# Download and install "MesloLGS NF" fonts from:
# https://github.com/romkatv/powerlevel10k#fonts

# 2. Configure Windows Terminal font
# Settings → Ubuntu profile → Appearance → Font face → "MesloLGS NF"

# 3. Run Powerlevel10k configuration
p10k configure

# 4. Answer prompts to customize
# Choose: Diamond → Unicode → 24-hour → Angled → Sharp → Flat → One line → Sparse → Few icons → Concise → Transient → Instant

# 5. Reload
source ~/.zshrc
```

---

## Scenario 5: Disk Space Crisis

### Situation

You're installing Docker when you get an error:

```
E: Failed to fetch ...
E: Unable to fetch some archives, maybe run apt-get update or try with --fix-missing?
No space left on device
```

Your Ubuntu WSL only has 100MB free, but you need to install Docker (2GB+ download).

### Your Task

1. Check disk usage
2. Clean up space
3. Resize WSL disk if needed
4. Complete Docker installation

### Solution

```bash
# 1. Check disk space
df -h
du -sh /* | sort -rh | head -10

# 2. Clean apt cache
sudo apt clean
sudo apt autoclean
sudo apt autoremove -y

# 3. Clean Docker (if installed)
docker system prune -af
docker volume prune -f

# 4. Find large files
find ~ -type f -size +100M -exec ls -lh {} \;

# 5. If still not enough, resize WSL disk
# In PowerShell (Admin):
wsl --shutdown
# Locate: %USERPROFILE%\AppData\Local\Packages\CanonicalGroupLimited...\LocalState\ext4.vhdx
# Use Diskpart to resize (advanced)

# Or move to different drive with more space
```

---

## Scenario 6: Multiple WSL Distributions Confusion

### Situation

You accidentally installed Ubuntu 20.04, Ubuntu 22.04, and Debian. Now you're confused about which one to use, and commands run in different distributions.

### Your Task

1. List all installed distributions
2. Choose the correct one
3. Set it as default
4. Remove unwanted distributions

### Solution

```powershell
# 1. List all distributions
wsl --list --verbose

# Output:
# * Ubuntu-20.04    Running    2
#   Ubuntu-22.04    Stopped    2
#   Debian          Stopped    2

# 2. Set Ubuntu-22.04 as default
wsl --set-default Ubuntu-22.04

# 3. Remove unwanted (backup data first!)
wsl --unregister Ubuntu-20.04
wsl --unregister Debian

# 4. Verify
wsl --list
# Should show only Ubuntu-22.04

# 5. Test
wsl
cat /etc/os-release
# Should show Ubuntu 22.04
```

---

## Scenario 7: The Corrupted .bashrc

### Situation

You edited `.bashrc` to add aliases, but made a syntax error. Now every time you open terminal, you get errors and half your commands don't work.

### Your Task

1. Fix the corrupted `.bashrc`
2. Restore to working state
3. Add aliases correctly
4. Create backup strategy

### Solution

```bash
# 1. Backup current (broken) .bashrc
cp ~/.bashrc ~/.bashrc.broken

# 2. Restore default .bashrc
cp /etc/skel/.bashrc ~/.bashrc

# 3. Or restore from backup if you had one
# cp ~/.bashrc.backup ~/.bashrc

# 4. Add aliases correctly
cat >> ~/.bashrc << 'EOF'

# Custom aliases
alias ll='ls -lah'
alias update='sudo apt update && sudo apt upgrade -y'
alias gs='git status'
EOF

# 5. Test syntax
bash -n ~/.bashrc
# No output = syntax OK

# 6. Apply changes
source ~/.bashrc

# 7. Create backup strategy
# Add to crontab or make regular backups
cp ~/.bashrc ~/.bashrc.backup.$(date +%Y%m%d)
```

---

## Scenario 8: GitHub Authentication Failure After Password Change

### Situation

You changed your GitHub password yesterday. Today, `git push` fails:

```
remote: Support for password authentication was removed on August 13, 2021.
fatal: Authentication failed
```

### Your Task

1. Understand the new authentication method
2. Set up Personal Access Token or SSH
3. Update repository remote
4. Successfully push code

### Solution Option 1: Personal Access Token

```bash
# 1. Generate token on GitHub
# Settings → Developer settings → Personal access tokens → Generate new token
# Select scopes: repo, workflow, write:packages
# Copy token (you'll only see it once!)

# 2. Update remote to use token
git remote set-url origin https://TOKEN@github.com/username/repo.git

# Or use credential helper
git config --global credential.helper store
# Next push will prompt for token, then save it
```

### Solution Option 2: Switch to SSH (Recommended)

```bash
# 1. Generate SSH key (if not exists)
ssh-keygen -t ed25519 -C "your-email@example.com"

# 2. Add to GitHub
cat ~/.ssh/id_ed25519.pub
# Copy and add to GitHub SSH keys

# 3. Change remote from HTTPS to SSH
git remote set-url origin git@github.com:username/repo.git

# 4. Test
git push
# Should work without password!
```

---

## Scenario 9: Terminal Performance is Terrible

### Situation

Your WSL terminal is extremely slow. Simple commands like `ls` take 2-3 seconds. Your productivity has dropped 80%.

### Your Task

1. Diagnose the slowness
2. Optimize WSL performance
3. Reduce startup time
4. Make terminal usable again

### Solution

```bash
# 1. Check what's running at startup
cat ~/.bashrc | grep -v "^#" | grep -v "^$"
cat ~/.zshrc | grep -v "^#" | grep -v "^$"

# 2. Disable slow plugins
# Edit ~/.zshrc
# Comment out slow plugins like:
# - git (if in large repos)
# - nvm (if not needed)
# - heavy themes

# 3. Optimize .wslconfig (Windows)
# Create: %USERPROFILE%\.wslconfig
[wsl2]
memory=4GB
processors=2
swap=2GB

# 4. Move project to WSL filesystem (not /mnt/c/)
# Projects in /mnt/c/ are MUCH slower
mv /mnt/c/Users/YourName/projects ~/projects

# 5. Disable Windows Defender for WSL folders
# Windows Security → Virus & threat protection → Exclusions
# Add: C:\Users\YourName\AppData\Local\Packages\CanonicalGroupLimited...

# 6. Restart WSL
wsl --shutdown
wsl
```

---

## Scenario 10: Team Onboarding Automation

### Situation

Your team is growing fast. Every new developer takes 3 hours to set up their environment, and they all ask the same questions. Your manager wants you to reduce this to 15 minutes.

### Your Task

1. Create automated setup script
2. Write clear documentation
3. Test on fresh WSL install
4. Train new hire using your solution

### Solution

```bash
#!/bin/bash
# team-setup.sh - Automated team onboarding

echo "🚀 Starting team environment setup..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install tools
sudo apt install -y git curl wget nano build-essential

# Install Node.js LTS
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Configure Git
read -p "Enter your name: " GIT_NAME
read -p "Enter your email: " GIT_EMAIL
git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"
git config --global init.defaultBranch main

# Generate SSH key
ssh-keygen -t ed25519 -C "$GIT_EMAIL" -f ~/.ssh/id_ed25519 -N ""
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Install company tools
# ... (add your company-specific tools)

# Display SSH public key
echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Add this SSH key to GitHub:"
cat ~/.ssh/id_ed25519.pub
echo ""
echo "2. Clone team repositories:"
echo "   git clone git@github.com:company/project.git"
```

---

## 🎯 Practice Method

For each scenario:

1. **Read the situation** carefully
2. **Try solving** without looking at solution
3. **Compare** your approach with provided solution
4. **Test** the solution on your system
5. **Document** what you learned

---

> **Master these scenarios → Production-ready troubleshooting skills!** 🔧
