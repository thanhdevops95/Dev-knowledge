# 🐧 Linux Administration — Quản trị hệ thống

> `[INTERMEDIATE]` — Kiến thức cần thiết cho mọi developer/devops

---

## 1. User & Permission Management

```bash
# Tạo user / group
sudo useradd -m -s /bin/bash -G sudo,docker devuser
sudo passwd devuser

# Quản lý groups
sudo groupadd developers
sudo usermod -aG developers devuser    # Thêm user vào group
groups devuser                           # Xem groups của user

# File permissions
# rwx rwx rwx = owner group others
# r=4 w=2 x=1

chmod 755 script.sh      # Owner: rwx, Group: r-x, Others: r-x
chmod 644 config.yaml    # Owner: rw-, Group: r--, Others: r--
chmod +x deploy.sh       # Thêm execute cho tất cả
chown devuser:developers /var/www   # Đổi owner
chown -R devuser:devuser /app       # Đổi recursive

# Special permissions
chmod u+s /usr/bin/prog   # SUID: chạy với quyền owner
chmod g+s /shared/        # SGID: file mới kế thừa group
chmod +t /tmp/            # Sticky bit: chỉ owner xóa được file
```

---

## 2. Process Management

```bash
# Xem processes
ps aux                    # Tất cả processes
ps aux | grep node        # Tìm Node process
top                       # Monitor real-time
htop                      # htop (interactive, đẹp hơn)

# Quản lý processes
kill PID                  # Gửi SIGTERM (graceful shutdown)
kill -9 PID               # Gửi SIGKILL (force kill)
kill -HUP PID             # Reload config (Nginx, etc.)
pkill -f "node server"    # Kill theo tên command

# Background jobs
nohup node server.js &    # Chạy background, không chết khi logout
disown %1                 # Tách job khỏi terminal

# systemd (production)
sudo systemctl start myapp     # Bật service
sudo systemctl stop myapp      # Tắt
sudo systemctl restart myapp   # Restart
sudo systemctl enable myapp    # Auto-start khi boot
sudo systemctl status myapp    # Xem trạng thái
journalctl -u myapp -f         # Xem logs real-time
```

### Tạo systemd service

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Node.js App
After=network.target

[Service]
Type=simple
User=devuser
WorkingDirectory=/var/www/myapp
ExecStart=/usr/bin/node dist/main.js
Restart=on-failure
RestartSec=5
Environment=NODE_ENV=production
Environment=PORT=3000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now myapp
```

---

## 3. Networking

```bash
# Xem network interfaces
ip addr show              # IP addresses
ip route show             # Routing table

# Port management
ss -tulnp                 # Ports đang listen (thay netstat)
ss -tulnp | grep :3000    # Ai đang dùng port 3000?
lsof -i :3000             # Process nào đang listen port 3000

# Firewall (UFW — Ubuntu)
sudo ufw enable
sudo ufw allow 22/tcp     # SSH
sudo ufw allow 80/tcp     # HTTP
sudo ufw allow 443/tcp    # HTTPS
sudo ufw deny 3306/tcp    # Block MySQL from outside
sudo ufw status

# DNS lookup
dig example.com           # DNS records
nslookup example.com      # Simpler DNS lookup
host example.com          # Simplest

# Network debugging
ping google.com           # Connectivity test
traceroute google.com     # Route tracing
curl -I https://api.com   # HTTP headers only
curl -v https://api.com   # Verbose (SSL, headers, body)
wget https://file.com/f   # Download file
```

---

## 4. Disk & Storage

```bash
# Xem dung lượng
df -h                     # Disk usage (tổng)
du -sh /var/log/*         # Thư mục nào nặng nhất?
du -sh * | sort -rh | head -10   # Top 10 thư mục nặng nhất

# Dọn dẹp
sudo apt autoremove       # Xóa packages không cần
sudo journalctl --vacuum-size=100M  # Giới hạn logs 100MB
docker system prune -a    # Xóa Docker rác

# Mount disk
lsblk                     # Liệt kê block devices
sudo mkfs.ext4 /dev/sdb1  # Format
sudo mount /dev/sdb1 /mnt/data
# Auto-mount khi boot: thêm vào /etc/fstab
echo '/dev/sdb1 /mnt/data ext4 defaults 0 2' | sudo tee -a /etc/fstab
```

---

## 5. Log Management

```bash
# System logs
journalctl -f              # Follow system logs
journalctl -u nginx --since "1 hour ago"
journalctl --disk-usage    # Logs đang chiếm bao nhiêu?

# Application logs
tail -f /var/log/nginx/access.log
tail -100 /var/log/nginx/error.log
grep "ERROR" /var/log/myapp/*.log | tail -20

# Log rotation
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily
    missingok
    rotate 14          # Giữ 14 ngày
    compress           # Nén file cũ
    delaycompress
    notifempty
    create 0640 devuser devuser
    postrotate
        systemctl reload myapp
    endscript
}
```

---

## 6. SSH & Security

```bash
# SSH key pair
ssh-keygen -t ed25519 -C "devuser@company.com"
ssh-copy-id user@server   # Copy public key lên server

# SSH config (~/.ssh/config)
Host prod
    HostName 10.0.1.100
    User devuser
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host staging
    HostName 10.0.2.100
    User devuser

# Sau đó chỉ cần: ssh prod

# Hardening SSH (/etc/ssh/sshd_config)
PermitRootLogin no             # Không cho login root
PasswordAuthentication no      # Chỉ dùng SSH key
MaxAuthTries 3
AllowUsers devuser deploy
```

---

## 7. Cron Jobs — Lập lịch tự động

```bash
# Sửa crontab
crontab -e

# Format:  phút giờ ngày tháng thứ command
# Mỗi 5 phút
*/5 * * * * /usr/bin/curl http://localhost:3000/api/health

# Mỗi ngày 2h sáng
0 2 * * * /home/devuser/scripts/backup.sh >> /var/log/backup.log 2>&1

# Mỗi Monday 9h sáng
0 9 * * 1 /home/devuser/scripts/weekly-report.sh

# Xem crontab
crontab -l
```

---

## Quick Reference

| Tình huống | Lệnh |
|---|---|
| Tìm file | `find / -name "*.log" -mtime -1` |
| Tìm text trong files | `grep -rn "ERROR" /var/log/` |
| Xem ai login | `who`, `last` |
| RAM usage | `free -h` |
| CPU info | `lscpu`, `nproc` |
| Xem environment | `env`, `printenv` |
| Download file | `curl -O url` hoặc `wget url` |

---

## Bài tập thực hành

- [ ] Setup user + SSH key login (disable password auth)
- [ ] Tạo systemd service cho Node.js app
- [ ] Setup UFW firewall rules
- [ ] Cron job: backup database mỗi đêm

---

## Tài nguyên thêm

- [Linux Journey](https://linuxjourney.com/) — Interactive tutorial
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials) — Server guides
- [TLDR Pages](https://tldr.sh/) — Simplified man pages
