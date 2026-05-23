# 🔧 Linux Administration — Quản trị hệ thống Linux

> `[INTERMEDIATE → ADVANCED]` — Prerequisite: `01-linux-essentials-basics.md`
> System administration, process management, storage, networking, và security nâng cao.

---

## 1. Process Management Nâng cao

### Process States

```
R — Running/Runnable    (đang chạy hoặc sẵn sàng)
S — Sleeping            (đang chờ event: I/O, signal)
D — Uninterruptible     (đang chờ disk I/O — KHÔNG kill được)
Z — Zombie              (đã exit nhưng parent chưa wait())
T — Stopped             (Ctrl+Z hoặc SIGSTOP)
```

### Process Inspection

```bash
# Detailed process info
ps aux                              # Tất cả processes
ps aux --sort=-%mem | head -20      # Top 20 by memory ⭐
ps aux --sort=-%cpu | head -20      # Top 20 by CPU
ps -ef --forest                     # Process tree

# Real-time monitoring
top                                 # Basic monitor
htop                                # Interactive monitor ⭐
atop                                # Advanced (disk, network)

# Specific process
pgrep -f "python app"               # Find PID by name
pidof nginx                         # PID of program

# /proc filesystem — process info
cat /proc/<PID>/status              # Process details
cat /proc/<PID>/cmdline             # Command line
ls -la /proc/<PID>/fd               # Open file descriptors
cat /proc/<PID>/environ             # Environment variables

# File descriptors & open files
lsof -p <PID>                      # Files opened by process
lsof -i :8080                      # Process using port 8080
lsof +D /var/log                   # Processes using directory
```

### Signal Management

```bash
# Common signals
kill <PID>                  # SIGTERM (15) — graceful terminate
kill -9 <PID>               # SIGKILL (9) — force kill ⚠️
kill -HUP <PID>             # SIGHUP (1) — reload config (nginx, apache)
kill -USR1 <PID>            # SIGUSR1 — custom action (log rotation)

# Signal table:
# 1  SIGHUP    — Hangup (often: reload config)
# 2  SIGINT    — Interrupt (Ctrl+C)
# 9  SIGKILL   — Force kill (can't be caught!)
# 15 SIGTERM   — Graceful terminate (default)
# 18 SIGCONT   — Continue stopped process
# 19 SIGSTOP   — Stop process (can't be caught!)
# 20 SIGTSTP   — Terminal stop (Ctrl+Z)
```

### Resource Limits

```bash
# View limits
ulimit -a                   # All limits
ulimit -n                   # Max open files (default: 1024)
ulimit -u                   # Max user processes

# Tăng limits (temporary)
ulimit -n 65536             # Set max open files

# Permanent limits (/etc/security/limits.conf)
# <user>   <type>  <item>    <value>
# nginx    soft    nofile    65536
# nginx    hard    nofile    65536
# *        soft    nproc     4096
```

---

## 2. System Performance Analysis

### CPU, Memory, Disk, Network

```bash
# ── CPU ──
uptime                      # Load average (1, 5, 15 min)
mpstat -P ALL 1             # Per-CPU stats every 1 second
vmstat 1                    # Virtual memory statistics
sar -u 1 5                  # CPU usage every 1sec, 5 samples

# ── Memory ──
free -h                     # Memory overview
vmstat -s                   # Detailed memory stats
cat /proc/meminfo           # Raw memory info
slabtop                     # Kernel slab cache

# ── Disk I/O ──
iostat -xz 1                # Disk I/O stats
iotop                       # Real-time I/O by process
hdparm -Tt /dev/sda         # Disk speed test

# ── Network ──
iftop                       # Real-time bandwidth by connection
nethogs                     # Bandwidth by process
ss -tuln                    # Listening ports ⭐
ss -s                       # Socket statistics summary
nload                       # Real-time network traffic

# ── Comprehensive ──
dstat                       # All-in-one: CPU, disk, net, memory
glances                     # Modern system monitor
```

### Load Average

```
Load average: 2.50, 1.80, 0.90
              1min  5min  15min

Ý nghĩa (trên máy 4 cores):
  < 4.0  — OK, system idle
  = 4.0  — 100% utilized (1.0 per core)
  > 4.0  — Overloaded, processes waiting

Quy tắc: Load average nên < số CPU cores × 0.7
```

---

## 3. Storage Management

### LVM (Logical Volume Manager)

```bash
# LVM layers: Physical Volume → Volume Group → Logical Volume

# Create PV from disk
sudo pvcreate /dev/sdb

# Create Volume Group
sudo vgcreate data-vg /dev/sdb

# Create Logical Volume
sudo lvcreate -L 50G -n data-lv data-vg

# Format & Mount
sudo mkfs.ext4 /dev/data-vg/data-lv
sudo mkdir /data
sudo mount /dev/data-vg/data-lv /data

# Extend volume (NO DOWNTIME!)
sudo lvextend -L +20G /dev/data-vg/data-lv
sudo resize2fs /dev/data-vg/data-lv    # ext4
sudo xfs_growfs /data                   # xfs
```

### RAID

```
RAID 0:  Striping — Fast, NO redundancy
RAID 1:  Mirroring — 2x copies, 50% capacity loss
RAID 5:  Striping + parity — 1 disk failure tolerance
RAID 6:  Striping + double parity — 2 disk failure
RAID 10: Mirror + stripe — Performance + redundancy ⭐
```

---

## 4. Security Hardening

```bash
# ── SSH hardening (/etc/ssh/sshd_config) ──
PermitRootLogin no              # Disable root SSH
PasswordAuthentication no       # Key-only auth ⭐
Port 2222                       # Change default port
MaxAuthTries 3                  # Limit login attempts
AllowUsers deployer admin       # Whitelist users

sudo systemctl restart sshd

# ── Firewall (ufw — Ubuntu) ──
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp           # SSH
sudo ufw allow 80/tcp           # HTTP
sudo ufw allow 443/tcp          # HTTPS
sudo ufw status verbose

# ── Firewall (firewalld — RHEL/CentOS) ──
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload

# ── Fail2ban — block brute force ──
sudo apt install fail2ban
# /etc/fail2ban/jail.local
# [sshd]
# enabled = true
# maxretry = 3
# bantime = 3600
sudo systemctl enable fail2ban

# ── Auto updates ──
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades
```

---

## 5. Log Management

```bash
# System logs
journalctl -xe                      # Recent errors
journalctl -u nginx --since today   # Service logs today
journalctl --disk-usage             # Log disk usage
journalctl --vacuum-size=500M       # Cleanup logs

# Traditional logs (/var/log/)
tail -f /var/log/syslog             # System log
tail -f /var/log/auth.log           # Authentication log
tail -f /var/log/nginx/access.log   # Nginx access

# Log rotation (/etc/logrotate.d/)
# /var/log/myapp/*.log {
#     daily
#     rotate 14
#     compress
#     missingok
#     notifempty
#     create 0640 www-data www-data
# }
```

---

## 6. Backup Strategies

```bash
# rsync — incremental backup ⭐
rsync -avz --delete /data/ /backup/data/   # Local backup
rsync -avz -e ssh /data/ user@backup-server:/backup/

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M)
BACKUP_DIR="/backup/${DATE}"
mkdir -p "$BACKUP_DIR"

# Database backup
mysqldump --all-databases | gzip > "${BACKUP_DIR}/db.sql.gz"

# Files backup
rsync -av --exclude='node_modules' /var/www/ "${BACKUP_DIR}/www/"

# Cleanup old backups (keep 7 days)
find /backup -maxdepth 1 -mtime +7 -exec rm -rf {} \;

echo "Backup completed: ${BACKUP_DIR}"
```

---

## Gotchas — Những lỗi thường gặp

| # | ❌ Sai | ✅ Đúng | Giải thích |
|---|--------|---------|------------|
| 1 | `kill -9` là default | Dùng `kill` (SIGTERM) trước, `-9` khi cần | SIGTERM cho app cleanup trước khi exit |
| 2 | Quên monitor disk space | Setup alert khi > 80% | Disk full → service crash |
| 3 | Không backup trước upgrade | `apt upgrade` sau khi snapshot/backup | Rollback khi upgrade fail |
| 4 | Root login qua SSH | Disable root SSH, dùng sudo user | Security best practice |
| 5 | Ignore log rotation | Setup logrotate cho mọi app | Logs chiếm hết disk |

---

## Bài tập thực hành

- [ ] **Bài 1 (Trung bình):** SSH hardening — disable root, key-only auth, change port
- [ ] **Bài 2 (Trung bình):** Setup firewall (ufw/firewalld) cho web server
- [ ] **Bài 3 (Khó):** Setup LVM, extend volume without downtime
- [ ] **Bài 4 (Khó):** Write automated backup script with cron job

---

## Tài nguyên thêm

- [Linux Performance Analysis (Brendan Gregg)](https://www.brendangregg.com/linuxperf.html) — Performance analysis bible
- [Linux System Administration Handbook](https://www.admin.com/) — Comprehensive reference
- [DigitalOcean Community Tutorials](https://www.digitalocean.com/community/tutorials) — Practical Linux guides
- [Hardening Checklist](https://github.com/trimstray/the-practical-linux-hardening-guide) — Security checklist
