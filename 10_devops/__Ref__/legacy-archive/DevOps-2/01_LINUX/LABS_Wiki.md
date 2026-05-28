# Module 01: Linux Labs

---

## 🎯 Mục tiêu của bài thực hành

Sau khi hoàn thành labs này, bạn sẽ **tự tin thao tác với Linux server** như một DevOps thực thụ. Không chỉ biết lệnh, mà còn hiểu KHI NÀO và TẠI SAO dùng.

---

## 🔧 Chuẩn bị môi trường

### Bạn cần một trong các options sau

**Option 1: WSL2 trên Windows (Khuyến nghị cho người mới)**

```powershell
# Mở PowerShell với quyền Admin, chạy:
wsl --install -d Ubuntu
# Restart máy, mở Ubuntu từ Start Menu
```

**Option 2: Docker (Nhanh nhất)**

```bash
docker run -it ubuntu:22.04 bash
```

**Option 3: Virtual Machine**

- Tải Ubuntu Server từ [ubuntu.com](https://ubuntu.com/download/server)
- Cài trên VirtualBox/VMware

**Option 4: Cloud (AWS/GCP Free Tier)**

- Tạo EC2 instance với Ubuntu

### Xác nhận môi trường đã sẵn sàng

```bash
# Bạn đang ở Linux terminal khi thấy prompt như:
user@hostname:~$

# Kiểm tra phiên bản Ubuntu
cat /etc/os-release
```

---

## 📚 Lab 1: Khám phá ngôi nhà Linux

### 🎬 Bối cảnh

Bạn vừa được cấp quyền SSH vào một server mới. Nhiệm vụ đầu tiên: **làm quen với môi trường**.

### Bước 1: Bạn đang ở đâu?

Khi mới vào server, điều đầu tiên cần biết là vị trí hiện tại.

```bash
pwd
```

**Bạn sẽ thấy:**

```
/home/youruser
```

**Giải thích:** Đây là "phòng riêng" của bạn - nơi an toàn để làm việc.

### Bước 2: Xung quanh có gì?

```bash
ls
```

**Nếu thư mục rỗng, bạn thấy:** (không có output gì)

**Thử với options chi tiết:**

```bash
ls -la
```

**Bạn sẽ thấy:**

```
total 28
drwxr-xr-x 4 youruser youruser 4096 Jan 15 10:00 .
drwxr-xr-x 3 root     root     4096 Jan 10 09:00 ..
-rw-r--r-- 1 youruser youruser  220 Jan 10 09:00 .bashrc
-rw-r--r-- 1 youruser youruser  807 Jan 10 09:00 .profile
```

**Giải thích các files ẩn (bắt đầu bằng `.`):**

- `.bashrc` = Config của terminal (alias, colors...)
- `.profile` = Script chạy khi login

### Bước 3: Khám phá ngôi nhà Linux

**Đi đến thư mục gốc:**

```bash
cd /
ls
```

**Bạn sẽ thấy:**

```
bin   dev  home  lib64  mnt  proc  run   srv  tmp  var
boot  etc  lib   media  opt  root  sbin  sys  usr
```

**Vào xem thư mục config:**

```bash
cd /etc
ls | head -20
```

**Bạn sẽ thấy nhiều file config:**

```
adduser.conf
apt
bash.bashrc
cron.d
environment
group
hostname
hosts
...
```

**Xem nội dung file hosts (danh bạ DNS local):**

```bash
cat /etc/hosts
```

**Output:**

```
127.0.0.1   localhost
127.0.1.1   yourserver

# IPv6
::1         localhost ip6-localhost ip6-loopback
```

### Bước 4: Quay về nhà

```bash
# Về home bằng ~ hoặc cd không tham số
cd ~
pwd
# /home/youruser
```

### ✅ Checkpoint Lab 1

Bạn đã biết:

- [ ] Xác định vị trí với `pwd`
- [ ] Liệt kê files (kể cả ẩn) với `ls -la`
- [ ] Di chuyển qua lại với `cd`
- [ ] Khám phá cấu trúc / và /etc

---

## 📁 Lab 2: Xây dựng workspace

### 🎬 Bối cảnh

Bắt đầu làm việc, bạn cần tạo một cấu trúc thư mục có tổ chức để quản lý scripts, logs, và configs.

### Bước 1: Tạo cấu trúc dự án

**Mục tiêu:** Tạo cấu trúc như sau:

```
devops-workspace/
├── scripts/
├── logs/
├── configs/
└── backups/
```

**Thực hiện:**

```bash
# Đảm bảo đang ở home
cd ~

# Tạo toàn bộ cấu trúc bằng 1 lệnh
mkdir -p devops-workspace/{scripts,logs,configs,backups}
```

**`-p` làm gì?** Tạo cả thư mục cha nếu chưa tồn tại, và không báo lỗi nếu đã có.

**Kiểm tra:**

```bash
ls -la devops-workspace/
```

**Output:**

```
total 24
drwxr-xr-x 6 user user 4096 Jan 15 10:00 .
drwxr-xr-x 5 user user 4096 Jan 15 10:00 ..
drwxr-xr-x 2 user user 4096 Jan 15 10:00 backups
drwxr-xr-x 2 user user 4096 Jan 15 10:00 configs
drwxr-xr-x 2 user user 4096 Jan 15 10:00 logs
drwxr-xr-x 2 user user 4096 Jan 15 10:00 scripts
```

### Bước 2: Tạo file script đầu tiên

```bash
# Vào thư mục scripts
cd ~/devops-workspace/scripts

# Tạo script đơn giản
cat > hello.sh << 'EOF'
#!/bin/bash
echo "Hello from DevOps workspace!"
echo "Current time: $(date)"
echo "Current user: $(whoami)"
echo "Current directory: $(pwd)"
EOF
```

**Giải thích `cat > file << 'EOF'`:**

- Tạo file và ghi nội dung cho đến khi gặp từ `EOF`
- Cách viết multi-line content thuận tiện

**Xem file vừa tạo:**

```bash
cat hello.sh
```

### Bước 3: Chạy script - Gặp lỗi đầu tiên

```bash
./hello.sh
```

**Bạn sẽ gặp LỖI:**

```
bash: ./hello.sh: Permission denied
```

**Tại sao?** File mới tạo không có quyền execute.

**Kiểm tra permissions:**

```bash
ls -la hello.sh
```

**Output:**

```
-rw-r--r-- 1 user user 140 Jan 15 10:00 hello.sh
```

Thấy không? `rw-r--r--` nghĩa là không ai được **execute** (chạy) file này.

### Bước 4: Cấp quyền execute

```bash
# Thêm quyền execute cho owner
chmod u+x hello.sh

# Kiểm tra lại
ls -la hello.sh
```

**Output mới:**

```
-rwxr--r-- 1 user user 140 Jan 15 10:00 hello.sh
```

Giờ owner có `rwx` = đọc, ghi, và **chạy**.

### Bước 5: Chạy lại script

```bash
./hello.sh
```

**Output thành công:**

```
Hello from DevOps workspace!
Current time: Mon Jan 15 10:05:00 UTC 2024
Current user: youruser
Current directory: /home/youruser/devops-workspace/scripts
```

🎉 **Script đầu tiên hoạt động!**

### ✅ Checkpoint Lab 2

Bạn đã biết:

- [ ] Tạo cấu trúc thư mục với `mkdir -p`
- [ ] Viết file nhiều dòng với `cat << EOF`
- [ ] Hiểu tại sao "Permission denied" xảy ra
- [ ] Cấp quyền execute với `chmod u+x`

---

## 📝 Lab 3: Làm việc với Files

### 🎬 Bối cảnh

Bạn cần tạo file config, backup, và thực hành các thao tác copy/move/delete an toàn.

### Bước 1: Tạo file config mẫu

```bash
cd ~/devops-workspace/configs

# Tạo app.config
cat > app.config << 'EOF'
# Application Configuration
APP_NAME=MyWebApp
APP_PORT=8080
APP_ENV=development

# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp_db

# Logging
LOG_LEVEL=debug
LOG_FILE=/var/log/myapp/app.log
EOF
```

**Xem nội dung:**

```bash
cat app.config
```

### Bước 2: Backup file config

**Quy tắc vàng:** Luôn backup trước khi sửa config!

```bash
# Copy làm backup
cp app.config app.config.backup

# Kiểm tra
ls -la
```

**Output:**

```
-rw-r--r-- 1 user user 312 Jan 15 10:10 app.config
-rw-r--r-- 1 user user 312 Jan 15 10:10 app.config.backup
```

### Bước 3: Sửa file config

**Sửa đổi LOG_LEVEL từ debug sang info:**

```bash
# Dùng sed để replace
sed -i 's/LOG_LEVEL=debug/LOG_LEVEL=info/' app.config

# Kiểm tra
grep "LOG_LEVEL" app.config
```

**Output:**

```
LOG_LEVEL=info
```

**So sánh với backup:**

```bash
diff app.config app.config.backup
```

**Output:**

```
10c10
< LOG_LEVEL=info
---
> LOG_LEVEL=debug
```

### Bước 4: Di chuyển backup vào thư mục backups

```bash
# Di chuyển và đổi tên thêm timestamp
mv app.config.backup ../backups/app.config.$(date +%Y%m%d_%H%M%S)

# Kiểm tra
ls ../backups/
```

**Output:**

```
app.config.20240115_101500
```

### Bước 5: Thực hành xóa an toàn

**Tạo files test để xóa:**

```bash
cd ~/devops-workspace
touch test1.txt test2.txt test3.txt

# LUÔN kiểm tra trước khi xóa
ls test*.txt
```

**Output:**

```
test1.txt  test2.txt  test3.txt
```

**Xóa:**

```bash
rm test1.txt test2.txt test3.txt

# Hoặc dùng pattern (CẨN THẬN!)
# rm test*.txt
```

**⚠️ Quy tắc an toàn khi dùng `rm`:**

1. **LUÔN** `ls` pattern trước: `ls test*.txt`
2. **SAU ĐÓ** mới `rm`: `rm test*.txt`
3. **KHÔNG BAO GIỜ** chạy `rm -rf /` hoặc `rm -rf *` khi đang ở thư mục quan trọng

### ✅ Checkpoint Lab 3

Bạn đã biết:

- [ ] Tạo file config với `cat > file << EOF`
- [ ] Backup file trước khi sửa
- [ ] Sửa file với `sed`
- [ ] So sánh files với `diff`
- [ ] Xóa file an toàn (ls trước, rm sau)

---

## 🔍 Lab 4: Debug với Logs

### 🎬 Bối cảnh

Server production có vấn đề. Bạn cần phân tích logs để tìm nguyên nhân.

### Bước 1: Tạo sample log file

```bash
cd ~/devops-workspace/logs

# Tạo log file mô phỏng
cat > app.log << 'EOF'
2024-01-15 10:00:00 INFO  Application starting...
2024-01-15 10:00:01 INFO  Loading configuration from /etc/app/config.yml
2024-01-15 10:00:02 INFO  Connecting to database at localhost:5432
2024-01-15 10:00:03 INFO  Database connection established
2024-01-15 10:00:04 INFO  Server listening on port 8080
2024-01-15 10:00:10 INFO  Received request: GET /api/users
2024-01-15 10:00:10 INFO  Request completed in 45ms
2024-01-15 10:00:15 WARN  High memory usage detected: 85%
2024-01-15 10:00:20 INFO  Received request: POST /api/orders
2024-01-15 10:00:21 ERROR Failed to process order: Database timeout
2024-01-15 10:00:21 ERROR Stack trace: Connection refused at db.connect()
2024-01-15 10:00:25 WARN  Retrying database connection...
2024-01-15 10:00:30 INFO  Database reconnected successfully
2024-01-15 10:00:35 INFO  Received request: GET /api/products
2024-01-15 10:00:35 INFO  Request completed in 120ms
2024-01-15 10:00:40 ERROR Failed to load product images: Disk full
2024-01-15 10:00:45 CRITICAL System running out of disk space!
2024-01-15 10:00:50 INFO  Received request: GET /health
2024-01-15 10:00:50 INFO  Health check passed
EOF
```

### Bước 2: Xem tổng quan log

```bash
# Đếm tổng số dòng
wc -l app.log
```

**Output:** `19 app.log`

```bash
# Xem 5 dòng đầu
head -5 app.log
```

```bash
# Xem 5 dòng cuối (thường là log mới nhất)
tail -5 app.log
```

### Bước 3: Tìm các dòng ERROR

**Câu hỏi:** Có bao nhiêu errors và chúng là gì?

```bash
# Tìm tất cả dòng ERROR
grep "ERROR" app.log
```

**Output:**

```
2024-01-15 10:00:21 ERROR Failed to process order: Database timeout
2024-01-15 10:00:21 ERROR Stack trace: Connection refused at db.connect()
2024-01-15 10:00:40 ERROR Failed to load product images: Disk full
```

```bash
# Đếm số lượng
grep -c "ERROR" app.log
```

**Output:** `3`

### Bước 4: Xem context xung quanh error

**Để hiểu error, cần xem trước và sau nó:**

```bash
# Hiển thị 2 dòng TRƯỚC và SAU mỗi ERROR
grep -C 2 "ERROR" app.log
```

**Output:**

```
2024-01-15 10:00:20 INFO  Received request: POST /api/orders
2024-01-15 10:00:21 ERROR Failed to process order: Database timeout
2024-01-15 10:00:21 ERROR Stack trace: Connection refused at db.connect()
2024-01-15 10:00:25 WARN  Retrying database connection...
--
2024-01-15 10:00:35 INFO  Request completed in 120ms
2024-01-15 10:00:40 ERROR Failed to load product images: Disk full
2024-01-15 10:00:45 CRITICAL System running out of disk space!
```

**Phân tích:**

1. Error đầu tiên: Database timeout → retry thành công
2. Error thứ 2: Disk full → dẫn đến CRITICAL

### Bước 5: Tìm tất cả warnings và errors

```bash
# Dùng regex OR
grep -E "WARN|ERROR|CRITICAL" app.log
```

**Output:**

```
2024-01-15 10:00:15 WARN  High memory usage detected: 85%
2024-01-15 10:00:21 ERROR Failed to process order: Database timeout
2024-01-15 10:00:21 ERROR Stack trace: Connection refused at db.connect()
2024-01-15 10:00:25 WARN  Retrying database connection...
2024-01-15 10:00:40 ERROR Failed to load product images: Disk full
2024-01-15 10:00:45 CRITICAL System running out of disk space!
```

### Bước 6: Mô phỏng tail -f (theo dõi real-time)

**Mở terminal thứ 2 và chạy:**

```bash
tail -f ~/devops-workspace/logs/app.log
```

**Quay lại terminal 1, thêm log mới:**

```bash
echo "2024-01-15 10:01:00 INFO  New request received" >> ~/devops-workspace/logs/app.log
```

**Quan sát terminal 2:** Dòng mới tự động hiển thị!

**Đây là cách DevOps theo dõi production logs real-time.**

### ✅ Checkpoint Lab 4

Bạn đã biết:

- [ ] Xem đầu/cuối file với `head`/`tail`
- [ ] Tìm text với `grep`
- [ ] Xem context với `grep -C`
- [ ] Kết hợp patterns với `grep -E "A|B"`
- [ ] Theo dõi real-time với `tail -f`

---

## ⚙️ Lab 5: Quản lý Processes

### 🎬 Bối cảnh

Server chậm. Bạn cần xác định process nào đang chiếm resources.

### Bước 1: Xem tất cả processes

```bash
ps aux
```

**Output (rút gọn):**

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.1 225848  9424 ?        Ss   10:00   0:05 /sbin/init
root       100  0.0  0.0  10784  3200 ?        Ss   10:00   0:00 /usr/sbin/sshd
youruser  1234  0.0  0.1  10000  5000 pts/0    Ss   10:05   0:00 -bash
```

### Bước 2: Tìm process cụ thể

```bash
# Tìm tất cả process của bash
ps aux | grep bash
```

**Output:**

```
youruser  1234  0.0  0.1  10000  5000 pts/0    Ss   10:05   0:00 -bash
youruser  5678  0.0  0.0   8168   736 pts/0    S+   10:10   0:00 grep --color=auto bash
```

**Lưu ý:** Dòng cuối là chính lệnh `grep` bạn vừa chạy. Để loại trừ:

```bash
ps aux | grep bash | grep -v grep
```

### Bước 3: Tạo process "nặng" để test

```bash
# Chạy một lệnh chiếm CPU ở background
yes > /dev/null &
```

**`&` làm gì?** Chạy lệnh ở background, trả terminal lại cho bạn.

**Kiểm tra:**

```bash
ps aux | grep yes
```

**Output:**

```
youruser  2345 99.0  0.0   7200   568 pts/0    R    10:15   0:05 yes
```

**Thấy chưa?** Process `yes` đang chiếm **99% CPU**!

### Bước 4: Xem real-time với top

```bash
top
```

**Trong top, bạn sẽ thấy process `yes` ở trên cùng vì nó ngốn CPU nhiều nhất.**

**Các phím trong top:**

- `q` = Thoát
- `k` = Kill process
- `M` = Sắp xếp theo Memory
- `P` = Sắp xếp theo CPU
- `1` = Hiển thị từng CPU core

**Thoát top:** Nhấn `q`

### Bước 5: Kill process

```bash
# Tìm PID của process yes
ps aux | grep yes | grep -v grep
# Giả sử PID là 2345

# Kill nhẹ nhàng
kill 2345

# Kiểm tra
ps aux | grep yes
# Process đã biến mất!
```

**Nếu process không chịu dừng, force kill:**

```bash
kill -9 2345
```

### Bước 6: Chạy process background với nohup

**Vấn đề:** Khi bạn logout, processes bạn khởi động sẽ bị kill.

**Giải pháp:** Dùng `nohup`

```bash
# Tạo script chạy lâu
cat > ~/devops-workspace/scripts/long_task.sh << 'EOF'
#!/bin/bash
while true; do
    echo "$(date): Still running..." >> ~/devops-workspace/logs/long_task.log
    sleep 60
done
EOF

chmod +x ~/devops-workspace/scripts/long_task.sh

# Chạy với nohup
nohup ~/devops-workspace/scripts/long_task.sh &

# Kiểm tra
ps aux | grep long_task
```

**Giờ cho dù bạn logout, script vẫn chạy!**

**Để dừng:**

```bash
pkill -f long_task.sh
```

### ✅ Checkpoint Lab 5

Bạn đã biết:

- [ ] Xem processes với `ps aux`
- [ ] Tìm process với `grep`
- [ ] Theo dõi real-time với `top`
- [ ] Kill process với `kill` và `kill -9`
- [ ] Chạy background với `&` và `nohup`

---

## 🔐 Lab 6: Permissions thực tế

### 🎬 Bối cảnh

Bạn tạo file chứa database password. Cần đảm bảo CHỈ bạn mới đọc được.

### Bước 1: Tạo file nhạy cảm

```bash
cd ~/devops-workspace/configs

cat > database.secrets << 'EOF'
DB_PASSWORD=super_secret_password_123!
API_KEY=sk_live_abcdef123456
EOF
```

### Bước 2: Kiểm tra permissions hiện tại

```bash
ls -la database.secrets
```

**Output:**

```
-rw-r--r-- 1 youruser youruser 82 Jan 15 10:30 database.secrets
```

**Vấn đề:** `r--` cho Others nghĩa là **BẤT KỲ AI** trên server đều đọc được file này!

### Bước 3: Bảo vệ file

```bash
# Chỉ cho phép owner đọc/ghi
chmod 600 database.secrets

ls -la database.secrets
```

**Output:**

```
-rw------- 1 youruser youruser 82 Jan 15 10:30 database.secrets
```

**Giờ chỉ owner mới truy cập được!**

### Bước 4: Test permissions

```bash
# Đọc OK
cat database.secrets

# Thử với user khác (nếu có)
# sudo -u otheruser cat database.secrets
# Sẽ báo Permission denied
```

### Bước 5: Permissions cho scripts

```bash
cd ~/devops-workspace/scripts

# Tạo deploy script
cat > deploy.sh << 'EOF'
#!/bin/bash
echo "Starting deployment..."
echo "Pulling latest code..."
echo "Restarting services..."
echo "Deployment complete!"
EOF

# Xem permissions mặc định
ls -la deploy.sh
```

**Output:**

```
-rw-r--r-- 1 youruser youruser 125 Jan 15 10:35 deploy.sh
```

**Không có `x`, không chạy được!**

```bash
# Cấp quyền execute (755 = owner rwx, others rx)
chmod 755 deploy.sh

# Chạy
./deploy.sh
```

### ✅ Checkpoint Lab 6

Bạn đã biết:

- [ ] Đọc hiểu permission string
- [ ] Bảo vệ file nhạy cảm với `chmod 600`
- [ ] Cấp quyền execute với `chmod 755`

---

## 🧹 Lab 7: Dọn dẹp workspace

### 🎬 Bối cảnh

Sau một thời gian làm việc, bạn cần dọn dẹp: xóa files test, lưu trữ logs cũ.

### Bước 1: Tìm files lớn

```bash
cd ~/devops-workspace

# Tạo file test lớn
dd if=/dev/zero of=logs/bigfile.log bs=1M count=50

# Tìm files > 10MB
find . -size +10M -exec ls -lh {} \;
```

**Output:**

```
-rw-r--r-- 1 user user 50M Jan 15 11:00 ./logs/bigfile.log
```

### Bước 2: Nén logs cũ

```bash
cd logs

# Nén file
gzip bigfile.log

# Xem kết quả
ls -lh bigfile.log.gz
```

**Output:** Size giảm đáng kể vì file zeros nén rất tốt.

### Bước 3: Tạo archive

```bash
cd ~/devops-workspace

# Tạo tar archive của toàn bộ workspace
tar -czvf workspace_backup.tar.gz scripts/ configs/ logs/

# c = create
# z = gzip compress
# v = verbose (hiện tiến trình)
# f = filename

ls -lh workspace_backup.tar.gz
```

### Bước 4: Xóa các files test

```bash
# Xóa file nén đã backup
rm logs/bigfile.log.gz

# Dọn dẹp files tạm (nếu có)
find . -name "*.tmp" -delete
find . -name "*~" -delete
```

### ✅ Checkpoint Lab 7

Bạn đã biết:

- [ ] Tìm files lớn với `find -size`
- [ ] Nén files với `gzip`
- [ ] Tạo archive với `tar`
- [ ] Dọn dẹp files theo pattern

---

## 🎓 Tổng kết Labs

### Bạn đã thực hành thành công

| Lab | Kỹ năng | Commands chính |
|-----|---------|----------------|
| 1 | Điều hướng | `pwd`, `ls`, `cd` |
| 2 | Tạo workspace | `mkdir -p`, `chmod`, scripts |
| 3 | Thao tác files | `cp`, `mv`, `rm`, `sed` |
| 4 | Phân tích logs | `grep`, `tail -f` |
| 5 | Quản lý processes | `ps`, `kill`, `nohup` |
| 6 | Permissions | `chmod 600`, `chmod 755` |
| 7 | Dọn dẹp | `find`, `gzip`, `tar` |

### Tiếp theo

Đã thực hành xong? Hãy thử sức với các tình huống thực tế!

👉 **[SCENARIOS.md - Tình huống thực chiến](SCENARIOS.md)**
