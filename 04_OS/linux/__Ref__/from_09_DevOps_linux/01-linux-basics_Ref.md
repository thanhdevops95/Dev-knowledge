# 🐧 Linux cơ bản — Dòng lệnh cho developer

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — 96% server trên thế giới chạy Linux

---

## Tại sao developer cần biết Linux?

- **Server:** Hầu hết backend, DevOps, cloud đều chạy trên Linux
- **Docker/K8s:** Container dựa trên Linux kernel
- **WSL/macOS:** Terminal commands gần giống Linux
- **Hiệu quả:** CLI nhanh hơn GUI cho nhiều tác vụ dev

---

## 1. Điều hướng & File System

```bash
# Cấu trúc thư mục Linux
/               # Root — gốc của mọi thứ
├── /home       # Thư mục người dùng (/home/an)
├── /etc        # Cấu hình hệ thống (nginx.conf, hosts...)
├── /var        # Dữ liệu thay đổi (logs, database, mail)
├── /tmp        # File tạm (xóa khi reboot)
├── /usr        # User programs, libraries
├── /bin        # Binary (lệnh cơ bản: ls, cp, mv)
├── /sbin       # System binary (lệnh admin: fdisk, iptables)
├── /opt        # Optional software (cài thủ công)
├── /dev        # Devices (disk, terminal, USB...)
└── /proc       # Process info (virtual filesystem)

# Di chuyển
pwd                    # In thư mục hiện tại
ls                     # Liệt kê files
ls -la                 # Chi tiết + hidden files
ls -lh                 # Human-readable size (KB, MB, GB)

cd /var/log            # Đi đến đường dẫn tuyệt đối
cd ~                   # Về home directory
cd ..                  # Lên 1 cấp
cd -                   # Quay lại thư mục trước

# Tìm kiếm
find /var/log -name "*.log" -mtime -7    # File .log sửa trong 7 ngày
find . -type f -size +100M               # File > 100MB
which python3                             # Tìm đường dẫn của lệnh
```

---

## 2. Thao tác file & thư mục

```bash
# Tạo
mkdir -p project/src/components    # Tạo thư mục (kể cả parent)
touch index.js                     # Tạo file trống

# Copy
cp file.txt backup.txt             # Copy file
cp -r src/ src_backup/             # Copy thư mục (recursive)

# Di chuyển / Đổi tên
mv old.txt new.txt                 # Đổi tên
mv file.txt /tmp/                  # Di chuyển

# Xóa
rm file.txt                        # Xóa file
rm -r directory/                   # Xóa thư mục
rm -rf node_modules/               # Xóa không hỏi (⚠️ cẩn thận!)

# Liên kết
ln -s /path/to/original link_name  # Symbolic link (shortcut)
```

---

## 3. Đọc & xử lý file

```bash
# Đọc file
cat file.txt                       # In toàn bộ file
head -20 file.txt                  # 20 dòng đầu
tail -20 file.txt                  # 20 dòng cuối
tail -f /var/log/app.log           # Follow log real-time ⭐
less file.txt                      # Xem cuộn (q để thoát)

# Tìm kiếm trong file
grep "error" app.log               # Tìm dòng chứa "error"
grep -i "error" app.log            # Case insensitive
grep -r "TODO" src/                # Tìm trong thư mục (recursive)
grep -n "function" app.js          # Hiện số dòng
grep -c "error" app.log            # Đếm số lần xuất hiện

# Sắp xếp & đếm
sort file.txt                      # Sắp xếp
sort -u file.txt                   # Sắp xếp + loại trùng
wc -l file.txt                     # Đếm số dòng
wc -w file.txt                     # Đếm số từ

# Xử lý text
cut -d',' -f1,3 data.csv           # Cắt cột 1, 3 (delimiter comma)
sed 's/old/new/g' file.txt         # Thay thế text
awk '{print $1, $3}' file.txt      # In cột 1 và 3
```

---

## 4. Pipe & Redirect — Sức mạnh thực sự

```bash
# Pipe (|): Output command A → Input command B
cat access.log | grep "404" | wc -l
# Đọc log → lọc 404 → đếm = bao nhiêu lỗi 404?

cat access.log | grep "POST" | awk '{print $7}' | sort | uniq -c | sort -rn | head -10
# Top 10 URL POST nhiều nhất

# Redirect (> >>): Ghi output vào file
echo "Hello" > file.txt            # Ghi (overwrite)
echo "World" >> file.txt           # Ghi thêm (append)
ls nonexistent 2> error.log        # Redirect stderr
ls nonexistent 2>/dev/null         # Bỏ qua errors

# Ví dụ thực tế
# Tìm 10 file lớn nhất trong project
find . -type f -exec du -h {} + | sort -rh | head -10

# Đếm số dòng code (không tính blank lines)
find . -name "*.js" | xargs cat | grep -v "^$" | wc -l

# Monitor log real-time, chỉ hiện errors
tail -f /var/log/app.log | grep --color "ERROR"
```

---

## 5. Quyền truy cập (Permissions)

```bash
ls -la
# -rw-r--r-- 1 an staff 1234 Mar 3 10:00 file.txt
#  │├─┤├─┤├─┤
#  │ │  │  └── Others: r-- (read only)
#  │ │  └───── Group:  r-- (read only)
#  │ └──────── Owner:  rw- (read + write)
#  └─────────── File type: - (file), d (dir), l (link)

# Thay đổi quyền
chmod 755 script.sh          # Owner: rwx, Group: r-x, Others: r-x
chmod +x script.sh           # Thêm quyền execute
chmod 644 config.txt         # Owner: rw-, Group: r--, Others: r--

# Octal:
# 7 = rwx (4+2+1)
# 6 = rw- (4+2)
# 5 = r-x (4+1)
# 4 = r-- (4)
# 0 = --- (0)

# Thay đổi owner
chown an:staff file.txt      # Đổi owner và group
chown -R an:staff project/   # Recursive
```

---

## 6. Process Management

```bash
# Xem processes
ps aux                             # Tất cả processes
ps aux | grep node                 # Tìm process Node.js
top                                # Monitor real-time (interactive)
htop                               # Monitor đẹp hơn (cài thêm)

# Quản lý processes
kill 12345                         # Kill process (SIGTERM - dừng nhẹ nhàng)
kill -9 12345                      # Force kill (SIGKILL - dừng ngay)
killall node                       # Kill tất cả process "node"

# Background / Foreground
node server.js &                   # Chạy background
jobs                               # Liệt kê background jobs
fg %1                              # Đưa job 1 về foreground
nohup node server.js &             # Chạy background, không bị kill khi đóng terminal

# System info
free -h                            # RAM usage
df -h                              # Disk usage
du -sh *                           # Kích thước thư mục
uptime                             # Thời gian hoạt động
```

---

## 7. Networking

```bash
# Kiểm tra kết nối
ping google.com                    # Test connectivity
curl https://api.github.com        # HTTP request
curl -X POST -d '{"key":"value"}' -H "Content-Type: application/json" URL

wget https://example.com/file.zip  # Download file

# Ports & connections
netstat -tlnp                      # Ports đang listen
ss -tlnp                           # Modern netstat
lsof -i :3000                     # Process nào dùng port 3000?

# SSH
ssh user@server.com                # Kết nối remote
ssh -i key.pem user@server.com     # Kết nối bằng key
scp file.txt user@server:/tmp/     # Copy file đến server
rsync -avz ./src/ user@server:/app/  # Sync thư mục (hiệu quả hơn scp)
```

---

## 8. Package Management

```bash
# Ubuntu/Debian (apt)
sudo apt update                    # Cập nhật danh sách packages
sudo apt install nginx             # Cài package
sudo apt remove nginx              # Gỡ package
sudo apt upgrade                   # Upgrade tất cả

# CentOS/RHEL (yum/dnf)
sudo dnf install nginx
sudo dnf remove nginx

# Alpine (apk) — dùng trong Docker
apk add --no-cache nodejs npm
```

---

## 9. Systemd — Quản lý services

```bash
# Quản lý service
sudo systemctl start nginx         # Khởi động
sudo systemctl stop nginx          # Dừng
sudo systemctl restart nginx       # Restart
sudo systemctl status nginx        # Xem trạng thái
sudo systemctl enable nginx        # Auto-start khi boot
sudo systemctl disable nginx       # Tắt auto-start

# Xem logs
journalctl -u nginx                # Logs của nginx
journalctl -u nginx -f             # Follow logs
journalctl --since "1 hour ago"    # Logs trong 1 giờ qua
```

---

## 10. Shell Script cơ bản

```bash
#!/bin/bash
# deploy.sh — Script deploy đơn giản

set -euo pipefail  # Exit on error, undefined var, pipe failure

APP_DIR="/var/www/myapp"
BRANCH="${1:-main}"  # Tham số 1 hoặc default "main"

echo "🚀 Deploying branch: $BRANCH"

cd "$APP_DIR"
git pull origin "$BRANCH"
npm ci --production
npm run build

echo "♻️ Restarting app..."
sudo systemctl restart myapp

echo "✅ Deploy complete!"
```

```bash
chmod +x deploy.sh
./deploy.sh develop    # Deploy branch develop
./deploy.sh            # Deploy branch main (default)
```

---

## Các lỗi thường gặp

```
❌ Sai: rm -rf / (xóa MỌI THỨ!)
✅ Đúng: LUÔN double-check path trước khi rm -rf

❌ Sai: chmod 777 (everyone rwx) → bảo mật kém
✅ Đúng: chmod 755 cho scripts, 644 cho files

❌ Sai: Chạy mọi thứ bằng root/sudo
✅ Đúng: Tạo user riêng, chỉ sudo khi cần
```

---

## Bài tập thực hành

- [ ] Dùng pipe tìm 10 từ xuất hiện nhiều nhất trong 1 file text
- [ ] Viết script backup: tar.gz thư mục, thêm timestamp vào tên file
- [ ] SSH vào server (hoặc WSL) — cài Nginx, serve 1 trang HTML
- [ ] Monitor log file bằng `tail -f` + grep lọc errors

---

## Tài nguyên thêm

- [Linux Journey](https://linuxjourney.com/) — Tutorial tương tác
- [The Linux Command Line (book)](https://linuxcommand.org/tlcl.php) — Free book
- [ExplainShell](https://explainshell.com/) — Dán lệnh → giải thích từng phần
