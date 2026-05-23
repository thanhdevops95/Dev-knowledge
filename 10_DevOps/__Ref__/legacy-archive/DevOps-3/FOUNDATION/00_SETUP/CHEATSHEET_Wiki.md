# Cheatsheet: Module 00 - SETUP

> **Quick Reference cho Environment Setup**

---

## 🔧 WSL2 COMMANDS

```bash
# Install WSL
wsl --install

# Check version
wsl --version
wsl -l -v

# Set default distribution
wsl --set-default-version 2
wsl --set-default Ubuntu

# Update WSL
wsl --update

# Shutdown all WSL
wsl --shutdown

# Start Ubuntu
wsl
```

---

## 🐧 LINUX BASIC COMMANDS

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install essentials
sudo apt install -y git curl wget

# Check versions
git --version
python3 --version
node --version
```

---

## 📝 VS CODE

```bash
# Open VS Code in current directory
code .

# Open specific file
code filename.md

# Open folder
code /path/to/folder
```

**Essential Extensions:**

- Remote - WSL
- Docker
- GitLens
- YAML

---

## 🐳 DOCKER COMMANDS

```bash
# Check Docker running
docker --version
docker info

# Test Docker
docker run hello-world
```

---

## 🔍 VERIFICATION

```bash
# Run verification script
./scripts/verify-linux.sh

# Manual checks
echo $SHELL      # Should be /bin/bash or /bin/zsh
pwd              # Should show home directory
ls -la           # Should show files
```

---

## 🌐 ACCOUNTS NEEDED

- **GitHub:** github.com/signup
- **Docker Hub:** hub.docker.com/signup

---

## 📂 FOLDER STRUCTURE

```
~/DevOpsTraining/
├── FOUNDATION/
│   ├── 00_SETUP/
│   ├── 01_LINUX_BASICS/
│   └── ...
├── PROJECTS/
└── SHARED/
```

---

## ⚠️ COMMON ISSUES

| Issue | Solution |
|-------|----------|
| WSL not starting | `wsl --shutdown` then restart |
| Permission denied | `chmod +x script.sh` |
| Package not found | `sudo apt update` first |
| Docker not running | Start Docker Desktop |

---

**Setup complete = Ready for DevOps! 🚀**
