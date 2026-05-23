# EXERCISES - Module 00: SETUP

> **Purpose:** Practice environment setup skills
>
> **Difficulty:** ⭐☆☆☆☆ to ⭐⭐☆☆☆
>
> **Time:** 2-3 hours

---

## Exercise Categories

1. **Basic Setup** (1-5): Essential environment configuration
2. **Verification** (6-10): Testing and troubleshooting
3. **Advanced** (11-15): Customization and optimization

---

## Basic Setup Exercises

### Exercise 1: WSL2 Configuration Check

**Difficulty:** ⭐☆☆☆☆

Verify your WSL2 installation is properly configured.

**Tasks:**

1. Check WSL version
2. Verify virtualization is enabled
3. Confirm Ubuntu 22.04 is installed
4. Check kernel version

**Expected Commands:**

```bash
wsl --version
wsl --list --verbose
uname -r
cat /etc/os-release
```

**Success Criteria:**

- WSL version 2.x.x displayed
- Ubuntu running with VERSION 2
- Kernel contains `-microsoft-standard-WSL2`
- OS shows Ubuntu 22.04 LTS

---

### Exercise 2: Git Configuration

**Difficulty:** ⭐☆☆☆☆

Configure Git with proper identity and settings.

**Tasks:**

1. Set global username
2. Set global email
3. Set default branch to 'main'
4. Enable colored output
5. Set nano as default editor

**Commands to Use:**

```bash
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
git config --global init.defaultBranch main
git config --global color.ui auto
git config --global core.editor nano
```

**Verification:**

```bash
git config --global --list
```

**Success Criteria:**

- All 5 settings appear in output
- No errors when running commands

---

### Exercise 3: SSH Key Generation & GitHub

**Difficulty:** ⭐⭐☆☆☆

Create SSH keys and connect to GitHub.

**Tasks:**

1. Generate ED25519 SSH key
2. Add key to ssh-agent
3. Copy public key
4. Add to GitHub account
5. Test connection

**Commands:**

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
ssh -T git@github.com
```

**Success Criteria:**

- `ssh -T git@github.com` returns: "Hi username! You've successfully authenticated"

---

### Exercise 4: VS Code Setup

**Difficulty:** ⭐☆☆☆☆

Install and configure VS Code for DevOps work.

**Tasks:**

1. Install VS Code
2. Install Remote-WSL extension
3. Connect to WSL from VS Code
4. Verify terminal runs in WSL
5. Create test file in WSL

**Verification Steps:**

1. Open VS Code
2. Press F1 → "WSL: Connect to WSL"
3. New window shows "WSL: Ubuntu-22.04" (bottom left)
4. Terminal → New Terminal shows bash prompt
5. Create `test.txt` → verify it exists in WSL: `ls ~/test.txt`

**Success Criteria:**

- VS Code connected to WSL
- Terminal runs Ubuntu bash
- Files created in WSL filesystem

---

### Exercise 5: Oh My Zsh Installation

**Difficulty:** ⭐⭐☆☆☆

Install and configure Oh My Zsh with Powerlevel10k theme.

**Tasks:**

1. Install Zsh
2. Install Oh My Zsh
3. Set Zsh as default shell
4. Install Powerlevel10k theme
5. Configure 3 useful plugins

**Commands:**

```bash
sudo apt install zsh -y
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
# After installation, configure theme and plugins
```

**Success Criteria:**

- Prompt shows Powerlevel10k theme
- Plugins work (test with `z` command after visiting directories)
- Shell prompt is colorful and informative

---

## Verification Exercises

### Exercise 6: Environment Health Check

**Difficulty:** ⭐⭐☆☆☆

Run comprehensive environment health check.

**Tasks:**
Create a script that checks:

1. Git installation & config
2. SSH keys exist
3. VS Code can connect to WSL
4. Zsh is default shell
5. Required tools installed (curl, wget, nano)

**Script Template:**

```bash
#!/bin/bash
echo "=== Environment Health Check ==="

# Check Git
if command -v git &> /dev/null; then
    echo "✓ Git: $(git --version)"
else
    echo "✗ Git not found"
fi

# Check SSH keys
if [ -f ~/.ssh/id_ed25519 ]; then
    echo "✓ SSH key exists"
else
    echo "✗ SSH key missing"
fi

# Add more checks...
```

**Success Criteria:**

- All checks pass with ✓
- Script runs without errors

---

### Exercise 7: Troubleshooting Practice

**Difficulty:** ⭐⭐☆☆☆

Fix common setup issues.

**Simulated Issues:**

1. **Issue:** Git commands fail with "Please tell me who you are"
   - **Task:** Configure user.name and user.email

2. **Issue:** SSH to GitHub fails
   - **Task:** Check SSH key, agent, and GitHub configuration

3. **Issue:** VS Code can't connect to WSL
   - **Task:** Verify WSL is running, restart if needed

4. **Issue:** Command not found errors
   - **Task:** Check PATH, reinstall packages

**Success Criteria:**

- Able to identify and fix each issue
- Document solution steps

---

### Exercise 8: Performance Verification

**Difficulty:** ⭐⭐☆☆☆

Verify system meets performance requirements.

**Tasks:**

1. Check CPU count: `nproc`
2. Check RAM: `free -h`
3. Check disk space: `df -h`
4. Test WSL2 performance: copy large file, measure time

**Benchmarks:**

```bash
# Create test file
dd if=/dev/zero of=testfile bs=1M count=1000

# Measure copy time
time cp testfile testfile2

# Clean up
rm testfile testfile2
```

**Success Criteria:**

- At least 2 CPU cores
- At least 4GB RAM available
- At least 20GB free disk space
- File copy completes in reasonable time

---

### Exercise 9: Backup Configuration

**Difficulty:** ⭐⭐☆☆☆

Create backup of your configuration files.

**Tasks:**

1. Create backup directory
2. Copy `.bashrc`, `.zshrc`, `.gitconfig`
3. Backup SSH keys (private key securely!)
4. Create restore script
5. Test restore on clean system

**Script:**

```bash
#!/bin/bash
BACKUP_DIR=~/config-backup
mkdir -p $BACKUP_DIR

cp ~/.bashrc $BACKUP_DIR/
cp ~/.zshrc $BACKUP_DIR/ 2>/dev/null
cp ~/.gitconfig $BACKUP_DIR/
# Add more files...

echo "Backup complete: $BACKUP_DIR"
```

**Success Criteria:**

- All config files backed up
- Can restore to working state
- Script runs without errors

---

### Exercise 10: Documentation

**Difficulty:** ⭐⭐☆☆☆

Document your setup for future reference or team members.

**Tasks:**
Create a `SETUP-NOTES.md` file with:

1. OS version and specs
2. Installed tools and versions
3. Configuration settings
4. Custom aliases and functions
5. Troubleshooting tips learned

**Template:**

```markdown
# My DevOps Setup

## System Info
- OS: Ubuntu 22.04 LTS (WSL2)
- RAM: 8GB
- CPU: 4 cores

## Installed Tools
- Git: 2.34.1
- Node.js: 18.x
- Docker: (to be installed)

## Custom Configuration
- Default shell: Zsh
- Theme: Powerlevel10k
- Editor: VS Code

## Helpful Aliases
```bash
alias ll='ls -lah'
alias gs='git status'
```

## Common Issues & Solutions

1. WSL not starting: `wsl --shutdown` then restart
...

```

**Success Criteria:**
- Well-formatted documentation
- Includes all key information
- Useful for reference

---

## Advanced Exercises

### Exercise 11: Custom Aliases
**Difficulty:** ⭐⭐☆☆☆

Create useful aliases for common tasks.

**Tasks:**
Create aliases for:
1. Quick directory navigation
2. Git shortcuts
3. Docker commands (prepare for future)
4. System information
5. Network testing

**Example:**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias ll='ls -lah'
alias gs='git status'
alias gp='git push'
alias gc='git commit -m'
alias dps='docker ps'
alias sysinfo='echo "CPU: $(nproc), RAM: $(free -h | grep Mem | awk "{print $2}")"'
```

**Success Criteria:**

- At least 10 useful aliases created
- All aliases work correctly
- Documented in a file

---

### Exercise 12: Dotfiles Repository

**Difficulty:** ⭐⭐⭐☆☆

Create a dotfiles repository for version control.

**Tasks:**

1. Create GitHub repo "dotfiles"
2. Move config files to repo
3. Create symlinks
4. Create install script
5. Test on clean WSL instance

**Structure:**

```
dotfiles/
├── .bashrc
├── .zshrc
├── .gitconfig
├── install.sh
└── README.md
```

**Success Criteria:**

- Configs version controlled
- Easy to deploy on new machine
- Documented process

---

### Exercise 13: Windows Terminal Customization

**Difficulty:** ⭐⭐☆☆☆

Customize Windows Terminal for productivity.

**Tasks:**

1. Set Ubuntu as default profile
2. Customize color scheme
3. Add useful key bindings
4. Configure split panes
5. Set up custom background

**Settings to Modify:**

```json
{
    "defaultProfile": "{Ubuntu GUID}",
    "schemes": [...],
    "keybindings": [
        { "command": "splitPane", "keys": "alt+shift+d" }
    ]
}
```

**Success Criteria:**

- Terminal looks professional
- Productive key bindings
- Easy to use

---

### Exercise 14: Startup Automation

**Difficulty:** ⭐⭐⭐☆☆

Automate WSL2 startup tasks.

**Tasks:**

1. Create startup script
2. Start ssh-agent automatically
3. Load environment variables
4. Display system info
5. Add to `.bashrc` or `.zshrc`

**Script:**

```bash
# In ~/.bashrc or ~/.zshrc

# Start ssh-agent
if ! pgrep -u "$USER" ssh-agent > /dev/null; then
    eval "$(ssh-agent -s)" > /dev/null
fi

# Load SSH keys
if [ -f ~/.ssh/id_ed25519 ]; then
    ssh-add ~/.ssh/id_ed25519 2>/dev/null
fi

# Welcome message
echo "Welcome back, $(whoami)!"
echo "System uptime: $(uptime -p)"
```

**Success Criteria:**

- Scripts run on shell start
- No errors
- Improves productivity

---

### Exercise 15: Multi-Environment Setup

**Difficulty:** ⭐⭐⭐☆☆

Configure multiple development environments.

**Tasks:**

1. Install multiple WSL distributions
2. Configure each for different purpose
3. Create quick-switch mechanism
4. Document use cases

**Example:**

- Ubuntu 22.04: Primary development
- Debian: Testing
- Alpine: Lightweight tasks

**Success Criteria:**

- Multiple distros working
- Easy to switch between them
- Each properly configured

---

## 🎯 Challenge Exercises

### Challenge 1: Full Setup Automation

**Difficulty:** ⭐⭐⭐⭐☆

Create a fully automated setup script.

**Goal:** Run one script to set up complete environment.

**Script should:**

1. Install all required packages
2. Configure Git, SSH, Zsh
3. Install VS Code extensions
4. Set up dotfiles
5. Create project directories
6. Verify everything works

**Success Criteria:**

- Single command setup
- Works on fresh WSL install
- No manual intervention needed

---

### Challenge 2: Setup Testing Framework

**Difficulty:** ⭐⭐⭐⭐☆

Create tests to verify setup.

**Tasks:**

1. Write test suite for environment
2. Check all tools installed
3. Verify configurations
4. Test integrations (Git-GitHub, VS Code-WSL)
5. Generate report

**Example Test:**

```bash
#!/bin/bash
test_git_config() {
    if git config user.name &> /dev/null; then
        echo "PASS: Git configured"
    else
        echo "FAIL: Git not configured"
    fi
}

test_git_config
# Add more tests...
```

**Success Criteria:**

- Comprehensive test coverage
- Clear pass/fail reporting
- Easy to run

---

## 📝 Submission Checklist

For course completion, submit:

- [ ] Screenshots of working environment
- [ ] Git config output
- [ ] GitHub SSH connection test
- [ ] VS Code connected to WSL
- [ ] Zsh with Powerlevel10k theme
- [ ] Custom aliases/functions
- [ ] Environment health check results
- [ ] Documentation (SETUP-NOTES.md)

---

## 💡 Tips for Success

1. **Take notes** - Document issues and solutions
2. **Screenshot everything** - Proof of completion
3. **Backup configs** - Before making changes
4. **Test thoroughly** - Verify each step works
5. **Ask for help** - When stuck (forums, Discord)

---

> **Completed all exercises? You're ready for Module 01!** 🚀
