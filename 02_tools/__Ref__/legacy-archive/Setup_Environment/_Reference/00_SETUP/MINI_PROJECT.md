# MINI PROJECT - Module 00: SETUP

> **Project:** Automated Development Environment Setup
> **Difficulty:** ⭐⭐⭐☆☆ | **Time:** 3-4 hours

---

## 🎯 Project Overview

Create a fully automated setup script that configures a complete DevOps development environment from scratch on a fresh WSL2 Ubuntu installation.

### Learning Objectives

- Automate environment configuration
- Practice shell scripting
- Create reusable setup automation
- Document processes thoroughly

---

## 📋 Requirements

### Must Have Features

1. **System Updates**
   - Update apt packages
   - Upgrade existing packages
   - Install security updates

2. **Essential Tools Installation**
   - Git (latest version)
   - Node.js (LTS version)
   - Python 3.x
   - Docker (prepare for future modules)
   - curl, wget, nano, vim

3. **Git Configuration**
   - Set user name and email
   - Configure default branch (main)
   - Enable colored output
   - Set preferred editor

4. **SSH Setup**
   - Generate ED25519 key
   - Start ssh-agent automatically
   - Configure SSH config file

5. **Shell Enhancement**
   - Install Zsh
   - Install Oh My Zsh
   - Install Powerlevel10k theme
   - Configure useful plugins

6. **Aliases and Functions**
   - Create 15+ useful aliases
   - Add productivity functions
   - Source configuration files

7. **VS Code Integration**
   - List required extensions
   - Provide installation instructions

8. **Verification**
   - Health check script
   - Test all installations
   - Generate report

### Bonus Features

- Backup existing configurations before modifying
- Support for multiple Linux distributions
- Interactive mode (prompt for user preferences)
- Rollback capability
- Colored output and progress indicators

---

## 🏗️ Project Structure

```
devops-setup/
├── setup.sh              # Main setup script
├── config/
│   ├── .bashrc           # Bash configuration
│   ├── .zshrc            # Zsh configuration
│   ├── .gitconfig        # Git configuration
│   ├── ssh_config        # SSH configuration
│   └── aliases.sh        # Custom aliases
├── scripts/
│   ├── install-tools.sh  # Tool installation
│   ├── configure-git.sh  # Git setup
│   ├── setup-ssh.sh      # SSH setup
│   ├── install-zsh.sh    # Zsh installation
│   └── verify.sh         # Verification script
├── docs/
│   ├── README.md         # Project documentation
│   ├── USAGE.md          # Usage instructions
│   └── TROUBLESHOOTING.md
└── tests/
    └── test-setup.sh     # Test suite
```

---

## 📝 Implementation Guide

### Step 1: Main Setup Script

```bash
#!/bin/bash
# setup.sh - Main automated setup script

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Main execution
main() {
    log_info "Starting DevOps environment setup..."
    
    # Update system
    log_info "Updating system packages..."
    sudo apt update && sudo apt upgrade -y
    
    # Install tools
    log_info "Installing essential tools..."
    bash scripts/install-tools.sh
    
    # Configure Git
    log_info "Configuring Git..."
    bash scripts/configure-git.sh
    
    # Setup SSH
    log_info "Setting up SSH..."
    bash scripts/setup-ssh.sh
    
    # Install Zsh
    log_info "Installing Zsh and Oh My Zsh..."
    bash scripts/install-zsh.sh
    
    # Verify installation
    log_info "Verifying installation..."
    bash scripts/verify.sh
    
    log_info "Setup complete! 🎉"
    log_info "Please restart your terminal or run: source ~/.zshrc"
}

main "$@"
```

### Step 2: Tool Installation

```bash
#!/bin/bash
# scripts/install-tools.sh

# Install essential packages
sudo apt install -y \
    git \
    curl \
    wget \
    nano \
    vim \
    build-essential \
    software-properties-common

# Install Node.js (LTS)
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python
sudo apt install -y python3 python3-pip

echo "Tools installed successfully!"
```

### Step 3: Git Configuration

```bash
#!/bin/bash
# scripts/configure-git.sh

read -p "Enter your Git name: " GIT_NAME
read -p "Enter your Git email: " GIT_EMAIL

git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"
git config --global init.defaultBranch main
git config --global color.ui auto
git config --global core.editor nano

echo "Git configured successfully!"
```

### Step 4: SSH Setup

```bash
#!/bin/bash
# scripts/setup-ssh.sh

read -p "Enter your email for SSH key: " EMAIL

# Generate SSH key
ssh-keygen -t ed25519 -C "$EMAIL" -f ~/.ssh/id_ed25519 -N ""

# Start ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Display public key
echo "Your SSH public key:"
cat ~/.ssh/id_ed25519.pub

echo ""
echo "Add this key to GitHub: https://github.com/settings/keys"
```

### Step 5: Verification Script

```bash
#!/bin/bash
# scripts/verify.sh

echo "=== Environment Verification ==="
echo ""

# Check Git
if command -v git &> /dev/null; then
    echo "✓ Git: $(git --version)"
else
    echo "✗ Git not found"
fi

# Check Node.js
if command -v node &> /dev/null; then
    echo "✓ Node.js: $(node --version)"
else
    echo "✗ Node.js not found"
fi

# Check Python
if command -v python3 &> /dev/null; then
    echo "✓ Python: $(python3 --version)"
else
    echo "✗ Python not found"
fi

# Check SSH key
if [ -f ~/.ssh/id_ed25519 ]; then
    echo "✓ SSH key exists"
else
    echo "✗ SSH key not found"
fi

# Check Git config
if git config user.name &> /dev/null; then
    echo "✓ Git configured"
else
    echo "✗ Git not configured"
fi

echo ""
echo "Verification complete!"
```

---

## 🎓 Deliverables

### Required

1. **Working setup script** that runs without errors
2. **Documentation**:
   - README.md with project description
   - USAGE.md with installation instructions
   - TROUBLESHOOTING.md with common issues
3. **GitHub repository** with all code
4. **Demo video** showing:
   - Fresh WSL installation
   - Running setup script
   - Verification of all features
5. **Configuration files** that work on any machine

### Bonus

- Interactive prompts for customization
- Support for both Ubuntu and Debian
- Uninstall script
- Unit tests for each component
- GitHub Actions workflow for testing

---

## ✅ Acceptance Criteria

- [ ] Script runs on fresh WSL2 Ubuntu without errors
- [ ] All essential tools installed and verified
- [ ] Git properly configured
- [ ] SSH keys generated and agent running
- [ ] Zsh with Oh My Zsh installed
- [ ] 15+ useful aliases created
- [ ] VS Code integration documented
- [ ] Verification script passes all checks
- [ ] Documentation is complete and clear
- [ ] Code is on GitHub with good README

---

## 🚀 Stretch Goals

1. **Dotfiles Management**
   - Create dotfiles repository
   - Symlink configuration files
   - Version control all configs

2. **Multiple Profiles**
   - Web development profile
   - DevOps profile
   - Data science profile

3. **Auto-Update**
   - Check for updates
   - Update configurations
   - Migrate to new versions

4. **Backup & Restore**
   - Backup current config before changes
   - Restore from backup
   - Cloud sync of configurations

---

## 📚 Resources

- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [Oh My Zsh Documentation](https://github.com/ohmyzsh/ohmyzsh/wiki)
- [Git Configuration](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration)
- [SSH Key Generation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

## 💡 Tips

1. **Test frequently** - Don't wait until the end
2. **Use version control** - Commit after each feature
3. **Handle errors** - Use `set -e` and check return codes
4. **Add logging** - Help with debugging
5. **Make it idempotent** - Script should work if run multiple times
6. **Document as you go** - Don't leave it for the end

---

## 🎯 Grading Rubric

| Criteria | Points | Description |
|----------|--------|-------------|
| Functionality | 40 | Script works correctly |
| Code Quality | 20 | Clean, well-organized code |
| Documentation | 20 | Complete and clear docs |
| Error Handling | 10 | Proper error messages |
| Bonus Features | 10 | Extra functionality |
| **Total** | **100** | |

**Passing Score:** 70/100

---

## 🎉 Success Criteria

Your project is complete when:

1. Someone can use your script on fresh WSL
2. Setup completes in under 10 minutes
3. All tools work correctly
4. Documentation helps troubleshoot issues
5. You can demo it confidently

---

> **This project proves you can automate your dev environment! Ship it! 🚀**
