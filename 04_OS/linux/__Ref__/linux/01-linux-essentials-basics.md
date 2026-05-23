# 🐧 Linux Essentials — Kiến thức nền tảng Linux

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Prerequisite: `terminal/01-terminal-basics.md`
> Mọi developer cần biết Linux — servers, Docker, Cloud đều chạy Linux.

---

## Tại sao developer cần biết Linux?

- **96%+ web servers** chạy Linux (Ubuntu, CentOS, Debian)
- **Docker containers** = Linux Containers
- **Cloud** (AWS, GCP, Azure) = Linux VMs
- **DevOps/SRE** = quản lý Linux servers
- **WSL** trên Windows = Linux ngay trên máy bạn

---

## 1. Filesystem Hierarchy — Cấu trúc thư mục

```
/                           # Root — gốc của mọi thứ
├── bin/                    # Essential binaries (ls, cp, cat)
├── sbin/                   # System binaries (iptables, mount)
├── etc/                    # Configuration files ⭐
│   ├── nginx/nginx.conf
│   ├── ssh/sshd_config
│   └── hosts
├── home/                   # User home directories
│   └── thanh/              # ~ (home dir)
├── root/                   # Root user's home
├── var/                    # Variable data
│   ├── log/                # System logs ⭐
│   └── www/                # Web server files
├── tmp/                    # Temporary files (cleared on reboot)
├── usr/                    # User programs
│   ├── bin/                # User binaries
│   ├── lib/                # Libraries
│   └── local/              # Locally compiled programs
├── opt/                    # Optional/third-party software
├── dev/                    # Device files
├── proc/                   # Process info (virtual filesystem)
└── sys/                    # System info (virtual filesystem)
```

---

## 2. Users & Permissions

### User management

```bash
# User info
whoami                      # Current user
id                          # User ID, group IDs
groups                      # List groups

# Create/modify users (need sudo)
sudo adduser newuser        # Create user interactively
sudo usermod -aG docker newuser  # Add user to group
sudo passwd newuser         # Change password
sudo userdel -r newuser     # Delete user + home dir

# Switch user
su - username               # Switch to user (need password)
sudo -u username command    # Run command as another user
```

### File Permissions — rwx

```
Ý nghĩa: r=read, w=write, x=execute

Permission cấu trúc: [user][group][others]

-rwxr-xr-- 1 thanh developers 4096 Jan 15 10:30 script.sh
│└┬┘└┬┘└┬┘   │      │
│ │   │   │   owner  group
│ │   │   └── Others: r-- (read only)
│ │   └────── Group:  r-x (read + execute)
│ └────────── User:   rwx (full access)
└──────────── Type:   - (file), d (directory), l (link)
```

```bash
# Thay đổi permissions
chmod 755 script.sh         # rwxr-xr-x (owner full, others read+execute)
chmod 644 config.txt        # rw-r--r-- (owner read/write, others read)
chmod +x script.sh          # Add execute permission
chmod u+w,g-w file.txt      # User +write, group -write

# Octal notation:
# r=4, w=2, x=1
# 7=rwx, 6=rw-, 5=r-x, 4=r--, 0=---

# Change owner
sudo chown user:group file.txt
sudo chown -R user:group dir/   # Recursive
```

---

## 3. Package Management

```bash
# ── Debian/Ubuntu (apt) ──
sudo apt update                 # Update package list
sudo apt upgrade                # Upgrade all packages
sudo apt install nginx          # Install package
sudo apt remove nginx           # Remove package
sudo apt autoremove             # Remove unused dependencies
apt search keyword              # Search packages
apt list --installed            # List installed

# ── RHEL/CentOS (dnf/yum) ──
sudo dnf update
sudo dnf install nginx
sudo dnf remove nginx

# ── Alpine (apk) — Docker containers ──
apk update
apk add nginx
apk del nginx
```

---

## 4. Services (systemd)

```bash
# ── Service management ──
sudo systemctl start nginx      # Start service
sudo systemctl stop nginx       # Stop service
sudo systemctl restart nginx    # Restart
sudo systemctl reload nginx     # Reload config (no downtime)
sudo systemctl enable nginx     # Auto-start on boot
sudo systemctl disable nginx    # Don't auto-start
sudo systemctl status nginx     # Check status ⭐

# ── View logs ──
journalctl -u nginx             # Logs of specific service
journalctl -u nginx -f          # Follow (tail) logs
journalctl -u nginx --since "1 hour ago"
journalctl -xe                  # Recent errors with explanation
```

---

## 5. SSH — Secure Shell

```bash
# ── Connect to server ──
ssh user@server-ip
ssh -p 2222 user@server        # Custom port
ssh -i ~/.ssh/mykey.pem user@server  # With key file

# ── SSH Key setup (recommended over password) ──
ssh-keygen -t ed25519 -C "your@email.com"
# Creates: ~/.ssh/id_ed25519 (private) + ~/.ssh/id_ed25519.pub (public)

ssh-copy-id user@server        # Copy public key to server
# OR manually:
cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys  # On server

# ── SSH config (~/.ssh/config) ──
Host myserver
    HostName 192.168.1.100
    User thanh
    Port 22
    IdentityFile ~/.ssh/id_ed25519

# Giờ chỉ cần: ssh myserver

# ── SCP — Copy files ──
scp file.txt user@server:/path/    # Local → remote
scp user@server:/path/file.txt .   # Remote → local
scp -r dir/ user@server:/path/     # Copy directory

# ── SSH Tunnel ──
ssh -L 8080:localhost:3000 user@server
# Truy cập localhost:8080 → forward đến server:3000
```

---

## 6. Environment Variables

```bash
# Xem variables
echo $PATH
echo $HOME
env                             # All environment variables
printenv USER                   # Specific variable

# Set variables
export MY_VAR="value"           # Set for current session
echo 'export MY_VAR="value"' >> ~/.bashrc   # Persistent

# PATH — nơi shell tìm executables
echo $PATH
# /usr/local/bin:/usr/bin:/bin

export PATH="$PATH:/my/custom/bin"   # Append to PATH

# Common env vars
HOME=/home/thanh               # Home directory
USER=thanh                     # Current user
SHELL=/bin/bash                # Current shell
EDITOR=vim                     # Default editor
LANG=en_US.UTF-8               # Language/locale
```

---

## 7. Cron Jobs — Scheduled Tasks

```bash
# Edit cron table
crontab -e

# Format: MIN HOUR DAY MONTH WEEKDAY COMMAND
# ┌─── Minute (0-59)
# │ ┌─── Hour (0-23)  
# │ │ ┌─── Day of month (1-31)
# │ │ │ ┌─── Month (1-12)
# │ │ │ │ ┌─── Day of week (0-7, 0=7=Sunday)
# │ │ │ │ │
# * * * * * command

# Examples
0 * * * *    /scripts/hourly.sh      # Every hour
0 2 * * *    /scripts/backup.sh      # Daily at 2:00 AM
0 0 * * 0    /scripts/weekly.sh      # Every Sunday midnight
*/5 * * * *  /scripts/health.sh      # Every 5 minutes
0 9 1 * *    /scripts/monthly.sh     # 1st of every month at 9 AM

# View cron jobs
crontab -l

# System-wide cron
ls /etc/cron.d/
ls /etc/cron.daily/
```

---

## 8. Disk & Storage

```bash
# Disk usage
df -h                   # Filesystem usage
du -sh /var/log         # Directory size
lsblk                   # List block devices
fdisk -l                # Disk partitions

# Mount
sudo mount /dev/sdb1 /mnt/usb
sudo umount /mnt/usb
cat /etc/fstab          # Auto-mount config
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | Chạy mọi thứ bằng `root` | Dùng user bình thường + `sudo` | Least privilege principle |
| 2 | `chmod 777` cho mọi file | Dùng `chmod 644` (file) / `chmod 755` (dir) | 777 = anyone can write = security hole |
| 3 | Quên `sudo apt update` trước install | Luôn `apt update` trước `apt install` | Package list cũ → install fail |
| 4 | Edit config gốc không backup | `cp config.conf config.conf.bak` trước khi edit | Rollback khi config sai |
| 5 | Password SSH auth trên production | Dùng SSH key auth, disable password | Brute force attacks |

---

## Bài tập thực hành

- [ ] **Bài 1 (Dễ):** Setup SSH key + config file, connect không cần password
- [ ] **Bài 2 (Trung bình):** Tạo user mới, set permissions cho web directory
- [ ] **Bài 3 (Trung bình):** Cài Nginx, enable service, check status, xem logs
- [ ] **Bài 4 (Khó):** Setup cron job backup database daily, gửi log qua email

---

## Tài nguyên thêm

- [Linux Journey](https://linuxjourney.com/) — Interactive learning
- [OverTheWire: Bandit](https://overthewire.org/wargames/bandit/) — Learn Linux qua CTF game
- [The Linux Command Line (William Shotts)](https://linuxcommand.org/tlcl.php) — Free book
- [Linux Upskill Challenge](https://linuxupskillchallenge.org/) — 20-day challenge
