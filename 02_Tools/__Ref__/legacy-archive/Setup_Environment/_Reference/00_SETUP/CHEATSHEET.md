# CHEATSHEET - Module 00: SETUP

Quick reference for environment setup commands.

---

## WSL2 Commands

```bash
# Check WSL version
wsl --version
wsl --list --verbose

# Set default version
wsl --set-default-version 2

# Set default distribution
wsl --set-default Ubuntu-22.04

# Shutdown WSL
wsl --shutdown

# Update WSL
wsl --update
```

---

## Git Configuration

```bash
# Set identity
git config --global user.name "Your Name"
git config --global user.email "email@example.com"

# Settings
git config --global init.defaultBranch main
git config --global color.ui auto
git config --global core.editor nano

# View config
git config --global --list
git config --show-origin user.name
```

---

## SSH Keys

```bash
# Generate key
ssh-keygen -t ed25519 -C "email@example.com"

# Start agent
eval "$(ssh-agent -s)"

# Add key
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Test GitHub
ssh -T git@github.com
```

---

## VS Code

```bash
# Install extensions from CLI
code --install-extension ms-vscode-remote.remote-wsl
code --install-extension ms-python.python
code --install-extension dbaeumer.vscode-eslint

# Open folder in VS Code
code .

# Connect to WSL
# F1 → "WSL: Connect to WSL"
```

---

## Zsh & Oh My Zsh

```bash
# Install Zsh
sudo apt install zsh

# Install Oh My Zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Change default shell
chsh -s $(which zsh)

# Edit config
nano ~/.zshrc

# Reload config
source ~/.zshrc
```

---

## Useful Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias ll='ls -lah'
alias la='ls -A'
alias gs='git status'
alias gp='git push'
alias gc='git commit -m'
alias gco='git checkout'
alias update='sudo apt update && sudo apt upgrade -y'
```

---

## Troubleshooting

```bash
# Fix "Please tell me who you are"
git config --global user.name "Name"
git config --global user.email "email"

# SSH agent not running
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# VS Code can't connect to WSL
wsl --shutdown
# Then restart WSL

# Permission denied
sudo chmod +x filename
```

---

## Quick Setup Script

```bash
#!/bin/bash
# Essential setup

# Update system
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y git curl wget nano zsh

# Configure Git
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
git config --global init.defaultBranch main

# Generate SSH key
ssh-keygen -t ed25519 -C "email@example.com" -N "" -f ~/.ssh/id_ed25519

echo "Setup complete!"
echo "Add SSH public key to GitHub:"
cat ~/.ssh/id_ed25519.pub
```

---

> **Bookmark this page for quick reference!** �
