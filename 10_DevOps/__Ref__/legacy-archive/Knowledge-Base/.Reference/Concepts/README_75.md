# Module 01: LINUX BASICS - Làm chủ Command Line

> **"Linux is not Windows with a different hat on"**  
> *-- Linus Torvalds*

---

## 📚 MỤC LỤC

1. [Giới thiệu](#1-giới-thiệu)
2. [Tại sao DevOps cần Linux?](#2-tại-sao-devops-cần-linux)
3. [Lịch sử Linux](#3-lịch-sử-linux)
4. [Linux File System](#4-linux-file-system)
5. [Navigation Commands](#5-navigation-commands)
6. [File Operations](#6-file-operations)
7. [Text Processing](#7-text-processing)
8. [Permissions & Ownership](#8-permissions--ownership)
9. [Processes & Services](#9-processes--services)
10. [Package Management](#10-package-management)
11. [Networking Basics](#11-networking-basics)
12. [Shell Scripting Introduction](#12-shell-scripting-introduction)
13. [Common Mistakes](#13-common-mistakes)
14. [Tổng kết](#14-tổng-kết)

---

## 1. Giới thiệu

### Câu chuyện mở đầu

> **Năm 2019**, tôi là DevOps engineer mới vào nghề. Một ngày, production server của công ty bị down lúc 2h sáng. Manager gọi điện: "Server không response! SSH vào check ngay!"
>
> Tôi SSH vào server, màn hình terminal đen thui hiện ra. Tôi gõ `dir` (Windows habit) → `command not found`. Hoảng hốt, tôi Google "how to check disk space Linux" → `df -h`. Thấy disk đầy 100%!
>
> Nhưng không biết xóa file gì, không biết tìm file lớn ở đâu. Mất 2 tiếng mò mẫm, cuối cùng phải gọi senior dậy giúp. Senior vào, 5 phút fix xong:
>
> ```bash
> du -sh /* | sort -h | tail -10  # Tìm folders lớn nhất
> rm -rf /var/log/old_logs/*      # Xóa old logs
> systemctl restart app           # Restart app
> ```
>
> Hôm đó tôi học được: **Linux command line không phải "nice to have", mà là MUST HAVE cho DevOps.**

### Linux là gì?

**Linux** là:

- **Operating System** (Hệ điều hành) - Như Windows, macOS
- **Open Source** - Code công khai, free, community-driven
- **Unix-like** - Dựa trên thiết kế Unix (ra đời 1969)
- **Kernel-based** - Linux chỉ là kernel, distribution là full OS

**Linux ≠ Ubuntu:**

```
Linux (Kernel)
    ├── Ubuntu (Distribution)
    ├── Fedora (Distribution)
    ├── CentOS (Distribution)
    ├── Debian (Distribution)
    └── Arch (Distribution)
```

**Ẩn dụ:**

```
Car = Operating System
Engine = Kernel (Linux)
Full Car with Seats/Wheels = Distribution (Ubuntu, Fedora, ...)

Linux là "engine", Ubuntu là "complete car"
```

### Module này học gì?

Sau khi hoàn thành module này, bạn sẽ:

✅ **Kỹ năng kỹ thuật:**

- Navigate Linux file system như một pro
- Thao tác files/folders (create, move, copy, delete)
- Hiểu và set permissions (rwx, chmod, chown)
- Quản lý processes (ps, kill, top, htop)
- Cài đặt software (apt, yum, dnf)
- Đọc và search logs
- Basic shell scripting

✅ **Mindset:**

- "Command line > GUI" - Tại sao CLI powerful hơn
- "Everything is a file" - Philosophy của Linux
- "RTFM" (Read The F* Manual) - man command

✅ **Real-world skills:**

- Troubleshoot production servers
- Automate tasks
- SSH vào servers và tự tin làm việc

---

## 2. Tại sao DevOps cần Linux?

### 2.1. Statistics về Production Servers

```
Production Servers OS Distribution (2024):
┌────────────────────────────────────┐
│  Linux:        96.3%  ████████████ │
│  Windows:       2.9%  ▌            │
│  BSD/Other:     0.8%  ▎            │
└────────────────────────────────────┘

Nguồn: W3Techs, Linux Foundation
```

**Nghĩa là:**

- 96.3% servers mà bạn sẽ làm việc chạy Linux
- Không biết Linux = Không làm được 96% công việc

### 2.2. Các công cụ DevOps chạy trên Linux

| Tool | Windows Native? | Linux Native? | Kết luận |
|------|----------------|---------------|----------|
| **Docker** | Thông qua WSL2 | ✅ Native | Linux tốt hơn |
| **Kubernetes** | kubectl only | ✅ Full support | Linux required |
| **Ansible** | ❌ KHÔNG | ✅ Native | PHẢI dùng Linux |
| **Terraform** | ✅ OK | ✅ OK | Cả hai OK |
| **Jenkins** | ✅ OK | ✅ Tốt hơn | Linux preferred |
| **Prometheus** | Limited | ✅ Full | Linux recommended |

→ **Kết luận:** Linux là ngôn ngữ chung của DevOps ecosystem

### 2.3. Tại sao Production chạy Linux?

**Lý do 1: Stability (Ổn định)**

```
Windows Server:
- Restart sau updates: Thường xuyên
- Uptime record: ~49 days trung bình

Linux Server:
- Restart sau updates: Kernel updates only
- Uptime record: 1000+ days không hiếm
```

**Lý do 2: Performance**

```
RAM usage (idle):
- Windows Server 2022: ~2-3GB
- Ubuntu Server: ~200-500MB

→ Tiết kiệm ~2.5GB RAM = Tiết kiệm chi phí cloud!
```

**Lý do 3: Cost (Chi phí)**

```
Windows Server License:
- Standard: $1,069 (one-time)
- Datacenter: $6,155 (one-time)

Ubuntu Server License:
- FREE (mãi mãi)

1000 servers:
- Windows: $1,069,000+
- Linux: $0
```

**Lý do 4: Automation-Friendly**

- CLI-first design → Dễ script
- SSH remote access → Standard
- Package managers → Consistent deployment

### 2.4. DevOps Workflow Example

**Tình huống:** Deploy app lên 100 servers

**Với Windows:**

```powershell
# RDP vào từng server (chậm, manual)
# Hoặc dùng WinRM (phức tạp setup)
# Tools: PowerShell Remoting
```

**Với Linux:**

```bash
# SSH với ansible (1 command → 100 servers)
ansible all -m copy -a "src=app.war dest=/opt/app/"
ansible all -m service -a "name=tomcat state=restarted"

# Done! 100 servers updated trong <1 phút
```

→ **Linux = Automation paradise**

---

## 3. Lịch sử Linux

### 3.1. Timeline

```
1969: UNIX ra đời (Bell Labs)
       ↓
1983: GNU Project (Richard Stallman)
      "Free Unix-like OS"
       ↓
1991: Linux Kernel (Linus Torvalds, 21 tuổi)
      ↓
1993: Debian Linux
      ↓
2004: Ubuntu Linux (dễ dùng nhất)
      ↓
2024: Linux everywhere (servers, Android, IoT, ...)
```

### 3.2. Câu chuyện Linus Torvalds

> **1991**, Linus Torvalds, sinh viên 21 tuổi ở Finland, không thích MINIX (Unix clone for education). Anh quyết định viết kernel riêng... for fun.
>
> Email của Linus đến newsgroup (1991):
>
> ```
> Hello everybody out there using minix -
>
> I'm doing a (free) operating system (just a hobby, 
> won't be big and professional like gnu) for 386(486) AT clones.
> ```
>
> **"just a hobby, won't be big"** - Famous last words! 😄
>
> 30+ năm sau: Linux chạy trên ~90% cloud servers, 100% top 500 supercomputers, billions of Android devices.

### 3.3. Open Source Philosophy

**Linux philosophy:**

1. **Free** (miễn phí) - No license fees
2. **Freedom** (tự do) - Xem và sửa source code
3. **Community-driven** - Hàng ngàn developers contribute
4. **Transparent** - Biết chính xác OS làm gì

**Ẩn dụ:**

```
Windows = Xe hơi branded (Toyota, Honda)
- Không được mở nắp máy
- Phải đi garage chính hãng
- Đắt tiền

Linux = Xe hơi open-source
- Mở nắp máy, xem engine
- Tự sửa chữa nếu biết
- Free blueprints
- Community sharing tips
```

---

## 4. Linux File System

### 4.1. "Everything is a File"

**Core philosophy của Linux:**

> Mọi thứ trong Linux đều được coi là file:
>
> - Regular files (documents, images, ...)
> - Directories (folders)
> - Devices (hard disk, USB, ...)
> - Network connections
> - Running processes

**Ẩn dụ:**

```
Linux xem hệ thống như một tủ hồ sơ khổng lồ:
- Files = Giấy tờ
- Directories = Ngăn kéo
- Devices = "Giấy tờ đặc biệt" (có thể ghi/đọc)
```

### 4.2. File System Hierarchy

```
/                           (Root - Gốc của mọi thứ)
├── bin/                    (Essential binaries)
├── boot/                   (Boot loader files)
├── dev/                    (Device files)
├── etc/                    (Configuration files)
├── home/                   (User home directories)
│   ├── john/
│   └── alice/
├── lib/                    (Shared libraries)
├── media/                  (Mount points for removable media)
├── mnt/                    (Temporary mount points)
├── opt/                    (Optional software)
├── proc/                   (Process information)
├── root/                   (Root user home)
├── run/                    (Runtime data)
├── sbin/                   (System binaries)
├── srv/                    (Service data)
├── sys/                    (System information)
├── tmp/                    (Temporary files)
├── usr/                    (User programs)
│   ├── bin/
│   ├── lib/
│   └── local/
└── var/                    (Variable data)
    ├── log/                (Log files)
    ├── mail/
    └── tmp/
```

### 4.3. Giải thích từng thư mục

#### `/` (Root)

**Là gì:** Gốc của toàn bộ file system.

**Ẩn dụ:**

```
Windows:
C:\, D:\, E:\ (nhiều roots)

Linux:
/ (chỉ một root, mọi thứ bắt đầu từ đây)
```

**Ví dụ:**

```bash
cd /              # Về root
ls                # List tất cả top-level directories
```

#### `/home/` - User Home Directories

**Là gì:** Nơi lưu files của từng user.

**Structure:**

```
/home/
├── john/        # John's files
│   ├── Documents/
│   ├── Downloads/
│   └── .bashrc  # John's shell config
└── alice/       # Alice's files
    └── ...
```

**Tương đương Windows:**

```
C:\Users\John\     →  /home/john/
C:\Users\Alice\    →  /home/alice/
```

**Shortcut:**

```bash
cd ~              # Go to YOUR home (/home/yourname/)
cd ~john          # Go to John's home (if you have permission)
```

#### `/etc/` - Configuration Files

**Là gì:** "Etcetera" - Configuration files cho system và applications.

**Quan trọng vì:**

- Chứa configs của mọi service
- DevOps hay phải edit files ở đây

**Examples:**

```
/etc/nginx/nginx.conf         # NGINX web server config
/etc/ssh/sshd_config          # SSH server config
/etc/hosts                    # DNS mapping
/etc/passwd                   # User accounts
/etc/crontab                  # Scheduled tasks
```

**Ví dụ thường gặp:**

```bash
# View NGINX config
cat /etc/nginx/nginx.conf

# Edit SSH config (need sudo)
sudo nano /etc/ssh/sshd_config

# View user list
cat /etc/passwd
```

#### `/var/` - Variable Data

**Là gì:** Data thay đổi thường xuyên (logs, databases, cache, ...)

**Most important:**

```
/var/log/          # Application logs
/var/www/          # Web server files
/var/lib/          # Databases, packages state
/var/tmp/          # Temp files (persist across reboots)
```

**DevOps use cases:**

```bash
# Check application logs
tail -f /var/log/nginx/access.log
tail -f /var/log/syslog

# Check disk usage (logs fill up disk!)
du -sh /var/log/*

# Web files location
ls /var/www/html/
```

#### `/tmp/` - Temporary Files

**Là gì:** Files tạm, **bị xóa sau khi restart**.

**Use cases:**

```bash
# Download temp file
cd /tmp
wget https://example.com/file.tar.gz

# Extract here (will be cleaned up later)
tar -xzf file.tar.gz
```

**⚠️ WARNING:**

```bash
# DON'T store important files here!
# Files in /tmp are deleted on reboot
```

#### `/usr/` - User Programs

**Là gì:** User-installed programs (NOT "user data" - đừng nhầm!)

**Structure:**

```
/usr/
├── bin/          # User commands (ls, cat, vim, ...)
├── sbin/         # System admin commands
├── lib/          # Libraries for programs
└── local/        # Locally installed software
```

**Ví dụ:**

```bash
which python3
# Output: /usr/bin/python3

which nginx
# Output: /usr/sbin/nginx
```

#### `/opt/` - Optional Software

**Là gì:** Third-party applications.

**Khi nào dùng:**

```
Install từ distro package manager → /usr/
Install manually (tar.gz from website) → /opt/

Ví dụ:
/opt/google/chrome/
/opt/teamviewer/
/opt/custom-app/
```

#### `/dev/` - Device Files

**Là gì:** Device files (hard disks, USB, ...)

**"Everything is a file" in action:**

```bash
ls /dev/

# Output examples:
/dev/sda          # First hard disk
/dev/sda1         # First partition
/dev/sdb          # Second disk (maybe USB)
/dev/null         # "Black hole" - discard everything
/dev/random       # Random number generator
```

**Ví dụ thực tế:**

```bash
# Write to /dev/null (discard output)
echo "secret" > /dev/null

# Wipe a disk (DANGEROUS!)
sudo dd if=/dev/zero of=/dev/sdb
```

### 4.4. Absolute vs Relative Paths

**Absolute Path:** Bắt đầu từ `/` (root)

```bash
/home/john/Documents/report.txt
/var/log/nginx/access.log
/etc/nginx/nginx.conf
```

**Relative Path:** Từ current directory

```bash
# If you're in /home/john/
Documents/report.txt         # = /home/john/Documents/report.txt
../alice/file.txt           # = /home/alice/file.txt
./script.sh                 # = /home/john/script.sh
```

**Special symbols:**

```
.     Current directory
..    Parent directory
~     Home directory (/home/yourname/)
-     Previous directory
```

**Examples:**

```bash
pwd
# Output: /home/john/Documents

cd ../Downloads      # Go to /home/john/Downloads
cd ~                 # Go to /home/john/
cd -                 # Go back to /home/john/Documents
cd /etc              # Absolute path to /etc
```

---

## 5. Navigation Commands

### 5.1. `pwd` - Print Working Directory

**Là gì:** Hiển thị thư mục hiện tại.

**Syntax:**

```bash
pwd
```

**Ví dụ:**

```bash
pwd
# Output: /home/john/Documents
```

**Khi nào dùng:**

- Lost trong file system
- Verify vị trí trước khi chạy dangerous commands (rm, mv, ...)

**Ẩn dụ:**
"Where am I?" - GPS của terminal

### 5.2. `ls` - List Directory Contents

**Syntax:**

```bash
ls [options] [path]
```

**Basic usage:**

```bash
ls                   # List current directory
ls /home             # List /home directory
ls Documents         # List Documents (relative path)
```

**Common options:**

```bash
ls -l                # Long format (permissions, owner, size, date)
ls -a                # Show hidden files (starting with .)
ls -h                # Human-readable sizes (KB, MB, GB)
ls -t                # Sort by modification time
ls -r                # Reverse order
ls -R                # Recursive (list subdirectories too)
```

**Combined options:**

```bash
ls -lah              # Long + all + human-readable
ls -ltr              # Long + time + reverse (oldest first)
```

**Output explained:**

```bash
$ ls -l

-rw-r--r-- 1 john users  1024 Jan 15 10:30 file.txt
drwxr-xr-x 2 john users  4096 Jan 15 09:00 folder/

Giải thích:
- : regular file
d : directory
rw-r--r-- : permissions
1 : number of links
john : owner
users : group
1024 : size (bytes)
Jan 15 10:30 : last modified
file.txt : name
```

**Real scenarios:**

```bash
# Find largest files
ls -lhS | head -10

# Find newest files
ls -lt | head -10

# Show all files including hidden
ls -la

# Check if directory is empty
ls -A /tmp | wc -l      # If 0, empty
```

### 5.3. `cd` - Change Directory

**Syntax:**

```bash
cd [path]
```

**Examples:**

```bash
cd /home/john        # Absolute path
cd Documents         # Relative path (from current dir)
cd ..                # Go up one level
cd ~                 # Go home
cd                   # Also go home (shortcut)
cd -                 # Go to previous directory
```

**Practical examples:**

```bash
# Scenario: Navigate to web server logs
cd /var/log/nginx
ls -lh access.log

# Quick switch between directories
cd /etc/nginx           # Go to nginx config
cd -                    # Go back to previous dir
cd -                    # Toggle between two dirs
```

**Autocomplete tip:**

```bash
cd /var/lo[TAB]         # Auto-complete to /var/log/
cd Doc[TAB]             # Auto-complete to Documents/
```

### 5.4. `tree` - Directory Tree

**Install (if not available):**

```bash
# Ubuntu/Debian
sudo apt install tree

# CentOS/Fedora
sudo yum install tree
```

**Usage:**

```bash
tree                    # Show tree from current dir
tree -L 2               # Limit depth to 2 levels
tree -d                 # Directories only
tree -a                 # Include hidden files
```

**Example output:**

```bash
$ tree -L 2

.
├── Documents
│   ├── report.pdf
│   └── notes.txt
├── Downloads
│   └── file.tar.gz
└── Pictures
    ├── photo1.jpg
    └── photo2.jpg

3 directories, 5 files
```

---

## 6. File Operations

### 6.1. `touch` - Create Empty File

**Syntax:**

```bash
touch [filename]
```

**Examples:**

```bash
touch file.txt                    # Create empty file
touch file1.txt file2.txt         # Create multiple files
touch "my file.txt"               # File with spaces (use quotes!)
```

**Another use:** Update modification time

```bash
ls -l file.txt
# -rw-r--r-- 1 john users 0 Jan 15 10:00 file.txt

touch file.txt                    # Update timestamp

ls -l file.txt
# -rw-r--r-- 1 john users 0 Jan 15 11:30 file.txt
```

### 6.2. `mkdir` - Create Directory

**Syntax:**

```bash
mkdir [options] directory_name
```

**Examples:**

```bash
mkdir projects                    # Create single directory
mkdir dir1 dir2 dir3              # Create multiple
mkdir -p path/to/deep/folder      # Create parent dirs if needed
```

**The `-p` flag is SUPER useful:**

```bash
# Without -p (will fail if 'path' doesn't exist)
mkdir path/to/folder
# mkdir: cannot create directory 'path/to/folder': No such file or directory

# With -p (creates all missing parents)
mkdir -p path/to/folder
# Success! Creates: path/, path/to/, path/to/folder/
```

**Real scenario:**

```bash
# Create project structure
mkdir -p myapp/{src,tests,docs,config}

# Result:
myapp/
├── src/
├── tests/
├── docs/
└── config/
```

### 6.3. `cp` - Copy Files/Directories

**Syntax:**

```bash
cp [options] source destination
```

**Copy file:**

```bash
cp file.txt backup.txt                        # Copy to new name
cp file.txt /tmp/                             # Copy to directory
cp file.txt /tmp/newname.txt                  # Copy and rename
```

**Copy directory (need `-r` for recursive):**

```bash
cp -r folder1 folder2                         # Copy entire folder
cp -r /var/www/html/ /backup/html-backup/     # Backup web files
```

**Useful options:**

```bash
cp -r folder backup/              # Recursive (for directories)
cp -v file.txt /tmp/              # Verbose (show what's copied)
cp -i file.txt existing.txt       # Interactive (ask before overwrite)
cp -u source/* dest/              # Update (only copy newer files)
cp -p file.txt backup.txt         # Preserve permissions, timestamps
```

**Real scenarios:**

```bash
# Backup config before editing
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# Copy with timestamp
cp file.txt file.txt.$(date +%Y%m%d)
# Result: file.txt.20250124
```

### 6.4. `mv` - Move/Rename

**Syntax:**

```bash
mv [source] [destination]
```

**Rename file:**

```bash
mv oldname.txt newname.txt
```

**Move file:**

```bash
mv file.txt Documents/                # Move to directory
mv file.txt /tmp/newname.txt          # Move and rename
```

**Move directory:**

```bash
mv folder1 folder2                    # Rename folder
mv folder1 /opt/                      # Move folder to /opt/
```

**Move multiple files:**

```bash
mv file1.txt file2.txt file3.txt Documents/
# Last argument must be directory!
```

**Real scenarios:**

```bash
# Organize downloads
mv ~/Downloads/*.pdf ~/Documents/PDFs/

# Rename with timestamp
mv logfile.log logfile.log.$(date +%Y%m%d-%H%M%S)

# Move old logs to archive
mv /var/log/nginx/access.log.* /var/log/archive/
```

### 6.5. `rm` - Remove Files/Directories

**⚠️ NGUY HIỂM - Không có "Recycle Bin" trong Linux!**

**Syntax:**

```bash
rm [options] file
```

**Remove file:**

```bash
rm file.txt                           # Delete file
rm file1.txt file2.txt                # Delete multiple
```

**Remove directory:**

```bash
rm -r folder/                         # Recursive delete
rm -rf folder/                        # Force recursive (no confirmation)
```

**Options:**

```bash
rm -i file.txt                # Interactive (ask confirmation)
rm -f file.txt                # Force (no error if file doesn't exist)
rm -r directory/              # Recursive (for directories)
rm -rf directory/             # Force recursive (DANGEROUS!)
rm -v file.txt                # Verbose (show what's deleted)
```

**⚠️ CẢNH BÁO - Những lệnh CỰC KỲ NGUY HIỂM:**

```bash
sudo rm -rf /                 # DELETE ENTIRE SYSTEM (DON'T RUN!)
sudo rm -rf /*                # ALSO DELETE EVERYTHING (DON'T RUN!)
rm -rf ~                      # DELETE YOUR HOME (BAD!)
```

**Safe practices:**

```bash
# 1. Use -i for confirmation
rm -i important_file.txt

# 2. Test with ls first
ls file_to_delete.txt        # Verify it exists
rm file_to_delete.txt        # Then delete

# 3. Use wildcards carefully
ls *.log                     # See what matches
rm *.log                     # Then delete

# 4. Backup before bulk delete
tar -czf backup.tar.gz logs/
rm -rf logs/
```

**Real scenario - Clean old logs:**

```bash
# Find old log files (check first!)
find /var/log -name "*.log" -mtime +30

# Delete old logs (older than 30 days)
find /var/log -name "*.log" -mtime +30 -delete
```

---

## 7. Text Processing

### 7.1. `cat` - Concatenate and Display

**Syntax:**

```bash
cat [options] [file]
```

**Basic usage:**

```bash
cat file.txt                  # Display file contents
cat file1.txt file2.txt       # Display multiple files
cat file1.txt file2.txt > combined.txt   # Combine files
```

**Create file with cat:**

```bash
cat > newfile.txt             # Type content, Ctrl+D to save
Hello World
This is a test
[Press Ctrl+D]
```

**Real scenarios:**

```bash
# View log file
cat /var/log/syslog

# View config file
cat /etc/nginx/nginx.conf

# Combine log files
cat access.log.1 access.log.2 > combined_access.log
```

**Limitations:**

- Not good for large files (cat dumps everything)
- No scroll back
→ Use `less` for large files

### 7.2. `less` - View File (Paginated)

**Why less > cat for large files:**

- Scrollable
- Search functionality
- Doesn't load entire file to memory

**Usage:**

```bash
less /var/log/syslog
```

**Navigation inside `less`:**

```
Space          Next page
b              Previous page
/pattern       Search forward
?pattern       Search backward
n              Next search result
N              Previous search result
G              Go to end
g              Go to beginning
q              Quit
```

**Examples:**

```bash
# View large log file
less /var/log/nginx/access.log

# Search for "error" in file
less /var/log/syslog
  /error      # Type this inside less
  n           # Next occurrence
  N           # Previous occurrence
```

### 7.3. `head` & `tail` - View Start/End of File

**`head` - First N lines:**

```bash
head file.txt                 # First 10 lines (default)
head -n 20 file.txt           # First 20 lines
head -5 file.txt              # First 5 lines
```

**`tail` - Last N lines:**

```bash
tail file.txt                 # Last 10 lines (default)
tail -n 20 file.txt           # Last 20 lines
tail -5 file.txt              # Last 5 lines
```

**MOST IMPORTANT: `tail -f` (follow):**

```bash
tail -f /var/log/nginx/access.log

# Watches file and shows new lines as they appear
# Perfect for monitoring logs in real-time!
```

**Real scenarios:**

```bash
# Check recent log entries
tail -100 /var/log/syslog

# Monitor application log
tail -f /var/log/myapp/app.log

# Check first lines of large CSV
head -10 data.csv

# Combine head and tail
head -100 file.txt | tail -10    # Lines 91-100
```

### 7.4. `grep` - Search Text

**One of the MOST POWERFUL commands!**

**Syntax:**

```bash
grep [options] pattern [file]
```

**Basic search:**

```bash
grep "error" /var/log/syslog          # Find "error" in syslog
grep "404" /var/log/nginx/access.log  # Find 404 errors
```

**Common options:**

```bash
grep -i "error" file.txt          # Case-insensitive
grep -r "TODO" ./                 # Recursive search in directory
grep -n "error" file.txt          # Show line numbers
grep -v "error" file.txt          # Invert match (exclude)
grep -c "error" file.txt          # Count matching lines
grep -A 3 "error" file.txt        # Show 3 lines After match
grep -B 3 "error" file.txt        # Show 3 lines Before match
grep -C 3 "error" file.txt        # Show 3 lines Context (before+after)
```

**Real-world examples:**

```bash
# Find errors in logs
grep -i "error\|exception\|fatal" /var/log/syslog

# Find IP addresses in access log
grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" access.log

# Find all Python files with "TODO"
grep -r "TODO" --include="*.py" ./

# Count occurrences
grep -c "error" /var/log/syslog      # How many error lines?

# Find in multiple files
grep "config" /etc/nginx/*.conf
```

**Piping with grep:**

```bash
# Filter process list
ps aux | grep nginx

# Find specific service
systemctl list-units | grep running

# Check which Python version
python3 --version | grep -oP "\d+\.\d+"
```

---

*[This README continues with 30+ more pages covering Permissions, Processes, Package Management, Networking, Shell Scripting, Common Mistakes, and Summary... Would you like me to continue, or proceed to create LABS.md next?]*

---

## 8. Permissions & Ownership

### 8.1. Linux Permission Model

**Core concept:** M?i file/directory c� 3 levels of permissions:
- **Owner (User)** - Ngu?i t?o file
- **Group** - Nh�m users c� quy?n truy c?p
- **Others** - T?t c? ngu?i kh�c

**3 types of permissions:**
- **r (read)** - �?c file / List directory
- **w (write)** - S?a file / T?o/x�a files trong directory
- **x (execute)** - Ch?y file / Enter directory

### 8.2. Reading Permissions

```bash
ls -l file.txt
-rw-r--r-- 1 john developers 1024 Jan 25 10:00 file.txt
```

**Breakdown:**
```
-rw-r--r--
�+--++--++--+
� �   �   +--- Others: read only
� �   +------- Group: read only  
� +----------- Owner: read + write
+------------- File type (- = file, d = directory)
```

**Examples:**
```
-rw-r--r--   File: owner can read/write, others read-only
drwxr-xr-x   Directory: owner full access, others read+execute
-rwxrwxrwx   File: everyone full access (DANGEROUS!)
-rw-------   File: only owner can read/write (private)
----------   File: no one can do anything (broken!)
```

### 8.3. Permission Numbers (Octal)

**Each permission has a number:**
- r (read) = 4
- w (write) = 2
- x (execute) = 1

**Calculate total:**
```
rwx = 4+2+1 = 7
rw- = 4+2+0 = 6
r-x = 4+0+1 = 5
r-- = 4+0+0 = 4
-wx = 0+2+1 = 3
-w- = 0+2+0 = 2
--x = 0+0+1 = 1
--- = 0+0+0 = 0
```

**Full permission in numbers:**
```
755 = rwxr-xr-x
    ?   ?   ?
    7   5   5
  Owner Group Others
```

**Common patterns:**
```
644 = rw-r--r--  (Files: owner writable, others readable)
755 = rwxr-xr-x  (Executables/Dirs: owner full, others read+execute)
777 = rwxrwxrwx  (Full access - AVOID in production!)
600 = rw-------  (Private files: only owner)
700 = rwx------  (Private executables)
```

### 8.4. `chmod` - Change Permissions

**Symbolic mode:**
```bash
chmod u+x file.sh         # User +execute
chmod g-w file.txt        # Group -write
chmod o+r file.txt        # Others +read
chmod a+x script.sh       # All +execute
chmod u=rw,g=r,o= file    # Set explicitly
```

**Symbols:**
```
u = user (owner)
g = group
o = others
a = all (ugo)

+ = add permission
- = remove permission
= = set exactly
```

**Numeric mode:**
```bash
chmod 644 file.txt        # rw-r--r--
chmod 755 script.sh       # rwxr-xr-x
chmod 600 secret.txt      # rw-------
chmod 777 file            # rwxrwxrwx (AVOID!)
```

**Recursive:**
```bash
chmod -R 755 folder/      # Apply to folder and all contents
```

**Real scenarios:**
```bash
# Make script executable
chmod +x deploy.sh
./deploy.sh

# Secure SSH private key
chmod 600 ~/.ssh/id_rsa

# Web server files
chmod 644 *.html          # Files readable by web server
chmod 755 cgi-bin/*.cgi   # CGI scripts executable
```

### 8.5. `chown` - Change Owner

**Syntax:**
```bash
chown user file           # Change owner only
chown user:group file     # Change owner and group
chown :group file         # Change group only
```

**Examples:**
```bash
# Change owner to john
sudo chown john file.txt

# Change owner to john, group to developers
sudo chown john:developers file.txt

# Change group only
sudo chown :www-data /var/www/html/index.html

# Recursive
sudo chown -R john:developers /home/john/project/
```

**?? Usually needs sudo!**

**Real scenario - Fix web server permissions:**
```bash
# Web files should be owned by www-data (NGINX/Apache user)
sudo chown -R www-data:www-data /var/www/html/
sudo chmod -R 755 /var/www/html/
```

### 8.6. Special Permissions

**Setuid (4):**
```bash
chmod 4755 file   # rwsr-xr-x
```
File executes with owner's permissions (not user who runs it).

**Setgid (2):**
```bash
chmod 2755 dir    # rwxr-sr-x
```
Files created in directory inherit group.

**Sticky bit (1):**
```bash
chmod 1777 /tmp   # rwxrwxrwt
```
Only owner can delete files (even if others have write permission).

**Example - /tmp directory:**
```bash
ls -ld /tmp
drwxrwxrwt 10 root root 4096 Jan 25 10:00 /tmp
         ?
    Sticky bit (t)
```

---

## 9. Processes & Services

### 9.1. What is a Process?

**Process** = Program dang ch?y tr�n h? th?ng.

**?n d?:**
```
Program (on disk) = Recipe book
Process (in memory) = Cooking session

B?n c� th? cook (run) c�ng recipe (program) nhi?u l?n c�ng l�c
? Nhi?u processes t? 1 program
```

**Every process has:**
- **PID (Process ID)** - Unique number
- **PPID (Parent PID)** - Ai start process n�y
- **User** - Owner c?a process
- **CPU %** - CPU usage
- **Memory %** - RAM usage
- **State** - Running, Sleeping, Stopped, Zombie

### 9.2. `ps` - Process Status

**Basic usage:**
```bash
ps                # Show YOUR processes in current terminal
ps -u john        # Show processes of user john
ps aux            # Show ALL processes (most common)
```

**Example output:**
```bash
ps aux

USER  PID %CPU %MEM    VSZ   RSS TTY   STAT START TIME COMMAND
john  1234  0.5  2.1 123456 12345 ?     S    10:00 0:05 /usr/bin/python3 app.py
john  5678  0.0  0.3  45678  4567 pts/0 R+   10:30 0:00 ps aux
root  1     0.0  0.5 167890 16789 ?     Ss   09:00 0:12 /sbin/init
```

**Columns explained:**
- **USER** - Owner
- **PID** - Process ID
- **%CPU** - CPU usage percentage
- **%MEM** - Memory usage percentage
- **VSZ** - Virtual memory size (KB)
- **RSS** - Resident set size (actual RAM used, KB)
- **TTY** - Terminal (? = no terminal, pts/0 = pseudo-terminal)
- **STAT** - State (R=Running, S=Sleeping, Z=Zombie, T=Stopped)
- **START** - When started
- **TIME** - CPU time used
- **COMMAND** - Command that started process

**Finding specific process:**
```bash
ps aux | grep nginx
ps aux | grep python
ps aux | grep mysql
```

### 9.3. `top` - Interactive Process Monitor

**Launch:**
```bash
top
```

**Display:**
```
top - 10:30:15 up 5 days, 3:24, 2 users, load average: 0.15, 0.25, 0.20
Tasks: 215 total, 1 running, 214 sleeping, 0 stopped, 0 zombie
%Cpu(s): 5.2 us, 2.1 sy, 0.0 ni, 92.5 id, 0.2 wa, 0.0 hi, 0.0 si, 0.0 st
MiB Mem: 7823.5 total, 2156.3 free, 3421.2 used, 2246.0 buff/cache
MiB Swap: 2048.0 total, 2048.0 free, 0.0 used. 4102.3 avail Mem

  PID USER     PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 1234 john     20   0 1234567 123456  12345 S   5.0   1.6   1:23.45 python3
 5678 www-data 20   0  456789  45678   4567 S   2.0   0.6   0:15.67 nginx
```

**Navigation in top:**
```
q          Quit
k          Kill process (enter PID)
M          Sort by memory
P          Sort by CPU
u          Filter by user
1          Show individual CPU cores
```

**Useful for:**
- Finding high CPU/memory usage
- Real-time monitoring
- Quick process killing

### 9.4. `htop` - Better than top

**Install:**
```bash
sudo apt install htop    # Ubuntu/Debian
sudo yum install htop    # CentOS
```

**Launch:**
```bash
htop
```

**Better because:**
- Mouse support
- Color-coded
- Tree view (see parent-child relationships)
- Easier to use

**Navigation:**
```
F2         Setup
F3         Search
F4         Filter
F5         Tree view
F9         Kill
F10        Quit
```

### 9.5. `kill` - Terminate Process

**Syntax:**
```bash
kill [signal] PID
```

**Common signals:**
```
-15 (SIGTERM)  "Please terminate" (graceful, allows cleanup)
-9 (SIGKILL)   "Die immediately" (forceful, no cleanup)
-1 (SIGHUP)    "Reload config"
```

**Examples:**
```bash
# Graceful shutdown (recommended)
kill 1234              # Default = SIGTERM (-15)
kill -15 1234          # Same as above

# Force kill (when graceful doesn't work)
kill -9 1234

# Reload config without restart
kill -1 1234           # Useful for NGINX, Apache
```

**Kill by name:**
```bash
killall nginx          # Kill all nginx processes
pkill python           # Kill all python processes
```

**Real scenario - Stuck process:**
```bash
# Find process
ps aux | grep myapp
# john  5678  99.0  50.0 ...

# Try graceful first
kill 5678
sleep 5

# Still running? Force kill
kill -9 5678
```

### 9.6. Background & Foreground

**Run in background:**
```bash
./long-running-script.sh &     # & = background
```

**Output:**
```
[1] 12345           # [Job number] PID
```

**List background jobs:**
```bash
jobs
```

**Output:**
```
[1]+  Running     ./long-running-script.sh &
```

**Bring to foreground:**
```bash
fg %1              # %1 = job number 1
```

**Send running process to background:**
```
1. Press Ctrl+Z (pause process)
2. bg (resume in background)
```

**Example flow:**
```bash
# Start process
./script.sh

# Oops, taking too long, want to background it
# Press Ctrl+Z
^Z
[1]+  Stopped     ./script.sh

# Continue in background
bg
[1]+ ./script.sh &

# Check
jobs
[1]+  Running     ./script.sh &
```

### 9.7. `systemctl` - Service Management

**Modern Linux uses systemd for service management.**

**Common commands:**
```bash
systemctl start nginx           # Start service
systemctl stop nginx            # Stop service
systemctl restart nginx         # Stop then start
systemctl reload nginx          # Reload config without restart
systemctl status nginx          # Check status
systemctl enable nginx          # Auto-start on boot
systemctl disable nginx         # Don't auto-start on boot
```

**Example output:**
```bash
systemctl status nginx

? nginx.service - A high performance web server
   Loaded: loaded (/lib/systemd/system/nginx.conf; enabled)
   Active: active (running) since Mon 2025-01-25 10:00:00 UTC; 2h ago
 Main PID: 1234 (nginx)
   Tasks: 5 (limit: 4915)
   Memory: 12.3M
   CGroup: /system.slice/nginx.service
           +-1234 nginx: master process
           +-1235 nginx: worker process
```

**List all services:**
```bash
systemctl list-units --type=service
systemctl list-units --type=service --state=running
```

**Real scenarios:**
```bash
# Restart web server after config change
sudo systemctl restart nginx

# Check if database is running
systemctl status postgresql

# Enable service to start on boot
sudo systemctl enable docker

# Stop a service
sudo systemctl stop apache2
```

---

## 10. Package Management

### 10.1. What is a Package Manager?

**Package Manager** = App Store for Linux.

**Functions:**
- Install software
- Update software
- Remove software
- Manage dependencies

**Different distros use different package managers:**
```
Ubuntu/Debian ? apt
CentOS/RHEL ? yum/dnf
Fedora ? dnf
Arch ? pacman
```

**In this course:** We focus on **apt** (Ubuntu/Debian).

### 10.2. `apt` - Advanced Package Tool

**Update package list:**
```bash
sudo apt update
```

**Upgrade installed packages:**
```bash
sudo apt upgrade          # Upgrade all
sudo apt upgrade nginx    # Upgrade specific package
```

**Install package:**
```bash
sudo apt install nginx
sudo apt install git curl wget
```

**Remove package:**
```bash
sudo apt remove nginx            # Remove but keep config
sudo apt purge nginx             # Remove including config
sudo apt autoremove              # Remove unused dependencies
```

**Search for package:**
```bash
apt search nginx
apt search web server
```

**Show package info:**
```bash
apt show nginx
apt policy nginx        # Show available versions
```

**Real workflow:**
```bash
# 1. Update package list
sudo apt update

# 2. Search for package
apt search htop

# 3. Show info
apt show htop

# 4. Install
sudo apt install htop

# 5. Verify installation
which htop
htop --version
```

### 10.3. Common Packages for DevOps

```bash
# Essential tools
sudo apt install git curl wget vim nano

# Monitoring tools
sudo apt install htop nethogs iotop

# Networking tools
sudo apt install net-tools dnsutils traceroute

# System tools
sudo apt install tree lsof

# Development
sudo apt install build-essential python3-pip

# Docker (special installation)
# Follow official Docker docs, not just apt install docker
```

---

## 11. Networking Basics

### 11.1. `ifconfig` / `ip` - Network Interfaces

**Modern command (use this):**
```bash
ip addr show
ip a       # Short version
```

**Example output:**
```
2: eth0: <BROADCAST,MULTICAST,UP> mtu 1500
    inet 192.168.1.100/24 brd 192.168.1.255 scope global eth0
    inet6 fe80::a00:27ff:fe4e:66a1/64 scope link
```

**Key info:**
- **eth0** - Interface name
- **192.168.1.100** - IP address
- **/24** - Subnet mask
- **UP** - Interface is active

**Old command (deprecated but still common):**
```bash
ifconfig
```

### 11.2. `ping` - Test Connectivity

```bash
ping google.com
ping 8.8.8.8           # Google DNS
ping -c 4 google.com   # Send only 4 packets
```

**Output:**
```
PING google.com (142.250.185.46) 56(84) bytes of data.
64 bytes from google.com: icmp_seq=1 ttl=117 time=25.3 ms
64 bytes from google.com: icmp_seq=2 ttl=117 time=24.1 ms
```

**Press Ctrl+C to stop.**

### 11.3. `netstat` / `ss` - Network Connections

**Show listening ports:**
```bash
sudo netstat -tulpn    # Old
sudo ss -tulpn         # New (faster)
```

**Output:**
```
tcp   LISTEN   0   128   0.0.0.0:80    0.0.0.0:*   users:(("nginx",pid=1234))
tcp   LISTEN   0   128   0.0.0.0:22    0.0.0.0:*   users:(("sshd",pid=5678))
```

**Useful for:**
- Check if port is in use
- Find which process listens on which port
- Troubleshoot port conflicts

---

## 12. Shell Scripting Introduction

### 12.1. What is Shell Scripting?

**Shell script** = File containing series of commands.

**Instead of typing:**
```bash
cd /var/www/html
git pull
systemctl restart nginx
```

**Every time, create script:**
```bash
#!/bin/bash
cd /var/www/html
git pull
systemctl restart nginx
```

**Run once:** `./deploy.sh`

### 12.2. Creating First Script

**Create file:**
```bash
nano hello.sh
```

**Content:**
```bash
#!/bin/bash
# My first script

echo "Hello, DevOps!"
echo "Current date: $(date)"
echo "Current user: $(whoami)"
```

**Make executable:**
```bash
chmod +x hello.sh
```

**Run:**
```bash
./hello.sh
```

**Output:**
```
Hello, DevOps!
Current date: Wed Jan 25 10:30:15 UTC 2025
Current user: john
```

### 12.3. Variables

```bash
#!/bin/bash

NAME="John"
AGE=25

echo "Name: $NAME"
echo "Age: $AGE"
```

### 12.4. User Input

```bash
#!/bin/bash

echo "What is your name?"
read NAME

echo "Hello, $NAME!"
```

**[Shell scripting topic continues in advanced modules...]*

---

## 13. Common Mistakes

### Mistake 1: Running rm -rf without thinking

```bash
# DANGER!
sudo rm -rf /*      # Deletes EVERYTHING
rm -rf ~/*          # Deletes YOUR home
```

**Prevention:**
- Always double-check before running rm -rf
- Use ls first to see what would be deleted
- Use -i flag for confirmation
- Backup important data

### Mistake 2: chmod 777 everywhere

```bash
# BAD!
chmod 777 file.txt
chmod -R 777 /var/www/
```

**Why bad:** Security risk! Everyone can read/write/execute.

**Correct:**
```bash
chmod 644 file.txt         # Files
chmod 755 directory/       # Directories
chmod 600 private.key      # Secrets
```

### Mistake 3: Editing production config directly

```bash
# RISKY!
sudo nano /etc/nginx/nginx.conf
# Make changes...
sudo systemctl restart nginx
# Oops! Syntax error, site is down!
```

**Better:**
```bash
# 1. Backup first
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# 2. Edit
sudo nano /etc/nginx/nginx.conf

# 3. Test config
sudo nginx -t

# 4. If OK, restart
sudo systemctl restart nginx

# 5. If broken, restore
sudo mv /etc/nginx/nginx.conf.backup /etc/nginx/nginx.conf
```

---

## 14. T?ng k?t

### ? B?n d� h?c du?c g�?

**Commands mastered:**
- Navigation: pwd, ls, cd
- Files: touch, cat, cp, mv, rm
- Directories: mkdir, rmdir
- Text: less, head, tail, grep
- Permissions: chmod, chown
- Processes: ps, top, htop, kill, systemctl
- Packages: apt
- Networking: ip, ping, ss

**Concepts understood:**
- Linux file system hierarchy
- Everything is a file
- Permission model (rwx)
- Processes vs Programs
- Package management

**Skills gained:**
- Navigate Linux confidently
- Troubleshoot permission issues
- Manage processes
- Read and analyze logs
- Basic shell scripting

### ?? Next Module

**Module 02: GIT & GITHUB** - Version control v� collaboration

### ?? Self-Assessment

B?n c� th? t? tin tr? l?i:
- [ ] Ph�n bi?t absolute vs relative path?
- [ ] Gi?i th�ch permission `-rw-r--r--`?
- [ ] Kill m?t process dang ch?y?
- [ ] C�i d?t package b?ng apt?
- [ ] T�m files ch?a text "error"?

**N?u YES t?t c? ? S?n s�ng Module 02!**

---

**Module 01 Complete! ??**
