# Module 01: Linux Fundamentals

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Linux** | /ˈlɪnəks/ | Hệ điều hành mã nguồn mở, 90% servers sử dụng |
| **Terminal** | - | Giao diện dòng lệnh để tương tác với hệ thống |
| **Shell** | - | Chương trình nhận và thực thi lệnh (Bash, Zsh) |
| **Bash** | /bæʃ/ | Bourne Again Shell - Shell mặc định trên Linux |
| **SSH** | - | Secure Shell - Kết nối an toàn đến server từ xa |
| **Root** | - | User có quyền cao nhất trong Linux |
| **sudo** | - | Super User Do - Chạy lệnh với quyền root |
| **Directory** | - | Thư mục - Nơi chứa files và thư mục con |
| **Path** | - | Đường dẫn đến file hoặc thư mục |
| **Permission** | - | Quyền truy cập (read, write, execute) |
| **Process** | - | Tiến trình - Chương trình đang chạy |
| **Service** | - | Dịch vụ chạy nền (nginx, mysql, docker) |
| **Package Manager** | - | Công cụ cài đặt phần mềm (apt, yum) |
| **Daemon** | - | Tiến trình chạy nền không có giao diện |

---

## 🎬 Câu chuyện mở đầu

Hãy tưởng tượng bạn được nhận vào công ty công nghệ đầu tiên. Ngày đầu đi làm, Senior DevOps đưa cho bạn một tờ giấy ghi:

```
Server Production: 192.168.1.100
User: deploy
Task: Kiểm tra tại sao website bị chậm
```

Bạn mở laptop, kết nối SSH vào server... và thấy một màn hình đen với dấu nhấp nháy. Không có nút click, không có icon, không có gì cả - chỉ có dòng lệnh.

**Đây là Linux.** Và đây là lý do bạn cần học nó.

---

## 📖 Linux là gì và tại sao bạn cần biết?

### Câu chuyện ngắn về Linux

Năm 1991, một sinh viên Phần Lan tên **Linus Torvalds** muốn có một hệ điều hành miễn phí để học tập. Anh ta viết ra Linux - ban đầu chỉ là dự án cá nhân.

30+ năm sau, Linux chạy trên:

- **90% servers trên internet** (bao gồm Google, Facebook, Netflix)
- **100% supercomputers** trên thế giới
- **Tất cả điện thoại Android** (Android chạy trên Linux kernel)
- **Hầu hết thiết bị IoT** (router, smart TV, tủ lạnh thông minh...)

### Tại sao DevOps PHẢI biết Linux?

Hãy hình dung thế này:

```
Bạn là DevOps Engineer
         ↓
Bạn quản lý servers
         ↓
90% servers là Linux
         ↓
Không biết Linux = Không làm được việc
```

**Cụ thể hơn:**

| Công việc DevOps | Cần Linux vì... |
|------------------|-----------------|
| Deploy ứng dụng | App chạy trên Linux server |
| Debug production | Phải đọc logs, check processes trên Linux |
| Viết Docker | Container là Linux simplified |
| Setup Kubernetes | K8s nodes là Linux servers |
| Automation | Shell scripting chạy trên Linux |

---

## 🏠 Ẩn dụ: Linux như ngôi nhà của bạn

Để dễ hiểu, hãy so sánh Linux với **ngôi nhà**:

```
Ngôi nhà của bạn              Linux Server
─────────────────            ──────────────
Địa chỉ nhà                  → IP address
Cửa chính (có khóa)          → SSH (login với password/key)
Các phòng                    → Thư mục (directories)
Đồ vật trong nhà             → Files
Người sống trong nhà         → Users
Điện, nước, gas              → Services (nginx, mysql, redis...)
```

Khi bạn "vào nhà" (SSH vào server), bạn cần biết:

1. **Đang ở phòng nào?** → `pwd` (print working directory)
2. **Phòng này có gì?** → `ls` (list)
3. **Đi sang phòng khác** → `cd` (change directory)

---

## 🗂️ Cấu trúc thư mục Linux - Bản đồ ngôi nhà

Khi vào Linux lần đầu, bạn sẽ thấy mình ở `/home/username`. Đây là "phòng riêng" của bạn.

Nhưng ngôi nhà Linux có nhiều phòng hơn. Đây là bản đồ:

```
/                          ← Sảnh chính (root - gốc của mọi thứ)
│
├── /home/                 ← Khu phòng ngủ (mỗi user một phòng)
│   ├── /home/alice/       ← Phòng của Alice
│   └── /home/bob/         ← Phòng của Bob
│
├── /etc/                  ← Tủ hồ sơ (config files - RẤT QUAN TRỌNG)
│   ├── nginx/             ← Config của nginx
│   ├── ssh/               ← Config SSH
│   └── hosts              ← Danh bạ DNS local
│
├── /var/                  ← Kho đồ thay đổi thường xuyên
│   ├── /var/log/          ← Nhật ký hoạt động (logs - XEM THƯỜNG XUYÊN)
│   └── /var/www/          ← Website files
│
├── /tmp/                  ← Phòng đồ tạm (tự dọn dẹp)
│
├── /opt/                  ← Gara để xe (software bên thứ 3)
│
└── /bin/, /usr/bin/       ← Hộp công cụ (các lệnh như ls, cp, mv...)
```

### 🎯 Bạn cần nhớ 4 thư mục quan trọng nhất

| Thư mục | Dùng khi nào | Ví dụ thực tế |
|---------|--------------|---------------|
| `/home/username` | Làm việc cá nhân | Viết scripts, để code |
| `/etc/` | Sửa config | Edit nginx.conf, hosts file |
| `/var/log/` | Debug lỗi | Xem nginx error log |
| `/tmp/` | Để file tạm | Download file test |

---

## 🧭 Điều hướng - Di chuyển trong ngôi nhà

### Bạn đang ở đâu?

Khi mới SSH vào server, câu hỏi đầu tiên: **"Mình đang ở đâu?"**

```bash
pwd
```

Output: `/home/deploy`

Giải thích: Bạn đang ở thư mục home của user `deploy`.

### Xung quanh có gì?

```bash
ls
```

Output: `documents  downloads  scripts`

Giải thích: Thư mục hiện tại có 3 thư mục con.

**Muốn xem chi tiết hơn?**

```bash
ls -la
```

Output:

```
drwxr-xr-x  5 deploy deploy 4096 Jan 15 10:00 .
drwxr-xr-x  3 root   root   4096 Jan 10 09:00 ..
-rw-r--r--  1 deploy deploy  220 Jan 10 09:00 .bashrc
drwxr-xr-x  2 deploy deploy 4096 Jan 15 10:00 documents
drwxr-xr-x  2 deploy deploy 4096 Jan 15 10:00 downloads
drwxr-xr-x  2 deploy deploy 4096 Jan 15 10:00 scripts
```

**Đọc hiểu output này:**

```
drwxr-xr-x  5 deploy deploy 4096 Jan 15 10:00 scripts
│└──┬───┘     └──┬─┘ └──┬─┘ └─┬┘ └─────┬─────┘ └──┬──┘
│   │           │      │     │        │          └─ Tên file/folder
│   │           │      │     │        └─ Ngày sửa cuối
│   │           │      │     └─ Kích thước (bytes)
│   │           │      └─ Group sở hữu
│   │           └─ User sở hữu
│   └─ Permissions (quyền truy cập)
└─ Loại: d=directory, -=file, l=link
```

### Di chuyển đến nơi khác

**Đi vào thư mục con:**

```bash
cd scripts
pwd
# /home/deploy/scripts
```

**Quay lại thư mục cha:**

```bash
cd ..
pwd
# /home/deploy
```

**Về thẳng nhà (home):**

```bash
cd ~
# hoặc đơn giản
cd
```

**Đi đến địa chỉ tuyệt đối:**

```bash
cd /var/log
pwd
# /var/log
```

**Quay lại nơi vừa đứng:**

```bash
cd -
# Quay lại /home/deploy
```

### 💡 Mẹo nhớ

| Lệnh | Ẩn dụ | Tác dụng |
|------|-------|----------|
| `pwd` | "Mình đang ở đâu?" | In ra đường dẫn hiện tại |
| `ls` | "Xung quanh có gì?" | Liệt kê files/folders |
| `cd X` | "Đi đến X" | Chuyển đến thư mục X |
| `cd ..` | "Lùi lại 1 bước" | Lên thư mục cha |
| `cd ~` | "Về nhà" | Về home directory |

---

## 📁 Thao tác với Files - Làm việc với đồ vật trong nhà

### Tạo file mới

**Câu chuyện:** Bạn cần tạo file config cho ứng dụng.

```bash
# Tạo file rỗng
touch config.txt

# Tạo file có nội dung
echo "database_host=localhost" > config.txt

# Xem nội dung
cat config.txt
# database_host=localhost
```

**Thêm nội dung vào file (không ghi đè):**

```bash
echo "database_port=5432" >> config.txt

cat config.txt
# database_host=localhost
# database_port=5432
```

⚠️ **Lưu ý quan trọng:**

- `>` = Ghi đè (XÓA hết nội dung cũ)
- `>>` = Thêm vào cuối (GIỮ nội dung cũ)

### Tạo thư mục

```bash
# Tạo một thư mục
mkdir projects

# Tạo thư mục lồng nhau (nested)
mkdir -p projects/webapp/src/components

# Xem kết quả
ls -R projects/
```

### Copy (sao chép)

```bash
# Copy file
cp config.txt config.backup.txt

# Copy file vào thư mục khác
cp config.txt projects/

# Copy cả thư mục (cần -r = recursive)
cp -r projects/ projects_backup/
```

### Move (di chuyển/đổi tên)

```bash
# Di chuyển file
mv config.txt projects/

# Đổi tên file
mv projects/config.txt projects/app.config

# Di chuyển và đổi tên cùng lúc
mv projects/app.config ./main.config
```

### Delete (xóa)

```bash
# Xóa file
rm main.config

# Xóa thư mục rỗng
rmdir empty_folder

# Xóa thư mục có nội dung
rm -r projects_backup/

# Xóa không hỏi (NGUY HIỂM!)
rm -rf old_projects/
```

⚠️ **CẢNH BÁO:** `rm -rf` là lệnh nguy hiểm nhất trong Linux!

- Không có Recycle Bin
- Xóa là xóa vĩnh viễn
- `rm -rf /` sẽ xóa TOÀN BỘ hệ thống

**Quy tắc an toàn:** Luôn `ls` trước khi `rm`

```bash
# Kiểm tra trước
ls old_projects/

# Chắc chắn rồi mới xóa
rm -rf old_projects/
```

---

## 👀 Đọc nội dung file - Mở đồ vật ra xem

### Các cách đọc file

**Câu chuyện:** Server báo lỗi. Bạn cần đọc log file để debug.

```bash
# Xem toàn bộ file (file nhỏ)
cat /var/log/app.log

# Xem file dài theo trang
less /var/log/app.log
# Điều khiển: Space=next page, b=back, q=quit, /text=search

# Xem 10 dòng đầu
head /var/log/app.log

# Xem 20 dòng đầu
head -n 20 /var/log/app.log

# Xem 10 dòng cuối
tail /var/log/app.log

# Xem 50 dòng cuối
tail -n 50 /var/log/app.log
```

### 🌟 Lệnh quan trọng nhất cho DevOps: `tail -f`

**Câu chuyện thực tế:**

Bạn vừa deploy code mới. Website dường như hoạt động, nhưng bạn muốn theo dõi real-time xem có lỗi gì không.

```bash
tail -f /var/log/nginx/error.log
```

Lệnh này sẽ:

1. Hiển thị 10 dòng cuối của file
2. **TỰ ĐỘNG** hiển thị dòng mới khi có log mới
3. Chạy liên tục cho đến khi bạn nhấn `Ctrl+C`

**Đây là cách DevOps theo dõi production!**

---

## 🔍 Tìm kiếm - Tìm đồ trong nhà

### Tìm file theo tên (find)

**Câu chuyện:** Ai đó để file config ở đâu đó, bạn cần tìm nó.

```bash
# Tìm file có tên chính xác
find /etc -name "nginx.conf"

# Tìm tất cả file .log
find /var/log -name "*.log"

# Tìm file lớn hơn 100MB
find /home -size +100M

# Tìm file được sửa trong 24h qua
find /var/log -mtime -1
```

### Tìm nội dung trong file (grep)

**Câu chuyện:** Có 10,000 dòng log. Bạn cần tìm những dòng có chứa "ERROR".

```bash
# Tìm dòng chứa "ERROR"
grep "ERROR" /var/log/app.log

# Không phân biệt hoa thường
grep -i "error" /var/log/app.log

# Đếm số lần xuất hiện
grep -c "ERROR" /var/log/app.log

# Hiển thị số dòng
grep -n "ERROR" /var/log/app.log

# Hiển thị 3 dòng trước và sau match
grep -C 3 "ERROR" /var/log/app.log
```

**Ví dụ thực tế - Phân tích access log:**

```bash
# Đếm số request 404 (Not Found)
grep -c "404" /var/log/nginx/access.log

# Xem chi tiết các request 404
grep "404" /var/log/nginx/access.log

# Tìm request từ IP cụ thể
grep "192.168.1.50" /var/log/nginx/access.log
```

---

## 🔐 Permissions - Ai được phép làm gì?

### Câu chuyện

Bạn viết script `deploy.sh` nhưng khi chạy, Linux báo:

```
bash: ./deploy.sh: Permission denied
```

Đây là lúc bạn cần hiểu về **permissions**.

### Hiểu permission string

```
-rwxr-xr--  1 deploy webteam 1024 Jan 15 10:00 deploy.sh
 └─┬┘└─┬┘└┬┘
   │   │  └── Others (người khác): r-- = chỉ đọc
   │   └── Group (nhóm webteam): r-x = đọc và chạy
   └── Owner (deploy): rwx = đọc, ghi, chạy
```

**Giải thích:**

- `r` (read) = Được đọc
- `w` (write) = Được sửa/xóa
- `x` (execute) = Được chạy
- `-` = Không có quyền

### Thay đổi permissions với chmod

**Cách 1: Symbolic (dễ nhớ)**

```bash
# Thêm quyền execute cho owner
chmod u+x deploy.sh

# Thêm quyền write cho group
chmod g+w deploy.sh

# Bỏ quyền read của others
chmod o-r deploy.sh

# Kết hợp nhiều thay đổi
chmod u+x,g+w,o-r deploy.sh
```

Giải thích:

- `u` = user (owner)
- `g` = group
- `o` = others
- `a` = all (cả 3)
- `+` = thêm quyền
- `-` = bỏ quyền

**Cách 2: Numeric (nhanh hơn)**

Mỗi quyền có giá trị số:

- `r` = 4
- `w` = 2
- `x` = 1

Cộng lại để có permission:

- `rwx` = 4+2+1 = **7**
- `rw-` = 4+2+0 = **6**
- `r-x` = 4+0+1 = **5**
- `r--` = 4+0+0 = **4**

```bash
# 755 = rwxr-xr-x (phổ biến cho scripts)
chmod 755 deploy.sh

# 644 = rw-r--r-- (phổ biến cho files)
chmod 644 config.txt

# 600 = rw------- (file nhạy cảm, chỉ owner xem)
chmod 600 secrets.txt
```

### 🎯 Permissions thường dùng

| Số | Permission | Dùng cho |
|----|------------|----------|
| 755 | rwxr-xr-x | Scripts, thư mục |
| 644 | rw-r--r-- | Files thông thường |
| 600 | rw------- | Files nhạy cảm (passwords, keys) |
| 700 | rwx------ | Thư mục riêng tư |

---

## ⚙️ Processes - Các hoạt động đang diễn ra

### Câu chuyện

Website chậm. Bạn cần xem server đang làm gì - có process nào đang "ăn" hết CPU/RAM không.

### Xem processes đang chạy

```bash
# Xem tất cả processes
ps aux

# Output:
# USER   PID %CPU %MEM    VSZ   RSS TTY  STAT START   TIME COMMAND
# root     1  0.0  0.1 225848  9424 ?    Ss   10:00   0:05 /sbin/init
# nginx  100  0.0  0.2 128400 10240 ?    S    10:00   0:10 nginx: worker process
```

Giải thích các cột quan trọng:

- **PID** = Process ID (số định danh)
- **%CPU** = Phần trăm CPU đang dùng
- **%MEM** = Phần trăm RAM đang dùng
- **COMMAND** = Lệnh đang chạy

```bash
# Tìm process cụ thể
ps aux | grep nginx

# Xem real-time (như Task Manager)
top

# Phiên bản đẹp hơn của top
htop
```

### Dừng/Kill process

**Câu chuyện:** Một process bị treo, chiếm 100% CPU.

```bash
# Dừng nhẹ nhàng (cho process cleanup)
kill 1234

# Dừng ngay lập tức (force kill)
kill -9 1234

# Kill theo tên
pkill nginx

# Kill tất cả process cùng tên
killall python3
```

---

## 🔧 Services - Các dịch vụ của ngôi nhà

### Câu chuyện

Sau khi sửa file config của nginx, bạn cần restart nginx để áp dụng thay đổi.

### Hiểu về Services

**Service** = Chương trình chạy nền, tự động khởi động cùng server.

Ví dụ services phổ biến:

- `nginx` - Web server
- `mysql` - Database
- `ssh` - Remote login
- `docker` - Container runtime

### Quản lý services với systemctl

```bash
# Xem trạng thái service
systemctl status nginx

# Output:
# ● nginx.service - A high performance web server
#    Loaded: loaded (/lib/systemd/system/nginx.service; enabled)
#    Active: active (running) since Mon 2024-01-15 10:00:00 UTC

# Khởi động service
sudo systemctl start nginx

# Dừng service
sudo systemctl stop nginx

# Restart (dừng rồi chạy lại)
sudo systemctl restart nginx

# Reload config (không downtime)
sudo systemctl reload nginx

# Bật tự động chạy khi server boot
sudo systemctl enable nginx

# Tắt tự động chạy
sudo systemctl disable nginx
```

### 🎯 Workflow thực tế khi sửa config

```bash
# 1. Edit config file
sudo nano /etc/nginx/nginx.conf

# 2. Kiểm tra syntax config
sudo nginx -t
# nginx: configuration file /etc/nginx/nginx.conf syntax is ok

# 3. Reload để áp dụng (không downtime)
sudo systemctl reload nginx

# 4. Kiểm tra status
systemctl status nginx
```

---

## 🔗 SSH - Kết nối từ xa

### Câu chuyện

Bạn làm việc ở văn phòng, nhưng server ở data center cách 100km. Làm sao để "vào" được server?

**SSH** (Secure Shell) là đường hầm bảo mật để bạn điều khiển server từ xa.

### Kết nối cơ bản

```bash
ssh username@server-ip-or-hostname

# Ví dụ
ssh deploy@192.168.1.100
ssh admin@myserver.example.com

# Dùng port khác (mặc định 22)
ssh -p 2222 deploy@192.168.1.100
```

### Kết nối bằng SSH Key (Bảo mật hơn password)

**Tại sao dùng SSH Key?**

- Password có thể bị brute-force
- Key có hàng tỷ tỷ tổ hợp, không thể đoán
- Không cần nhập password mỗi lần

**Bước 1: Tạo SSH key (trên máy của bạn)**

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"

# Nhấn Enter để dùng vị trí mặc định
# Nhập passphrase (optional nhưng khuyến khích)
```

**Bước 2: Copy public key lên server**

```bash
ssh-copy-id deploy@192.168.1.100

# Hoặc thủ công:
cat ~/.ssh/id_ed25519.pub | ssh deploy@192.168.1.100 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

**Bước 3: Kết nối không cần password**

```bash
ssh deploy@192.168.1.100
# Vào thẳng, không hỏi password!
```

### SSH Config - Tạo shortcuts

Thay vì nhớ IP và username, tạo file `~/.ssh/config`:

```bash
Host production
    HostName 192.168.1.100
    User deploy
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host staging
    HostName 192.168.1.101
    User deploy
```

Bây giờ chỉ cần:

```bash
ssh production
ssh staging
```

---

## 📊 Pipes và Kết hợp lệnh - Sức mạnh thực sự của Linux

### Câu chuyện

Trong Linux, bạn có thể **nối các lệnh đơn giản thành workflow phức tạp**. Đây là điều làm Linux mạnh mẽ hơn bất kỳ GUI nào.

### Pipe (|) - Nối output vào input

```bash
# Lấy danh sách processes → Lọc chỉ lấy nginx
ps aux | grep nginx

# Đếm số dòng chứa "ERROR" trong log
cat /var/log/app.log | grep "ERROR" | wc -l

# Tìm 10 files lớn nhất trong thư mục
du -sh * | sort -h | tail -10
```

**Cách đọc:** Lệnh A **|** Lệnh B = "Lấy kết quả của A, đưa vào B"

### Ví dụ thực tế: Phân tích access log

**Bài toán:** Tìm 10 IP truy cập nhiều nhất vào website.

```bash
cat /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10

# Giải thích từng bước:
# 1. cat ... → Đọc file log
# 2. awk '{print $1}' → Lấy cột đầu tiên (IP address)
# 3. sort → Sắp xếp để các IP giống nhau đứng cạnh nhau
# 4. uniq -c → Đếm số lần xuất hiện liên tiếp
# 5. sort -rn → Sắp xếp theo số, giảm dần
# 6. head -10 → Lấy 10 dòng đầu
```

---

## 📝 Tổng kết Module 01

### Bạn đã học được

✅ Linux là gì và tại sao DevOps cần biết  
✅ Cấu trúc thư mục Linux  
✅ Điều hướng với `pwd`, `ls`, `cd`  
✅ Thao tác files với `touch`, `mkdir`, `cp`, `mv`, `rm`  
✅ Đọc files với `cat`, `less`, `head`, `tail`, `tail -f`  
✅ Tìm kiếm với `find` và `grep`  
✅ Permissions và `chmod`  
✅ Processes và `ps`, `kill`  
✅ Services và `systemctl`  
✅ SSH và kết nối từ xa  
✅ Pipes và kết hợp lệnh  

### Tiếp theo

Đã hiểu lý thuyết? Hãy thực hành ngay!

👉 **[LABS.md - Bài thực hành Linux](LABS.md)**
