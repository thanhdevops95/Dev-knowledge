# Labs: Module 00 - SETUP

> **Hướng dẫn từng bước cài đặt môi trường**

---

## 🎯 Lab Objectives

Sau khi hoàn thành labs này, bạn sẽ có:

- ✅ Môi trường terminal sẵn sàng
- ✅ VS Code configured
- ✅ Tài liệu khóa học downloaded
- ✅ Tài khoản GitHub và Docker Hub
- ✅ Verified mọi thứ hoạt động

---

## 📋 Prerequisites

- Máy tính với Windows 10+ / macOS 11+ / Linux
- Quyền administrator
- Kết nối internet (tốc độ tối thiểu 5 Mbps)
- 20GB+ disk space

---

## 🪟 Lab Group A: Windows Users

### Lab A1: Install WSL2

**Time:** 15-20 minutes

#### Step 1: Check Windows version

```powershell
# Open PowerShell (no admin needed)
winver
```

**Expected:** Version 2004+ or Windows 11

**If older:** Update Windows first

```
Settings → Update & Security → Check for updates
```

#### Step 2: Install WSL2

```powershell
# Open PowerShell AS ADMINISTRATOR
# (Right-click Start → PowerShell (Admin))

wsl --install
```

**Expected output:**

```
Installing: Windows Subsystem for Linux
Installing: Virtual Machine Platform
Downloading: Ubuntu
```

⚠️ **MUST restart computer after this!**

#### Step 3: First Ubuntu setup

After restart, Ubuntu terminal opens automatically.

```bash
# When asked:
Enter new UNIX username: [your-name]  # lowercase, no spaces
New password: [type password - won't show anything!]
Retype new password: [type again]
```

**Verification:**

```bash
whoami
# Should show your username

pwd
# Should show /home/your-username
```

✅ **Success:** You see bash prompt: `username@COMPUTER:~$`

---

### Lab A2: Install Windows Terminal

**Time:** 5 minutes

#### Method 1: Microsoft Store

```
1. Open Microsoft Store
2. Search "Windows Terminal"
3. Click "Get" / "Install"
4. Wait for installation
5. Launch "Windows Terminal"
```

#### Method 2: winget

```powershell
# In PowerShell:
winget install Microsoft.Windows Terminal
```

**Set as default:**

```
1. Open Windows Terminal
2. Click down arrow next to tab
3. Settings
4. Startup → Default profile → Ubuntu
5. Save
```

**Test:**

```
Close and reopen Windows Terminal
→ Should open Ubuntu by default
```

✅ **Success:** Opens Ubuntu terminal directly

---

### Lab A3: Install VS Code + Remote WSL

**Time:** 10 minutes

#### Part 1: Install VS Code

```
1. Visit: https://code.visualstudio.com
2. Click "Download for Windows"
3. Run installer (VSCodeUserSetup-xxx.exe)
4. IMPORTANT: Check ✅ "Add to PATH"
5. Finish installation
```

#### Part 2: Install Remote - WSL extension

```
1. Open VS Code
2. Click Extensions icon (left sidebar, or Ctrl+Shift+X)
3. Search "Remote - WSL"
4. Click "Install" on extension by Microsoft
5. Wait for installation
```

#### Part 3: Test integration

```bash
# In Ubuntu terminal:
cd ~
mkdir test-vscode-wsl
cd test-vscode-wsl
code .
```

**Expected:**

- VS Code opens
- Bottom-left shows: "WSL: Ubuntu"
- First time: Installs VS Code Server (wait 1-2 min)

**Create test file:**

```bash
# In VS Code terminal (Ctrl+`):
echo "Hello from WSL!" > test.txt
cat test.txt
```

✅ **Success:** File created AND can read in VS Code

---

## 🍎 Lab Group B: macOS Users

### Lab B1: Setup Mac Terminal

**Time:** 2 minutes

Mac already has Terminal!

**Open Terminal:**

```
Cmd+Space → type "Terminal" → Enter
```

**Test:**

```bash
echo "Hello DevOps!"
# Output: Hello DevOps!

pwd  
# Output: /Users/your-username
```

✅ **Success:** Commands work

---

### Lab B2: Install Homebrew

**Time:** 10 minutes

```bash
# Paste this in Terminal:
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**During installation:**

- Will ask for macOS password → type it (won't show)
- Takes 5-10 minutes
- Read messages carefully

**After install, run commands shown** (usually):

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

**Verify:**

```bash
brew --version
# Expected: Homebrew 4.x.x
```

✅ **Success:** Homebrew version displays

---

### Lab B3: Install VS Code

**Time:** 5 minutes

#### Option 1: Direct download

```
1. Visit: https://code.visualstudio.com
2. Download for macOS
3. Open .dmg file
4. Drag VS Code to Applications
```

#### Option 2: Homebrew

```bash
brew install --cask visual-studio-code
```

**Setup `code` command:**

```bash
# Open VS Code
# Cmd+Shift+P (Command Palette)
# Type: "Shell Command: Install"
# Click "Shell Command: Install 'code' command in PATH"
```

**Test:**

```bash
cd ~
mkdir test-vscode
cd test-vscode
code .
```

✅ **Success:** VS Code opens the folder

---

## 🐧 Lab Group C: Linux Users

### Lab C1: Update System

**Time:** 5-10 minutes

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt upgrade -y
```

#### Fedora

```bash
sudo dnf upgrade -y
```

**Verify:**

```bash
lsb_release -a
# Check version is recent
```

---

### Lab C2: Install VS Code

**Time:** 5 minutes

#### Ubuntu/Debian

```bash
# Download .deb
wget -O vscode.deb 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'

# Install
sudo dpkg -i vscode.deb

# Fix dependencies if needed
sudo apt install -f

# Verify
code --version
```

#### Fedora

```bash
# Add Microsoft repo
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'

# Install
sudo dnf install code

# Verify
code --version
```

✅ **Success:** Version number shows

---

## 📥 Lab D: Download Course Materials (ALL OS)

### Lab D1: Download via Browser

**Time:** 5 minutes

**Step 1: Visit GitHub**

```
Browser → https://github.com/thanhlehoang0107/DevOpsTraining
```

**Step 2: Download ZIP**

```
1. Click green "Code" button
2. Click "Download ZIP"
3. Wait for download (~50-100MB)
```

**Step 3: Extract**

**Windows:**

```
1. Open File Explorer
2. Go to Downloads folder
3. Right-click DevOpsTraining-main.zip
4. "Extract All" → choose C:\DevOps\
```

**macOS:**

```bash
# ZIP auto-extracts in Downloads
# Move to home:
mkdir -p ~/DevOps
mv ~/Downloads/DevOpsTraining-main ~/DevOps/DevOpsTraining
```

**Linux:**

```bash
mkdir -p ~/DevOps
cd ~/DevOps
unzip ~/Downloads/DevOpsTraining-main.zip
mv DevOpsTraining-main DevOpsTraining
```

**Step 4: Verify structure**

```bash
# Windows (in WSL):
cd /mnt/c/DevOps/DevOpsTraining
ls

# macOS/Linux:
cd ~/DevOps/DevOpsTraining
ls
```

**Expected output:**

```
FOUNDATION/  ADVANCED/  PROJECTS/  SHARED/  README.md  LICENSE  ...
```

✅ **Success:** All folders visible

---

### Lab D2 (Alternative): Download via Command Line

**Time:** 3 minutes

```bash
# Create directory
mkdir -p ~/DevOps
cd ~/DevOps

# Download ZIP
wget https://github.com/thanhlehoang0107/DevOpsTraining/archive/refs/heads/main.zip

# OR use curl:
# curl -L -O https://github.com/thanhlehoang0107/DevOpsTraining/archive/refs/heads/main.zip

# Extract
unzip main.zip

# Rename
mv DevOpsTraining-main DevOpsTraining

# Cleanup
rm main.zip

# Verify
cd DevOpsTraining
ls -la
```

✅ **Success:** Same output as D1

---

## 👤 Lab E: Create Accounts (ALL OS)

### Lab E1: GitHub Account

**Time:** 10 minutes

**Step 1: Sign up**

```
1. Browser → https://github.com
2. Click "Sign up"
3. Enter email (use real email!)
4. Create password (strong!)
5. Choose username (keep it professional)
```

**Tips for username:**

- ✅ Good: john-smith, thanh-dev, devops-learner
- ❌ Avoid: xXx_c00l_guy_xXx, random123456

**Step 2: Verify email**

```
1. Check your email inbox
2. Click verification link from GitHub
3. Return to GitHub
```

**Step 3: Complete profile**

```
1. Click avatar → Settings
2. Upload a avatar (can be cartoon/abstract)
3. Add bio: "DevOps Engineer in training"
4. Add location (optional)
```

**Verification:**

Visit: `https://github.com/YOUR-USERNAME`

See your profile page? ✅ Success!

---

### Lab E2: Docker Hub Account

**Time:** 5 minutes

```
1. Browser → https://hub.docker.com
2. Click "Sign up"
3. Fill:
   - Docker ID: [same as GitHub username recommended]
   - Email: [same email as GitHub]
   - Password: [create strong password]
4. Verify email
```

**Verification:**

Visit: `https://hub.docker.com/u/YOUR-DOCKER-ID`

✅ **Success:** Profile page loads

---

### Lab E3: Save Account Info

**Time:** 3 minutes

```bash
# Create a file to remember (DON'T commit this!)
cd ~/DevOps
nano my-accounts.txt
```

**Content:**

```
DEVOPS TRAINING - ACCOUNT INFO
==============================

Created: 2025-01-15

GitHub:
- Username: your-github-username
- Email: your-email@example.com
- Profile: https://github.com/your-username

Docker Hub:
- Docker ID: your-docker-id  
- Email: your-email@example.com
- Profile: https://hub.docker.com/u/your-docker-id

2FA:
- GitHub: YES/NO
- Docker Hub: YES/NO

Notes:
- Passwords in password manager (LastPass/1Password)
- Never share passwords!
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

---

## ✅ Lab F: Verification (ALL OS)

### Lab F1: Run Verification Script

**Time:** 2 minutes

```bash
# Navigate to scripts folder
# Windows (WSL):
cd /mnt/c/DevOps/DevOpsTraining/FOUNDATION/00_SETUP/scripts

# macOS/Linux:
cd ~/DevOps/DevOpsTraining/FOUNDATION/00_SETUP/scripts

# List files
ls
# Should see: verify-linux.sh, verify-mac.sh, verify-windows.ps1

# Make executable (if needed)
chmod +x verify-*.sh

# Run appropriate script:
# Linux/WSL:
bash verify-linux.sh

# macOS:
bash verify-mac.sh
```

**Expected output:**

```
====================================
DevOps Training - Environment Check  
====================================

Checking operating system...
✅ OS: Ubuntu 22.04.3 LTS (WSL2)

Checking shell...
✅ Shell: bash 5.1.16

Checking VS Code...
✅ VS Code: version 1.85.0

Checking internet...
✅ Internet: Connected (ping google.com OK)

Checking disk space...
✅ Disk: 42.3 GB free

Checking course materials...
✅ Materials: Found at /mnt/c/DevOps/DevOpsTraining

====================================
ENVIRONMENT STATUS: ✅ READY
====================================

🎉 Congratulations! You're ready for Module 01!

Next steps:
1. Read Module 01 README
2. Complete Module 01 labs
3. Join Discord: https://discord.gg/devops-training

Happy learning! 🚀
```

---

### Lab F2: Manual Verification Checklist

If script fails or you want to check manually:

```bash
# 1. Check OS
uname -a
# Should show Linux/Darwin info

# 2. Check shell
echo $SHELL
# Should show: /bin/bash or /bin/zsh

# 3. Check VS Code
code --version
# Should show version number

# 4. Check internet
ping -c 3 google.com
# Should see replies

# 5. Check disk space
df -h ~
# Should see available space

# 6. Check course folder
ls ~/DevOps/DevOpsTraining/FOUNDATION
# Should see: 00_SETUP, 01_LINUX_BASICS, ...

# 7. Check accounts
echo "GitHub: https://github.com/YOUR-USERNAME"
echo "Docker Hub: https://hub.docker.com/u/YOUR-DOCKER-ID"
# Open these URLs and verify they load
```

---

## 📊 Lab Summary

| Lab | Task | Time | Status |
|-----|------|------|--------|
| A1/B1/C1 | OS Setup | 15-20m | [ ] |
| A2/- | Windows Terminal | 5m | [ ] |
| A3/B3/C2 | VS Code | 10m | [ ] |
| D1 | Download Materials | 5m | [ ] |
| E1 | GitHub Account | 10m | [ ] |
| E2 | Docker Hub Account | 5m | [ ] |
| E3 | Save Info | 3m | [ ] |
| F1 | Verification | 2m | [ ] |
| **TOTAL** | | **~60m** | [ ] |

---

## 🆘 Common Issues

### Issue 1: `wsl --install` fails (Windows)

**Error:** "The WSL optional component is not enabled"

**Fix:**

```powershell
# PowerShell as Admin:
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Restart computer
# Try again
```

---

### Issue 2: `brew` command not found (macOS)

**After installing Homebrew, terminal doesn't recognize `brew`**

**Fix:**

```bash
# Add brew to PATH:
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
source ~/.zprofile

# Try again:
brew --version
```

---

### Issue 3: `code` command not found

**macOS:**

```
1. Open VS Code
2. Cmd+Shift+P
3. "Shell Command: Install 'code' command in PATH"
```

**Linux:**

```bash
# Find where code is:
which code

# If not found, add to PATH:
export PATH="$PATH:/usr/share/code/bin"
echo 'export PATH="$PATH:/usr/share/code/bin"' >> ~/.bashrc
```

---

### Issue 4: Cannot download ZIP

**If download blocked by firewall/antivirus:**

1. Temporarily disable antivirus
2. Download ZIP
3. Re-enable antivirus
4. Right-click file → Properties → Unblock → OK

---

## 📝 Submission (Optional - For Instructor-Led Courses)

If you're taking this with an instructor:

**Take screenshots of:**

1. Verification script output
2. GitHub profile page
3. Docker Hub profile page
4. VS Code with course folder open

**Upload to:** [Submission link]

---

## ⏭️ Next Steps

✅ All labs complete?

👉 **[Read Module 01 README →](../01_LINUX_BASICS/README.md)**

Or check:

- [FAQ](FAQ.md) - Common questions
- [Troubleshooting](README.md#10-troubleshooting) - Detailed fixes

---

<div align="center">

**Lab 00 Complete! 🎉**

*Setup done right = smooth sailing ahead*

</div>
