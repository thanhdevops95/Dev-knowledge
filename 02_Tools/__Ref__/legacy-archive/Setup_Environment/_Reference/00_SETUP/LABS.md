# LABS - Module 00: SETUP

> **Mục tiêu:** Hoàn thành setup môi trường DevOps hoàn chỉnh
>
> **Thời gian:** 2-4 giờ (tùy OS và tốc độ internet)
>
> **Prerequisites:** Máy tính với admin rights

---

## 📋 Danh sách Labs

| Lab | Tên | Thời gian | Độ khó |
|-----|-----|-----------|--------|
| Lab 1 | Check System Requirements | 10 phút | ⭐☆☆☆☆ |
| Lab 2 | Install Windows Terminal | 15 phút | ⭐☆☆☆☆ |
| Lab 3 | Install & Configure WSL2 | 30 phút | ⭐⭐☆☆☆ |
| Lab 4 | Install VS Code & Extensions | 20 phút | ⭐☆☆☆☆ |
| Lab 5 | Setup Oh My Zsh | 15 phút | ⭐⭐☆☆☆ |
| Lab 6 | Generate SSH Keys | 15 phút | ⭐⭐☆☆☆ |
| Lab 7 | Create GitHub Account | 10 phút | ⭐☆☆☆☆ |
| Lab 8 | Create Docker Hub Account | 10 phút | ⭐☆☆☆☆ |
| Lab 9 | Run Environment Verification | 15 phút | ⭐⭐☆☆☆ |

**Tổng thời gian:** ~2.5 giờ

---

## Lab 1: Check System Requirements

### Objectives

- Verify máy tính đáp ứng minimum requirements
- Check Windows version (nếu dùng Windows)
- Confirm virtualization enabled

### Instructions

#### Step 1.1: Check Windows Version (Windows users)

**Action:**

```
1. Nhấn Win + R
2. Gõ: winver
3. Enter
```

**Expected Output:**

```
Windows Specifications
─────────────────────
Version 21H2 (OS Build 19044.xxxx)
hoặc
Windows 11 Version 22H2
```

**Verification:**

- ✅ Windows 10 version ≥ 1903 (Build ≥ 18362)
- ✅ Windows 11 bất kỳ version nào

**If version cũ hơn:**

```
Settings → Update & Security → Windows Update → Check for updates
```

⏱️ **Update có thể mất 1-2 giờ. Làm trong lúc học modules khác.**

#### Step 1.2: Check RAM

**Action:**

```
1. Ctrl + Shift + Esc (mở Task Manager)
2. Performance tab
3. Click "Memory"
```

**Expected Output:**

```
Total RAM: 8.0 GB hoặc nhiều hơn
```

**Verification:**

- ✅ Minimum: 8 GB
- ✅ Recommended: 16 GB

**If < 8 GB:**

- ⚠️ Có thể chạy nhưng sẽ chậm
- Đóng các apps không cần thiết khi coding
- Consider upgrade RAM nếu có thể

#### Step 1.3: Check Disk Space

**Action:**

```
1. Mở File Explorer (Win + E)
2. Click "This PC"
3. Xem Free space của C: drive
```

**Expected Output:**

```
Local Disk (C:)
Free space: 100 GB of 500 GB (hoặc hơn)
```

**Verification:**

- ✅ Minimum: 50 GB free
- ✅ Recommended: 100 GB free

**If < 50 GB:**

```
1. Settings → System → Storage
2. Click "Temporary files"
3. Check all, click "Remove files"
4. Uninstall unused apps
```

#### Step 1.4: Check Virtualization (Critical for WSL2)

**Action:**

```
1. Ctrl + Shift + Esc (Task Manager)
2. Performance tab
3. Click "CPU"
4. Tìm dòng "Virtualization"
```

**Expected Output:**

```
Virtualization: Enabled ✅
```

**If "Disabled":**

1. Restart máy tính
2. Nhấn phím vào BIOS (thường là F2, F10, F12, hoặc Delete)
   - Phím khác nhau tùy laptop/motherboard
   - Thường hiển thị khi boot: "Press F2 for Setup"
3. Tìm setting:
   - **Intel:** "Intel VT-x" hoặc "Virtualization Technology"
   - **AMD:** "AMD-V" hoặc "SVM Mode"
4. Set thành **Enabled**
5. Save & Exit (thường F10)

**Troubleshooting:**

```
Problem: Không tìm thấy Virtualization setting trong BIOS

Solution:
1. Google: "enable virtualization [tên laptop/motherboard]"
   Example: "enable virtualization Dell XPS 13"
2. Xem user manual
3. Một số laptop cũ không support → Consider dual boot Linux
```

#### Step 1.5: Summary Checklist

Sau khi hoàn thành Lab 1, check:

- [ ] Windows 10 (≥1903) hoặc Windows 11
- [ ] RAM ≥ 8 GB
- [ ] Disk free space ≥ 50 GB
- [ ] Virtualization enabled trong BIOS

✅ **Nếu tất cả OK, tiếp tục Lab 2!**

---

## Lab 2: Install Windows Terminal

### Objectives

- Install Windows Terminal
- Configure basic settings
- Set default profile

### Instructions

#### Step 2.1: Install từ Microsoft Store

**Action:**

```
1. Nhấn Win
2. Gõ "Microsoft Store"
3. Enter
4. Search: "Windows Terminal"
5. Click "Get" hoặc "Install"
6. Đợi download (1-2 phút)
```

**Alternative - PowerShell:**

```powershell
# Mở PowerShell as Admin
winget install Microsoft.WindowsTerminal
```

**Verification:**

```
1. Nhấn Win
2. Gõ "Terminal"
3. Should see "Windows Terminal" app
4. Click to open
```

**Expected Output:**

```
Windows PowerShell
PS C:\Users\YourName>
```

#### Step 2.2: Pin to Taskbar

**Action:**

```
1. Right-click Windows Terminal icon trên taskbar
2. Click "Pin to taskbar"
```

**Benefit:** Quick access (Win + [số thứ tự trên taskbar])

#### Step 2.3: Configure Settings

**Action:**

```
1. Mở Windows Terminal
2. Ctrl + , (mở Settings)
3. Hoặc click ▼ dropdown → Settings
```

**Recommended Settings:**

**Startup:**

```
Default profile: (sẽ set thành Ubuntu sau khi cài WSL2)
Launch size: Columns: 120, Rows: 30
```

**Appearance:**

```
Theme: Dark (hoặc Light nếu prefer)
Use acrylic: On (transparency effect)
Acrylic opacity: 80%
```

**Save:** Ctrl + S hoặc click "Save" button

#### Step 2.4: Keyboard Shortcuts

**Learn these shortcuts:**

```
Ctrl + Shift + T    : New tab
Ctrl + Shift + W    : Close tab
Ctrl + Shift + P    : Command palette
Alt + Shift + D     : Split pane (duplicate)
Alt + Shift + -     : Split pane horizontal
Alt + Shift + Plus  : Split pane vertical
Ctrl + Shift + F    : Search
Ctrl + C            : Copy (when text selected)
Ctrl + V            : Paste
```

**Practice:**

```
1. Mở Windows Terminal
2. Ctrl + Shift + T → Tạo tab mới
3. Alt + Shift + D → Split pane
4. Ctrl + Shift + W → Đóng pane/tab
```

#### Step 2.5: Verification

```powershell
# Check version
wt --version

# Expected output:
# Windows Terminal v1.18.xxxx
```

✅ **Windows Terminal ready! Tiếp tục Lab 3.**

---

## Lab 3: Install & Configure WSL2

### Objectives

- Install WSL2
- Install Ubuntu 22.04
- Create user account
- Update system packages

### Instructions

#### Step 3.1: Enable WSL Feature

**Action:**

```
Mở PowerShell as Administrator:
1. Win
2. Gõ "PowerShell"
3. Right-click "Windows PowerShell"
4. Click "Run as administrator"
```

**Run command:**

```powershell
wsl --install
```

**Expected Output:**

```
Installing: Virtual Machine Platform
Installing: Windows Subsystem for Linux
Downloading: Ubuntu
Installation complete!
Please restart your computer.
```

**Alternative (manual):**

Nếu `wsl --install` fails:

```powershell
# Enable WSL
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine Platform
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

**Restart required:**

```
Restart now! (Important)
```

⏱️ **Restart mất 2-5 phút**

#### Step 3.2: Set WSL 2 as Default

**After restart, mở PowerShell as Admin lại:**

```powershell
# Set WSL 2 as default version
wsl --set-default-version 2
```

**Expected Output:**

```
For information on key differences with WSL 2 please visit https://aka.ms/wsl2
The operation completed successfully.
```

#### Step 3.3: Install Ubuntu 22.04

**Method 1: Microsoft Store (Recommended)**

```
1. Mở Microsoft Store
2. Search "Ubuntu 22.04"
3. Click "Get" / "Install"
4. Đợi download (~500 MB, 2-10 phút tùy internet)
5. Click "Open" hoặc
   Win → gõ "Ubuntu 22.04" → Enter
```

**Method 2: Command line**

```powershell
# List available distros
wsl --list --online

# Install Ubuntu 22.04
wsl --install -d Ubuntu-22.04
```

#### Step 3.4: First Launch & User Creation

**Ubuntu sẽ launch lần đầu:**

```
Installing, this may take a few minutes...
Please create a default UNIX user account. The username does not need to match your Windows username.
For more information visit: https://aka.ms/wslusers

Enter new UNIX username:
```

**Action:**

```
1. Gõ username (lowercase, no spaces)
   Example: john

2. Enter

3. New password:
   (Gõ password, KHÔNG HIỂN THỊ GÌ - normal)
   
4. Retype password:
   (Gõ lại chính xác password)
```

**Tips:**

- Username: lowercase, ngắn, dễ nhớ
- Password: Cho local dev thì "1234" OK (KHÔNG dùng cho production!)
- Production: strong password bắt buộc

**Expected Output:**

```
Installation successful!
To run a command as administrator (user "root"), use "sudo <command>".
See "man sudo_root" for details.

username@DESKTOP-XXX:~$
```

✅ **Bạn đã vào Linux terminal!**

#### Step 3.5: Update System

**Run first commands:**

```bash
# Update package lists
sudo apt update
```

**Prompt for password:**

```
[sudo] password for username:
```

**→ Gõ password vừa tạo (không hiển thị), Enter**

**Expected Output:**

```
Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease
Get:2 http://archive.ubuntu.com/ubuntu jammy-updates InRelease [119 kB]
...
Fetched 25.3 MB in 8s (3,165 kB/s)
Reading package lists... Done
Building dependency tree... Done
All packages are up to date.
```

**Upgrade packages:**

```bash
sudo apt upgrade -y
```

**Expected:**

```
Reading package lists... Done
...
0 upgraded, 0 newly installed, 0 to remove and 0 not upgraded.
```

⏱️ **Upgrade có thể mất 5-15 phút lần đầu**

#### Step 3.6: Verify Installation

```bash
# Check WSL version
wsl --list --verbose
```

**Expected (trong PowerShell hoặc CMD):**

```
  NAME            STATE           VERSION
* Ubuntu-22.04    Running         2
```

**Check inside Ubuntu:**

```bash
# OS version
cat /etc/os-release
```

**Expected Output:**

```
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
ID=ubuntu
...
```

```bash
# Check kernel
uname -r
```

**Expected:**

```
5.15.90.1-microsoft-standard-WSL2
```

#### Step 3.7: Test Basic Commands

```bash
# Where am I?
pwd
# Output: /home/username

# List files
ls -la

# Output:
# drwxr-xr-x 2 username username 4096 Dec 25 10:00 .
# drwxr-xr-x 3 root     root     4096 Dec 25 09:55 ..
# -rw-r--r-- 1 username username  220 Dec 25 09:55 .bash_logout
# ...

# Create test file
echo "Hello WSL2!" > test.txt

# View file
cat test.txt
# Output: Hello WSL2!

# Remove test file
rm test.txt
```

✅ **All commands work? WSL2 setup complete!**

#### Troubleshooting

**Problem: "WslRegisterDistribution failed with error: 0x80370102"**

**Solution:**

```
Virtualization chưa enable trong BIOS
→ Quay lại Lab 1, Step 1.4
```

**Problem: "Windows Subsystem for Linux has no installed distributions"**

**Solution:**

```powershell
# Install Ubuntu lại
wsl --install -d Ubuntu-22.04
```

**Problem: Ubuntu crashes khi start**

**Solution:**

```powershell
# Terminate WSL
wsl --shutdown

# Restart
wsl
```

---

## Lab 4: Install VS Code & Extensions

### Objectives

- Install Visual Studio Code
- Install essential extensions
- Configure for WSL development
- Test connection to WSL

### Instructions

#### Step 4.1: Download VS Code

**Action:**

```
1. Visit: https://code.visualstudio.com/
2. Click "Download for Windows"
3. Run installer (VSCodeUserSetup-x64-x.xx.x.exe)
```

**Installer options:**

```
☑ Add "Open with Code" action to Windows Explorer file context menu
☑ Add "Open with Code" action to Windows Explorer directory context menu  
☑ Register Code as an editor for supported file types
☑ Add to PATH
```

**→ Click "Install"**

⏱️ **Installation: 2-3 phút**

#### Step 4.2: Launch VS Code

**Action:**

```
1. Desktop shortcut → Double-click "Visual Studio Code"
   OR
2. Win → gõ "VS Code" → Enter
```

**First launch:**

```
VS Code mở → Welcome screen
```

#### Step 4.3: Install Extensions

**Method 1: GUI**

```
1. Click Extensions icon (sidebar trái) hoặc Ctrl + Shift + X
2. Search extension name
3. Click "Install"
```

**Method 2: Command Palette**

```
1. Ctrl + Shift + P
2. Gõ "Extensions: Install Extensions"
3. Enter
4. Search & install
```

**Essential Extensions:**

**1. Remote - WSL** (MUST HAVE)

```
Search: "Remote - WSL"
Publisher: Microsoft
Click "Install"
```

**2. GitLens**

```
Search: "GitLens"
Publisher: GitKraken
Install
```

**3. Docker**

```
Search: "Docker"
Publisher: Microsoft
Install
```

**4. YAML**

```
Search: "YAML"
Publisher: Red Hat
Install
```

**5. Markdown All in One**

```
Search: "Markdown All in One"
Publisher: Yu Zhang
Install
```

**6. Live Share** (optional, for pair programming)

```
Search: "Live Share"
Publisher: Microsoft
Install
```

**Verification:**

```
Extensions sidebar → Installed tab
Should see all 6 extensions listed
```

#### Step 4.4: Configure Settings

**Action:**

```
1. Ctrl + , (Settings)
   OR
   File → Preferences → Settings
```

**Recommended settings:**

**Search "Font Size"**

```
Editor: Font Size = 14
```

**Search "Auto Save"**

```
Files: Auto Save = onFocusChange
```

**Search "Format On Save"**

```
Editor: Format On Save = ☑ (checked)
```

**Search "Tab Size"**

```
Editor: Tab Size = 2
```

**Search "Minimap"**

```
Editor: Minimap Enabled = ☐ (unchecked, optional - tiết kiệm space)
```

#### Step 4.5: Connect to WSL

**Action:**

```
1. Nhấn F1 (hoặc Ctrl + Shift + P)
2. Gõ: "WSL: Connect to WSL"
3. Enter
```

**Expected:**

```
New VS Code window opens
Bottom-left corner: WSL: Ubuntu-22.04 (chữ xanh lá)
```

**Verify connection:**

```
1. Terminal → New Terminal (Ctrl + `)
2. Should see Ubuntu bash prompt:
   username@HOSTNAME:~$
```

**Test:**

```bash
# In VS Code terminal (WSL):
pwd
# Output: /home/username

whoami
# Output: username
```

#### Step 4.6: Create Test Workspace

**In VS Code (connected to WSL):**

```bash
# Create project folder
mkdir -p ~/projects/test
cd ~/projects/test

# Open in VS Code
code .
```

**Expected:**

```
VS Code refreshes
Sidebar shows "TEST" folder
Still connected to WSL (check bottom-left)
```

**Create test file:**

```
1. Right-click in Explorer → New File
2. Name: hello.txt
3. Type: "Hello from VS Code in WSL!"
4. Ctrl + S (save)
```

**Verify file on disk:**

```bash
# In terminal
cat hello.txt
# Output: Hello from VS Code in WSL!
```

✅ **VS Code working với WSL!**

#### Troubleshooting

**Problem: Can't connect to WSL**

**Solution:**

```
1. Check WSL running:
   wsl --list --verbose
   (State should be "Running")

2. Restart WSL:
   wsl --shutdown
   wsl

3. Restart VS Code

4. Try connect again
```

**Problem: Extensions not working in WSL**

**Solution:**

```
Extensions installed in Windows, not WSL!

Fix:
1. Click Extensions (Ctrl + Shift + X)
2. Find extension
3. Click "Install in WSL: Ubuntu-22.04"
```

---

## Lab 5: Setup Oh My Zsh

### Objectives

- Install Zsh shell
- Install Oh My Zsh framework
- Install Powerlevel10k theme
- Configure plugins

### Instructions

#### Step 5.1: Install Zsh

**In WSL Ubuntu terminal:**

```bash
# Install Zsh
sudo apt install zsh -y
```

**Expected Output:**

```
Reading package lists... Done
...
Setting up zsh (5.8.1-1) ...
```

**Verify:**

```bash
zsh --version
# Output: zsh 5.8.1 (x86_64-ubuntu-linux-gnu)
```

#### Step 5.2: Install Oh My Zsh

**Run install script:**

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

**Expected Output:**

```
Cloning Oh My Zsh...
...
         __                                     __
  ____  / /_     ____ ___  __  __   ____  _____/ /_
 / __ \/ __ \   / __ `__ \/ / / /  /_  / / ___/ __ \
/ /_/ / / / /  / / / / / / /_/ /    / /_(__  ) / / /
\____/_/ /_/  /_/ /_/ /_/\__, /    /___/____/_/ /_/
                        /____/                       ....is now installed!
```

**Prompt:**

```
Time to change your default shell to zsh?
Do you want to change your default shell to zsh? (Y/n)
```

**→ Type: Y**

**Expected:**

```
Shell successfully changed to '/usr/bin/zsh'.
```

**Start new shell:**

```bash
# Exit current shell
exit

# Start fresh WSL
wsl
```

**Should see Zsh prompt:**

```
➜  ~
```

#### Step 5.3: Install Powerlevel10k Theme

```bash
# Clone theme
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

**Edit ~/.zshrc:**

```bash
nano ~/.zshrc
```

**Find line:**

```bash
ZSH_THEME="robbyrussell"
```

**Replace with:**

```bash
ZSH_THEME="powerlevel10k/powerlevel10k"
```

**Save:** Ctrl + O, Enter, Ctrl + X

**Apply:**

```bash
source ~/.zshrc
```

**Powerlevel10k configuration wizard starts:**

```
This is Powerlevel10k configuration wizard...

Does this look like a diamond (rotated square)?
  reference: https://...

(y)  Yes.
(n)  No.
(q)  Quit and do nothing.

Choice [ynq]:
```

**Follow prompts (recommended answers):**

```
Diamond? y
Lock? y
Debian logo? y
Prompt style? 3 (Rainbow)
Character set? 1 (Unicode)
Show current time? 2 (24-hour format)
Prompt separators? 1 (Angled)
Prompt heads? 1 (Sharp)
Prompt tails? 1 (Flat)
Prompt height? 1 (One line)
Prompt spacing? 2 (Sparse)
Icons? 2 (Many icons)
Prompt flow? 1 (Concise)
Transient prompt? n
Instant prompt mode? 1 (Verbose)
```

**Result:**

```
Beautiful colorful prompt với Git status, folder icons, etc.
```

#### Step 5.4: Install Useful Plugins

**Edit ~/.zshrc:**

```bash
nano ~/.zshrc
```

**Find:**

```bash
plugins=(git)
```

**Replace with:**

```bash
plugins=(
  git
  docker
  docker-compose
  kubectl
  sudo
  z
  colored-man-pages
)
```

**Save & apply:**

```bash
source ~/.zshrc
```

**Test plugins:**

```bash
# 'z' plugin - jump to directories
mkdir -p ~/projects/test1
cd ~/projects/test1
cd ~

# Later, just:
z test1
pwd
# Should be in ~/projects/test1

# 'sudo' plugin - press Esc twice to add sudo
echo "test"
# (Đang gõ) ls /root
# Press Esc Esc
# Becomes: sudo ls /root
```

#### Step 5.5: Install Syntax Highlighting (Optional)

```bash
# Install
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# Add to plugins
nano ~/.zshrc
```

**Update plugins:**

```bash
plugins=(
  git
  docker
  zsh-syntax-highlighting  # Add this
)
```

**Apply:**

```bash
source ~/.zshrc
```

**Test:**

```
Type: ls
Should be green (valid command)

Type: lsss
Should be red (invalid command)
```

✅ **Oh My Zsh configured!**

---

## Lab 6: Generate SSH Keys

### Objectives

- Generate SSH key pair
- Add key to SSH agent
- View public key
- Prepare for GitHub/server access

### Instructions

#### Step 6.1: Check Existing Keys

```bash
ls -la ~/.ssh/
```

**If no .ssh folder:**

```
ls: cannot access '/home/username/.ssh/': No such file or directory
```

**→ Good, proceed to generate**

**If .ssh exists với keys:**

```
-rw------- 1 username username  464 Dec 25 10:00 id_ed25519
-rw-r--r-- 1 username username  103 Dec 25 10:00 id_ed25519.pub
```

**→ Keys already exist. Can reuse or generate new.**

#### Step 6.2: Generate New SSH Key

```bash
ssh-keygen -t ed25519 -C "your.email@example.com"
```

**Replace:** `your.email@example.com` với email thật

**Prompts:**

```
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/username/.ssh/id_ed25519):
```

**→ Just press Enter (accept default)**

```
Enter passphrase (empty for no passphrase):
```

**→ Press Enter (no passphrase cho local dev)**
**Note:** Production servers NÊN có passphrase!

```
Enter same passphrase again:
```

**→ Press Enter again**

**Expected Output:**

```
Your identification has been saved in /home/username/.ssh/id_ed25519
Your public key has been saved in /home/username/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:abcd1234... your.email@example.com
The key's randomart image is:
+--[ED25519 256]--+
|      .o+        |
|     . o +       |
...
```

#### Step 6.3: Start SSH Agent

```bash
# Start agent
eval "$(ssh-agent -s)"
```

**Expected Output:**

```
Agent pid 1234
```

**Add key to agent:**

```bash
ssh-add ~/.ssh/id_ed25519
```

**Expected Output:**

```
Identity added: /home/username/.ssh/id_ed25519 (your.email@example.com)
```

#### Step 6.4: View Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

**Expected Output:**

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIAbCdEfGhIjKlMnOpQrStUvWxYz01234567890abcdef your.email@example.com
```

**Copy this entire line!** (sẽ dùng để add vào GitHub)

**Tips:**

```bash
# Copy to clipboard (nếu có xclip)
cat ~/.ssh/id_ed25519.pub | clip.exe

# Hoặc trong Windows Terminal: Select text → Right-click (auto copy)
```

#### Step 6.5: Set Correct Permissions

```bash
# Ensure proper permissions (security)
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

**Verify:**

```bash
ls -la ~/.ssh/
```

**Expected:**

```
drwx------ 2 username username  (700) .
-rw------- 1 username username  (600) id_ed25519
-rw-r--r-- 1 username username  (644) id_ed25519.pub
```

✅ **SSH keys generated & secured!**

---

## Lab 7: Create GitHub Account

### Objectives

- Create GitHub account
- Configure profile
- Add SSH key
- Test SSH connection

### Instructions

#### Step 7.1: Sign Up for GitHub

**Action:**

```
1. Visit: https://github.com/signup
2. Enter email
3. Create password (strong!)
4. Choose username (carefully - hard to change later)
5. Verify you're human (puzzle/captcha)
6. Check email for verification code
7. Enter code
```

**Username tips:**

- Professional (có thể dùng cho resume)
- Lowercase, no spaces
- Short, memorable
- Available (github.com/username)

#### Step 7.2: Complete Profile

**Action:**

```
1. Click profile icon (top-right) → Settings
2. Public profile:
   - Name: Your real name
   - Bio: (optional) "DevOps learner"
   - Location: (optional)
   - Website: (optional)
3. Upload profile picture (optional but recommended)
4. Save
```

#### Step 7.3: Enable 2FA (Two-Factor Authentication)

**Highly recommended for security!**

**Action:**

```
1. Settings → Password and authentication
2. Click "Enable two-factor authentication"
3. Choose method:
   - Authenticator app (recommended): Google Authenticator, Authy
   - SMS (less secure)
4. Scan QR code với app
5. Enter 6-digit code
6. Save recovery codes (IMPORTANT!)
```

⚠️ **Store recovery codes an toàn! Mất code = mất account!**

#### Step 7.4: Add SSH Key to GitHub

**Action:**

```
1. Settings → SSH and GPG keys
2. Click "New SSH key"
3. Title: "WSL Ubuntu 22.04"
4. Key: Paste public key từ Lab 6
   (ssh-ed25519 AAA...)
5. Click "Add SSH key"
6. Confirm với password hoặc 2FA
```

**Result:**

```
SSH key added successfully
Key fingerprint: SHA256:abc123...
```

#### Step 7.5: Test SSH Connection

**In WSL terminal:**

```bash
ssh -T git@github.com
```

**First time prompt:**

```
The authenticity of host 'github.com (140.82.121.4)' can't be established.
ED25519 key fingerprint is SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU.
This key's fingerprint is published at https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

**→ Type: yes**

**Expected Output:**

```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

✅ **GitHub account ready & SSH working!**

#### Troubleshooting

**Problem: "Permission denied (publickey)"**

**Solutions:**

```bash
# 1. Check SSH key added to GitHub (refresh browser)

# 2. Check SSH agent running
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 3. Test again
ssh -T git@github.com
```

**Problem: "Connection timed out"**

**Solutions:**

```bash
# Try HTTPS instead of SSH (firewall issue)
# OR configure SSH to use port 443:

nano ~/.ssh/config

# Add:
Host github.com
  Hostname ssh.github.com
  Port 443
  User git

# Save, test
ssh -T git@github.com
```

---

## Lab 8: Create Docker Hub Account

### Objectives

- Create Docker Hub account
- Generate access token
- Test docker login

### Instructions

#### Step 8.1: Sign Up

**Action:**

```
1. Visit: https://hub.docker.com/signup
2. Docker ID: Choose username (lowercase, no spaces)
3. Email: Your email
4. Password: Strong password
5. Check email for verification
6. Click verification link
```

**Docker ID tips:**

- Same as GitHub username (for consistency)
- Will be in image names: dockerhub-username/image-name

#### Step 8.2: Explore Docker Hub

**Action:**

```
1. Search "nginx" → See official images
2. Search "ubuntu" → Official Ubuntu images
3. Browse Featured Repos
```

**Understanding:**

```
Image naming:
- nginx             (official image)
- username/nginx    (user image)
- nginx:latest      (tag: latest version)
- nginx:1.25-alpine (tag: specific version + variant)
```

#### Step 8.3: Create Access Token

**Why:** Password deprecated, use tokens

**Action:**

```
1. Profile → Account Settings
2. Security → Access Tokens
3. New Access Token
4. Description: "WSL Ubuntu Development"
5. Access permissions: Read, Write, Delete
6. Generate
```

**IMPORTANT:**

```
Copy token NOW! (shows only once)
Example: dckr_pat_abc123...

Store securely:
- Password manager
- .env file (NEVER commit to Git!)
```

#### Step 8.4: Test Login

**In WSL terminal:**

```bash
# Login (use token as password, NOT account password)
docker login -u your-docker-id

# Prompt:
Password:
```

**→ Paste access token, Enter**

**Expected Output:**

```
WARNING! Your password will be stored unencrypted in /home/username/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```

⚠️ **Warning is OK for local dev. Production: use credential helpers**

#### Step 8.5: Verify Login

```bash
# Check config
cat ~/.docker/config.json
```

**Should see:**

```json
{
  "auths": {
    "https://index.docker.io/v1/": {
      "auth": "base64encodedtoken..."
    }
  }
}
```

✅ **Docker Hub ready!**

---

## Lab 9: Run Environment Verification

### Objectives

- Download verification script
- Run comprehensive environment check
- Interpret results
- Fix any issues

### Instructions

#### Step 9.1: Create Verification Script

**Create script file:**

```bash
cd ~
nano verify-setup.sh
```

**Paste this script:**

```bash
#!/bin/bash

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================"
echo "  DevOps Training - Setup Verification"
echo "======================================"
echo""

# OS Check
echo -n "Checking OS... "
if [[ -f /etc/os-release ]]; then
    OS_NAME=$(grep "^NAME=" /etc/os-release | cut -d'"' -f2)
    OS_VERSION=$(grep "^VERSION=" /etc/os-release | cut -d'"' -f2)
    echo -e "${GREEN}✓${NC} $OS_NAME $OS_VERSION"
else
    echo -e "${RED}✗${NC} Cannot detect OS"
fi

# WSL Version Check
echo -n "Checking WSL version... "
if grep -qi microsoft /proc/version; then
    WSL_VERSION=$(grep -oP 'WSL\K[0-9]' /proc/version || echo "1")
    if [[ "$WSL_VERSION" == "2" ]]; then
        echo -e "${GREEN}✓${NC} WSL2"
    else
        echo -e "${YELLOW}!${NC} WSL1 (upgrade to WSL2 recommended)"
    fi
else
    echo -e "${YELLOW}!${NC} Not running in WSL"
fi

# Git Check
echo -n "Checking Git... "
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo -e "${GREEN}✓${NC} version $GIT_VERSION"
else
    echo -e "${RED}✗${NC} Git not found - Install: sudo apt install git"
fi

# SSH Keys Check
echo -n "Checking SSH keys... "
if [[ -f ~/.ssh/id_ed25519 ]] || [[ -f ~/.ssh/id_rsa ]]; then
    echo -e "${GREEN}✓${NC} Found"
else
    echo -e "${RED}✗${NC} No SSH keys - Run: ssh-keygen -t ed25519"
fi

# Zsh Check
echo -n "Checking Zsh... "
if command -v zsh &> /dev/null; then
    echo -e "${GREEN}✓${NC} $(zsh --version | awk '{print $2}')"
else
    echo -e "${YELLOW}!${NC} Not installed (optional)"
fi

# Oh My Zsh Check
echo -n "Checking Oh My Zsh... "
if [[ -d ~/.oh-my-zsh ]]; then
    echo -e "${GREEN}✓${NC} Installed"
else
    echo -e "${YELLOW}!${NC} Not installed (optional)"
fi

# Docker Check (will install in Module 05)
echo -n "Checking Docker... "
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | awk '{print $3}' | tr -d ',')
    echo -e "${GREEN}✓${NC} version $DOCKER_VERSION"
else
    echo -e "${YELLOW}!${NC} Not installed yet (Module 05)"
fi

# curl Check
echo -n "Checking curl... "
if command -v curl &> /dev/null; then
    echo -e "${GREEN}✓${NC} Installed"
else
    echo -e "${RED}✗${NC} Install: sudo apt install curl"
fi

# wget Check
echo -n "Checking wget... "
if command -v wget &> /dev/null; then
    echo -e "${GREEN}✓${NC} Installed"
else
    echo -e "${YELLOW}!${NC} Install: sudo apt install wget"
fi

# Summary
echo ""
echo "======================================"
echo "  Summary"
echo "======================================"
echo -e "${GREEN}✓${NC} = Ready"
echo -e "${YELLOW}!${NC} = Optional/Will install later"
echo -e "${RED}✗${NC} = Action needed"
echo ""
echo "If all critical checks pass, you're ready for Module 01!"
```

**Save:** Ctrl + O, Enter, Ctrl + X

#### Step 9.2: Make Script Executable

```bash
chmod +x verify-setup.sh
```

#### Step 9.3: Run Verification

```bash
./verify-setup.sh
```

**Example Expected Output:**

```
======================================
  DevOps Training - Setup Verification
======================================

Checking OS... ✓ Ubuntu 22.04.3 LTS
Checking WSL version... ✓ WSL2
Checking Git... ✓ version 2.34.1
Checking SSH keys... ✓ Found
Checking Zsh... ✓ 5.8.1
Checking Oh My Zsh... ✓ Installed
Checking Docker... ! Not installed yet (Module 05)
Checking curl... ✓ Installed
Checking wget... ✓ Installed

======================================
  Summary
======================================
✓ = Ready
! = Optional/Will install later
✗ = Action needed

If all critical checks pass, you're ready for Module 01!
```

#### Step 9.4: Fix Any Issues

**If see ✗ (red X):**

**Git not found:**

```bash
sudo apt install git -y
```

**SSH keys missing:**

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

**curl/wget missing:**

```bash
sudo apt install curl wget -y
```

**Re-run script after fixes:**

```bash
./verify-setup.sh
```

✅ **All green? You're ready for Module 01!**

---

## 🎉 Labs Complete

### Checklist Final

- [ ] ✅ System requirements met
- [ ] ✅ Windows Terminal installed & configured
- [ ] ✅ WSL2 with Ubuntu 22.04 running
- [ ] ✅ VS Code installed với Remote-WSL extension
- [ ] ✅ Oh My Zsh với Powerlevel10k
- [ ] ✅ SSH keys generated
- [ ] ✅ GitHub account created & SSH key added
- [ ] ✅ Docker Hub account created
- [ ] ✅ Verification script passed

### What's Next?

**You're now ready to start:**

- ✅ Module 01: Linux Basics
- ✅ Module 02: Git & GitHub
- ✅ Rest of Foundation Track!

### Tips for Success

**1. Keep Learning:**

- Do LABS trong mỗi module
- Practice daily (consistency > intensity)
- Don't skip exercises

**2. Customize Your Environment:**

- Add aliases: `alias ll='ls -lah'`
- Customize VS Code theme
- Explore Oh My Zsh plugins

**3. Backup Important Files:**

```bash
# GitHub profile README
# SSH configs
# Custom scripts
```

**4. Join Communities:**

- DevOps Discord servers
- Reddit: r/devops, r/linux, r/docker
- Stack Overflow

---

> **"The journey of a thousand miles begins with a single step. You've taken the first step!" 🚀**
>
> **Happy learning! See you in Module 01!** 💻
