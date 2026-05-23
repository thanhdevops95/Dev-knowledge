# Module 01: Linux Scenarios

---

## 🎯 Mục đích

Đây là những **tình huống thực tế** bạn SẼ gặp khi làm DevOps. Mỗi scenario được thiết kế theo format:

1. **Bối cảnh** - Chuyện gì đang xảy ra?
2. **Triệu chứng** - Bạn thấy gì?
3. **Điều tra** - Làm sao tìm nguyên nhân?
4. **Giải quyết** - Fix như thế nào?
5. **Bài học** - Rút ra điều gì?

---

## 🚨 Scenario 1: "Disk Full" - Server hết dung lượng

### 📍 Bối cảnh

Đang yên đang lành, bạn nhận được alert:

```
🚨 ALERT: Disk usage > 90% on production-web-01
```

Bạn SSH vào server để điều tra.

### 👀 Triệu chứng

```bash
df -h
```

**Output:**

```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G   95G  5.0G  95% /
```

**95% dung lượng đã dùng!** Nếu đầy 100%, server sẽ không hoạt động.

### 🔍 Điều tra

**Câu hỏi:** Cái gì đang chiếm hết disk?

**Bước 1: Tìm thư mục lớn nhất**

```bash
# Kiểm tra từ root
sudo du -sh /* 2>/dev/null | sort -h | tail -10
```

**Output:**

```
1.2G    /usr
2.5G    /home
45G     /var
```

**Aha!** `/var` chiếm 45GB - đây là nơi chứa logs!

**Bước 2: Đi sâu vào /var**

```bash
sudo du -sh /var/* 2>/dev/null | sort -h | tail -5
```

**Output:**

```
500M    /var/cache
2.0G    /var/lib
42G     /var/log
```

**Logs chiếm 42GB!**

**Bước 3: Tìm file log nào lớn nhất**

```bash
sudo find /var/log -type f -size +100M -exec ls -lh {} \;
```

**Output:**

```
-rw-r--r-- 1 root root 35G Jan 15 11:00 /var/log/nginx/access.log
-rw-r--r-- 1 root root 5G Jan 15 11:00 /var/log/nginx/error.log
```

**35GB access log!** Có lẽ chưa được rotate.

### 💡 Giải quyết

**Giải pháp ngắn hạn: Xóa hoặc truncate log cũ**

```bash
# Option 1: Truncate (xóa nội dung, giữ file)
sudo truncate -s 0 /var/log/nginx/access.log

# Option 2: Nén logs cũ
sudo gzip /var/log/nginx/access.log.1
```

**Kiểm tra:**

```bash
df -h
```

**Output:**

```
/dev/sda1       100G   60G  40G  60% /
```

**Đã giảm từ 95% xuống 60%!**

**Giải pháp dài hạn: Setup log rotation**

```bash
sudo nano /etc/logrotate.d/nginx
```

```
/var/log/nginx/*.log {
    daily           # Rotate mỗi ngày
    rotate 7        # Giữ 7 files cũ
    compress        # Nén files cũ
    missingok       # Không báo lỗi nếu file không tồn tại
    notifempty      # Không rotate nếu file rỗng
    postrotate
        systemctl reload nginx
    endscript
}
```

### 📚 Bài học

1. **Luôn monitor disk usage** - Setup alert trước khi đầy
2. **Config log rotation** - Không để logs mọc vô hạn
3. **Biết cách điều tra** - `du` và `find` là bạn của bạn

---

## 🚨 Scenario 2: "Permission Denied" - Không chạy được script

### 📍 Bối cảnh

Bạn vừa viết xong deploy script, nhưng khi chạy:

```bash
./deploy.sh
```

### 👀 Triệu chứng

```
bash: ./deploy.sh: Permission denied
```

### 🔍 Điều tra

**Bước 1: Kiểm tra permissions**

```bash
ls -la deploy.sh
```

**Output:**

```
-rw-r--r-- 1 deploy deploy 1024 Jan 15 11:00 deploy.sh
```

**Vấn đề rõ ràng:** Không có `x` (execute) permission!

**Bước 2: Kiểm tra thêm (nếu đã có x)**

```bash
# Xem shebang (dòng đầu tiên)
head -1 deploy.sh
```

**Output có thể:**

```
#!/bin/bash
```

hoặc sai:

```
#! /bin/bash  (có space thừa)
# Thiếu shebang
```

### 💡 Giải quyết

**Trường hợp 1: Thiếu execute permission**

```bash
chmod +x deploy.sh
./deploy.sh
```

**Trường hợp 2: Shebang sai**

```bash
# Sửa dòng đầu tiên
sed -i '1s/.*/#!/bin/bash/' deploy.sh
```

**Trường hợp 3: File format sai (từ Windows)**

```bash
# Kiểm tra
file deploy.sh
```

**Output xấu:**

```
deploy.sh: Bash script, ASCII text executable, with CRLF line terminators
```

**Fix:**

```bash
# Chuyển từ Windows (CRLF) sang Linux (LF)
sed -i 's/\r$//' deploy.sh

# Hoặc dùng dos2unix
dos2unix deploy.sh
```

### 📚 Bài học

1. **Luôn `chmod +x` script mới**
2. **Dòng đầu phải là shebang:** `#!/bin/bash`
3. **Cẩn thận khi copy script từ Windows**

---

## 🚨 Scenario 3: "Can't SSH" - Không kết nối được server

### 📍 Bối cảnh

Bạn thử SSH vào server nhưng không được:

```bash
ssh deploy@192.168.1.100
```

### 👀 Triệu chứng

**Trường hợp 1: Connection timeout**

```
ssh: connect to host 192.168.1.100 port 22: Connection timed out
```

**Trường hợp 2: Connection refused**

```
ssh: connect to host 192.168.1.100 port 22: Connection refused
```

**Trường hợp 3: Permission denied**

```
deploy@192.168.1.100: Permission denied (publickey)
```

### 🔍 Điều tra & Giải quyết

**Trường hợp 1: Timeout - Vấn đề network**

```bash
# Kiểm tra có ping được không
ping 192.168.1.100

# Nếu không ping được:
# - Kiểm tra IP có đúng không
# - Kiểm tra firewall
# - Kiểm tra server có đang chạy không
```

**Trường hợp 2: Refused - SSH service không chạy**

```bash
# Nếu bạn có console access khác (VNC, cloud console):
sudo systemctl status sshd

# Nếu không chạy:
sudo systemctl start sshd
sudo systemctl enable sshd
```

**Trường hợp 3: Permission denied - Key hoặc user sai**

```bash
# Kiểm tra key đang dùng
ssh -v deploy@192.168.1.100

# Xem dòng:
# debug1: Offering public key: /home/user/.ssh/id_ed25519

# Đảm bảo public key đã có trên server
cat ~/.ssh/id_ed25519.pub
# So sánh với ~/.ssh/authorized_keys trên server

# Kiểm tra permissions trên server:
# ~/.ssh phải là 700
# ~/.ssh/authorized_keys phải là 600
```

### 💡 Quick Checklist

```
[ ] IP đúng?
[ ] Server đang chạy?
[ ] SSH service (sshd) đang chạy?
[ ] Firewall mở port 22?
[ ] SSH key đúng?
[ ] User tồn tại trên server?
[ ] Permissions ~/.ssh chính xác?
```

### 📚 Bài học

1. **Luôn có backup access** (console, VPN)
2. **Test SSH sau khi thay đổi config** trước khi logout
3. **Check từ đơn giản nhất:** ping → port → service → auth

---

## 🚨 Scenario 4: "Process eating CPU" - Một process chiếm hết CPU

### 📍 Bối cảnh

Server chậm đột ngột. Users phàn nàn website load lâu.

### 👀 Triệu chứng

```bash
# Load average cao bất thường
uptime
```

**Output:**

```
11:00:00 up 30 days,  1 user,  load average: 15.50, 12.30, 8.20
```

**Load 15.50 trên server 4 cores là QUÁ CAO!** (Bình thường < 4)

### 🔍 Điều tra

**Bước 1: Xem process nào đang chiếm CPU**

```bash
top -c
```

**Output:**

```
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
 5678 www-data  20   0  500000  50000   5000 R  99.0  2.5   45:30.00 php-fpm: pool www
 5679 www-data  20   0  500000  50000   5000 R  95.0  2.5   44:00.00 php-fpm: pool www
```

**2 process php-fpm chiếm gần 200% CPU!**

**Bước 2: Xem chi tiết process**

```bash
# Xem process đang làm gì
strace -p 5678
```

**Bước 3: Kiểm tra error logs**

```bash
sudo tail -100 /var/log/nginx/error.log
sudo tail -100 /var/log/php-fpm/error.log
```

### 💡 Giải quyết

**Giải pháp tức thì: Restart service**

```bash
# Nếu website không critical
sudo systemctl restart php-fpm
```

**Giải pháp có phân tích: Kill process cụ thể**

```bash
# Kill process có vấn đề
sudo kill 5678 5679

# PHP-FPM sẽ tự tạo worker mới
```

**Giải pháp dài hạn:**

```bash
# 1. Kiểm tra code có infinite loop không
# 2. Tăng timeout để kill slow requests
# 3. Limit resources per process
sudo nano /etc/php/8.0/fpm/pool.d/www.conf

# pm.max_execution_time = 30
# Requests chạy > 30s sẽ bị kill
```

### 📚 Bài học

1. **Monitor load average** - Đây là chỉ số sức khỏe server
2. **Biết dùng top/htop** để tìm process bermasalah
3. **Restart không phải lúc nào cũng xấu** - Đôi khi đó là cách nhanh nhất

---

## 🚨 Scenario 5: "Out of Memory" - Server hết RAM

### 📍 Bối cảnh

Bạn nhận alert:

```
🚨 ALERT: OOM Killer activated on production-app-01
```

OOM = Out Of Memory. Kernel đã phải kill process để giải phóng RAM.

### 👀 Triệu chứng

```bash
dmesg | grep -i "killed process"
```

**Output:**

```
[123456.789] Out of memory: Killed process 5678 (java) total-vm:8000000kB
```

**Java process bị kernel kill vì hết RAM!**

### 🔍 Điều tra

**Bước 1: Xem RAM hiện tại**

```bash
free -h
```

**Output:**

```
              total        used        free      shared  buff/cache   available
Mem:           7.8G        7.5G        100M        100M        200M        300M
Swap:          2.0G        2.0G          0B
```

**Cả RAM và Swap đều gần hết!**

**Bước 2: Ai đang dùng nhiều RAM nhất?**

```bash
ps aux --sort=-%mem | head -10
```

**Output:**

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
mysql     1000  5.0 45.0 5000000 3500000 ?    Sl   Jan14 100:00 /usr/sbin/mysqld
java      2000  3.0 40.0 8000000 3100000 ?    Sl   Jan14  50:00 java -jar app.jar
```

**MySQL và Java chiếm 85% RAM!**

### 💡 Giải quyết

**Giải pháp tức thì:**

```bash
# Clear cache (không mất data)
sync; echo 3 > /proc/sys/vm/drop_caches

# Restart service chiếm RAM
sudo systemctl restart mysql
```

**Giải pháp dài hạn:**

```bash
# Limit RAM cho MySQL
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
# innodb_buffer_pool_size = 1G  (thay vì auto)

# Limit RAM cho Java
# Sửa trong start script
java -Xmx2G -Xms1G -jar app.jar
```

### 📚 Bài học

1. **Luôn set memory limits** cho applications
2. **Monitor RAM usage** - Alert trước khi OOM
3. **Swap không phải giải pháp** - Chỉ là buffer tạm thời

---

## 🎓 Tổng kết Scenarios

### Bạn đã học cách xử lý

| Scenario | Vấn đề | Lệnh chính |
|----------|--------|------------|
| 1 | Disk full | `du`, `find -size`, `logrotate` |
| 2 | Permission denied | `chmod`, `file`, `dos2unix` |
| 3 | Can't SSH | `ping`, `ssh -v`, permissions |
| 4 | High CPU | `top`, `kill`, service restart |
| 5 | Out of memory | `free`, `ps --sort=-%mem`, limits |

### Mindset quan trọng

1. **Đừng hoảng** - Bình tĩnh điều tra từng bước
2. **Thu thập thông tin** trước khi hành động
3. **Ghi lại những gì đã làm** - Để postmortem
4. **Fix root cause** - Không chỉ fix symptom

---

## ⏭️ Bạn đã hoàn thành Module 01

Tiếp theo: **[Module 02: Networking](../02_NETWORKING/README.md)**
