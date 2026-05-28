# 💪 Exercises: Linux & Bash

> **Self-practice exercises to consolidate Linux and Bash scripting knowledge.**
>
> *Bài tập tự luyện để củng cố kiến thức Linux và Bash scripting.*

---

## 📋 Instructions (Hướng dẫn)

- Complete exercises **after finishing Labs**.
  *(Làm bài tập **sau khi hoàn thành Labs**.)*
- Try to solve them yourself before checking Solutions.
  *(Thử tự làm trước khi xem Solutions.)*
- Each exercise has a **difficulty level**: ⭐ Easy, ⭐⭐ Medium, ⭐⭐⭐ Hard.
  *(Mỗi bài có **mức độ khó**: ⭐ Dễ, ⭐⭐ Trung bình, ⭐⭐⭐ Khó.)*

---

## 🗂️ Exercise 1: File System Navigation (Điều hướng File System) ⭐

### Requirements (Yêu cầu)

Perform the following tasks and record the commands used:
*(Thực hiện các task sau và ghi lại commands đã dùng:)*

1. Create the following directory structure:
   *(Tạo cấu trúc thư mục sau:)*

```
~/devops-practice/
├── projects/
│   ├── web-app/
│   │   ├── src/
│   │   ├── tests/
│   │   └── docs/
│   └── api-server/
│       ├── src/
│       └── tests/
├── scripts/
└── logs/
```

1. Create a `README.md` file in each `src/` directory.
   *(Tạo file `README.md` trong mỗi thư mục `src/`.)*
2. Create 5 dummy log files in `logs/`: `app-01.log` to `app-05.log`.
   *(Tạo 5 files log giả trong `logs/`: `app-01.log` đến `app-05.log`.)*
3. Move all `.log` files to a new directory `logs/archive/`.
   *(Di chuyển tất cả files `.log` vào thư mục mới `logs/archive/`.)*
4. Delete the directory `api-server/tests/` (note: empty directory).
   *(Xóa thư mục `api-server/tests/` (chú ý: thư mục trống).)*

### Verification (Kiểm chứng)

```bash
# Check the structure (Kiểm tra cấu trúc)
tree ~/devops-practice/
```

---

## 🔐 Exercise 2: Permissions Management (Quản lý phân quyền) ⭐⭐

### Requirements (Yêu cầu)

1. Create file `secret.txt` with content "This is confidential".
   *(Tạo file `secret.txt` với nội dung "This is confidential".)*
2. Create file `public.txt` with content "This is public".
   *(Tạo file `public.txt` với nội dung "This is public".)*
3. Create script `deploy.sh` with content:
   *(Tạo script `deploy.sh` với nội dung:)*

   ```bash
   #!/bin/bash
   echo "Deploying application..."
   ```

4. Set permissions:
   *(Thiết lập permissions:)*
   - `secret.txt`: Owner read only (400). *(Chỉ owner đọc được.)*
   - `public.txt`: Everyone read, owner write (644). *(Ai cũng đọc được, chỉ owner sửa được.)*
   - `deploy.sh`: Owner full, group/others execute only (711). *(Owner full quyền, group và others chỉ execute.)*

5. Create group `devteam` and add current user to the group.
   *(Tạo group `devteam` và thêm user hiện tại vào group.)*
6. Change group owner of `deploy.sh` to `devteam`.
   *(Thay đổi group owner của `deploy.sh` thành `devteam`.)*

### Verification (Kiểm chứng)

```bash
ls -la secret.txt public.txt deploy.sh
```

---

## 🔍 Exercise 3: Text Processing (Xử lý văn bản) ⭐⭐

### Setup (Chuẩn bị)

Create file `server.log` with the following content:
*(Tạo file `server.log` với nội dung:)*

```bash
cat << 'EOF' > server.log
2024-01-15 08:00:01 INFO Server started
2024-01-15 08:05:23 INFO User login: admin
2024-01-15 08:10:45 WARNING High memory usage: 85%
2024-01-15 08:15:00 ERROR Database connection failed
2024-01-15 08:15:30 INFO Retrying database connection
2024-01-15 08:15:35 INFO Database connected
2024-01-15 08:20:00 INFO User login: john
2024-01-15 08:25:00 ERROR API timeout
2024-01-15 08:30:00 INFO User login: admin
2024-01-15 08:35:00 WARNING Disk space low: 90%
2024-01-15 08:40:00 INFO User logout: john
2024-01-15 08:45:00 ERROR Connection reset
2024-01-15 08:50:00 INFO Backup completed
EOF
```

### Tasks (Nhiệm vụ)

1. Count the number of ERROR lines in the file.
   *(Đếm số dòng ERROR trong file.)*
2. List all unique users who logged in.
   *(Liệt kê tất cả unique users đã login.)*
3. Display only the timestamp and message of WARNING lines.
   *(Hiển thị chỉ timestamp và message của các WARNING.)*
4. Find the last line containing "admin".
   *(Tìm dòng cuối cùng chứa "admin".)*
5. Replace all "INFO" with "[INFO]" and save to a new file.
   *(Thay thế tất cả "INFO" thành "[INFO]" và lưu vào file mới.)*
6. Display the first 5 lines.
   *(Hiển thị 5 dòng đầu tiên.)*
7. Count occurrences of "connection" (case-insensitive).
   *(Đếm số lần từ "connection" xuất hiện - không phân biệt hoa thường.)*

---

## 📊 Exercise 4: Process Management (Quản lý tiến trình) ⭐⭐

### Tasks (Nhiệm vụ)

1. List top 5 processes using the most CPU.
   *(Liệt kê top 5 processes sử dụng nhiều CPU nhất.)*
2. List top 5 processes using the most RAM.
   *(Liệt kê top 5 processes sử dụng nhiều RAM nhất.)*
3. Find all processes of the current user.
   *(Tìm tất cả processes của user hiện tại.)*
4. Run command `sleep 300` in the background.
   *(Chạy command `sleep 300` trong background.)*
5. Find the PID of the `sleep` process just started.
   *(Tìm PID của process `sleep` vừa chạy.)*
6. Send SIGTERM signal to that process.
   *(Gửi signal SIGTERM đến process đó.)*

### Bonus (Thử thách)

- Write a one-liner to kill all processes with names containing "sleep".
  *(Viết one-liner để kill tất cả processes có tên chứa "sleep".)*

---

## 🔧 Exercise 5: Bash Scripting Basics (Cơ bản về Bash Scripting) ⭐⭐

### Task 1: System Info Script (Script thông tin hệ thống)

Write script `sysinfo.sh` that displays:
*(Viết script `sysinfo.sh` hiển thị:)*

- Hostname
- OS version
- Kernel version
- CPU info (model name)
- Total RAM
- Disk usage of `/`
- Current date/time
- Uptime

### Task 2: User Input Script (Script nhận input)

Write script `greet.sh`:
*(Viết script `greet.sh`:)*

- Takes user name as input. *(Nhận input tên người dùng.)*
- Prints greeting based on time of day:
  *(In ra lời chào theo thời gian trong ngày:)*
  - 5:00 - 11:59 → "Good morning"
  - 12:00 - 17:59 → "Good afternoon"
  - 18:00 - 21:59 → "Good evening"
  - 22:00 - 4:59 → "Good night"

### Task 3: File Counter Script (Script đếm file)

Write script `counter.sh`:
*(Viết script `counter.sh`:)*

- Takes a directory path as argument. *(Nhận argument là đường dẫn thư mục.)*
- Counts and prints: *(Đếm và in ra:)*
  - Number of files *(Số files)*
  - Number of directories *(Số directories)*
  - Number of hidden files/dirs *(Số hidden files/dirs)*

---

## 🔄 Exercise 6: Loops and Conditions (Vòng lặp và Điều kiện) ⭐⭐⭐

### Task 1: Backup Script (Script sao lưu)

Write script `backup.sh`:
*(Viết script `backup.sh`:)*

- Takes 2 arguments: source_dir and backup_dir. *(Nhận 2 arguments: source_dir và backup_dir.)*
- Checks if source_dir exists. *(Kiểm tra source_dir tồn tại.)*
- Creates backup_dir if not exists. *(Tạo backup_dir nếu chưa có.)*
- Copies all files from source to backup. *(Copy tất cả files từ source sang backup.)*
- Adds timestamp to backup folder name. *(Thêm timestamp vào tên backup folder.)*
- Prints summary: number of files backed up. *(In summary: số files đã backup.)*

### Task 2: Log Rotator (Script quản lý log)

Write script `rotate.sh`:
*(Viết script `rotate.sh`:)*

- Takes a log directory as argument. *(Nhận argument là thư mục chứa logs.)*
- For each `.log` file: *(Với mỗi file `.log`:)*
  - If size > 1MB: compress to `.gz` and delete original. *(Nếu size > 1MB: nén thành `.gz` và xóa original.)*
  - If file is `.gz` and older than 7 days: delete. *(Nếu file đã là `.gz` và cũ hơn 7 ngày: xóa.)*
- Prints summary after completion. *(In summary sau khi hoàn thành.)*

### Task 3: Service Checker (Script kiểm tra dịch vụ)

Write script `check_services.sh`:
*(Viết script `check_services.sh`:)*

- Defines an array of services: nginx, docker, ssh. *(Định nghĩa array các services: nginx, docker, ssh.)*
- Loops through each service. *(Loop qua từng service.)*
- Checks status (running/stopped). *(Kiểm tra status (running/stopped).)*
- Prints a table with status of each service. *(In ra table với status của từng service.)*
- Exit code 1 if any service is stopped. *(Exit code 1 nếu có service nào stopped.)*

---

## 🌐 Exercise 7: Networking Commands (Lệnh mạng) ⭐⭐

### Tasks (Nhiệm vụ)

1. Display IP address of all interfaces. *(Hiển thị IP address của tất cả interfaces.)*
2. Check if port 80 is listening. *(Kiểm tra port 80 có đang listen không.)*
3. Check connectivity to google.com. *(Kiểm tra connectivity đến google.com.)*
4. Trace route to 8.8.8.8. *(Trace route đến 8.8.8.8.)*
5. Display all connections in ESTABLISHED state. *(Hiển thị tất cả connections đang ESTABLISHED.)*
6. Find which process is using port 22. *(Tìm process nào đang sử dụng port 22.)*

### Bonus (Thử thách)

Write a script to check connectivity to a list of hosts and report status.
*(Viết script kiểm tra connectivity đến list các hosts và report status.)*

---

## 📦 Exercise 8: Package Management (Quản lý gói) ⭐

### Tasks (Ubuntu/Debian)

1. Update package list. *(Update package list.)*
2. Search for package `nginx`. *(Tìm kiếm package `nginx`.)*
3. Display information about package `curl`. *(Hiển thị thông tin về package `curl`.)*
4. List all installed packages containing "python". *(Liệt kê tất cả packages đã cài đặt có chứa "python".)*
5. Check if `git` is installed. *(Kiểm tra xem `git` đã được cài chưa.)*

### Tasks (RHEL/CentOS)

1. Do the same with `yum` or `dnf`. *(Thực hiện tương tự với `yum` hoặc `dnf`.)*

---

## 🔐 Exercise 9: SSH & Remote Operations (SSH và Thao tác từ xa) ⭐⭐⭐

### Prerequisites (Điều kiện tiên quyết)

- Have access to a remote server (or use localhost).
  *(Có access đến một remote server (hoặc dùng localhost).)*

### Tasks (Nhiệm vụ)

1. Generate SSH key pair (ed25519). *(Generate SSH key pair (ed25519).)*
2. Copy public key to remote server. *(Copy public key đến remote server.)*
3. SSH to remote and run `uptime`. *(SSH đến remote và chạy `uptime`.)*
4. Copy file from local to remote. *(Copy file từ local sang remote.)*
5. Copy directory from remote to local. *(Copy thư mục từ remote về local.)*
6. Create SSH config entry for the remote server. *(Tạo SSH config entry cho remote server.)*

### Bonus (Thử thách)

Write a simple deploy script:
*(Viết script deploy đơn giản:)*

- SSH to server. *(SSH đến server.)*
- Pull new code from git. *(Pull code mới từ git.)*
- Restart service. *(Restart service.)*

---

## 🎯 Exercise 10: Comprehensive Challenge (Thử thách tổng hợp) ⭐⭐⭐

### Scenario (Tình huống)

You are a DevOps Engineer who needs to write an automation script for a new server.
*(Bạn là DevOps Engineer cần viết automation script cho server mới.)*

### Requirements (Yêu cầu)

Write script `server_setup.sh` that performs:
*(Viết script `server_setup.sh` thực hiện:)*

1. **System Update**
   - Update package list. *(Update package list.)*
   - Upgrade installed packages. *(Upgrade installed packages.)*

2. **User Setup**
   - Create user `deploy` if not exists. *(Tạo user `deploy` nếu chưa tồn tại.)*
   - Add user to group `sudo`. *(Thêm user vào group `sudo`.)*
   - Setup SSH key for user. *(Setup SSH key cho user.)*

3. **Security**
   - Install and enable `ufw`. *(Cài đặt và enable `ufw`.)*
   - Allow SSH (22), HTTP (80), HTTPS (443). *(Allow SSH (22), HTTP (80), HTTPS (443).)*
   - Deny all other incoming. *(Deny all other incoming.)*

4. **Software Installation**
   - Install: git, docker, nginx. *(Cài đặt: git, docker, nginx.)*
   - Enable and start docker, nginx. *(Enable và start docker, nginx.)*

5. **Directory Setup**
   - Create `/opt/apps` with owner `deploy`. *(Tạo `/opt/apps` với owner `deploy`.)*
   - Create `/var/log/apps` with proper permissions. *(Tạo `/var/log/apps` với proper permissions.)*

6. **Logging**
   - Log all actions to `/var/log/setup.log`. *(Log tất cả actions vào `/var/log/setup.log`.)*
   - Include timestamps. *(Include timestamps.)*

7. **Verification**
   - Check each step. *(Kiểm tra mỗi step.)*
   - Print summary at the end. *(Print summary ở cuối.)*

### Bonus Features (Tính năng bổ sung)

- Dry-run mode (--dry-run flag)
- Verbose mode (-v flag)
- Skip steps if already completed. *(Skip steps nếu đã hoàn thành.)*

---

## 📝 Submission Checklist (Danh sách kiểm tra)

After completing exercises:
*(Sau khi hoàn thành exercises:)*

- [ ] Exercise 1: File System Navigation
- [ ] Exercise 2: Permissions Management
- [ ] Exercise 3: Text Processing
- [ ] Exercise 4: Process Management
- [ ] Exercise 5: Bash Scripting Basics
- [ ] Exercise 6: Loops and Conditions
- [ ] Exercise 7: Networking Commands
- [ ] Exercise 8: Package Management
- [ ] Exercise 9: SSH & Remote Operations
- [ ] Exercise 10: Comprehensive Challenge

---

## 🔗 Resources (Tài nguyên)

- [SOLUTIONS.md](./SOLUTIONS.md) - View answers *(Xem đáp án)*
- [CHEATSHEET.md](./CHEATSHEET.md) - Command reference *(Tra cứu commands)*
- [LABS.md](./LABS.md) - Review labs *(Review bài thực hành)*

---

**[← Back to README](./README.md)** | **[View Solutions →](./SOLUTIONS.md)**
