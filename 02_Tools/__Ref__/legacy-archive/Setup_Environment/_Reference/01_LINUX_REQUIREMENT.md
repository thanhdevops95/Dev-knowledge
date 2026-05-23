# Module 01: LINUX FUNDAMENTALS

> **"Linux là nền móng của mọi thứ trong DevOps"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Thành thạo điều hướng và thao tác file trong Linux CLI
- ✅ Hiểu sâu về file system structure và permissions
- ✅ Quản lý users, groups và quyền truy cập
- ✅ Giám sát và quản lý processes
- ✅ Sử dụng thành thạo package managers (apt, yum)
- ✅ Cấu hình và quản lý systemd services
- ✅ Làm việc với text processing tools (grep, sed, awk)
- ✅ Hiểu về logs và cách troubleshoot

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| CLI | Command Line Interface | Giao diện dòng lệnh |
| Shell | Shell | Môi trường thực thi lệnh (bash, zsh) |
| Root | Root User | User quản trị cao nhất (UID=0) |
| Sudo | Super User Do | Chạy lệnh với quyền root |
| Permissions | File Permissions | Quyền đọc/ghi/thực thi |
| Process | Process | Chương trình đang chạy |
| Daemon | Daemon | Process chạy nền (background) |
| PID | Process ID | Số định danh process |
| Package | Software Package | Gói phần mềm cài đặt |
| Service | System Service | Dịch vụ hệ thống |
| Symlink | Symbolic Link | Liên kết tượng trưng (shortcut) |
| Pipe | Pipe | Kết nối output → input giữa các lệnh |
| Stdin | Standard Input | Đầu vào chuẩn |
| Stdout | Standard Output | Đầu ra chuẩn |
| Stderr | Standard Error | Đầu ra lỗi |

---

## ✅ Checklist Labs

### Labs cơ bản

- [ ] Lab 1: Điều hướng file system (cd, ls, pwd, tree)
- [ ] Lab 2: Thao tác file và thư mục (mkdir, cp, mv, rm, touch)
- [ ] Lab 3: Xem nội dung file (cat, less, head, tail, wc)
- [ ] Lab 4: Tìm kiếm file (find, locate, which, whereis)
- [ ] Lab 5: Text searching với grep

### Labs trung cấp

- [ ] Lab 6: File permissions chi tiết (chmod, chown, chgrp)
- [ ] Lab 7: Special permissions (SUID, SGID, Sticky bit)
- [ ] Lab 8: User và Group management
- [ ] Lab 9: Process monitoring (ps, top, htop)
- [ ] Lab 10: Process control (kill, nice, nohup, &)
- [ ] Lab 11: Job control (jobs, fg, bg, Ctrl+Z)

### Labs nâng cao

- [ ] Lab 12: Package management - apt (Debian/Ubuntu)
- [ ] Lab 13: Package management - yum/dnf (RHEL/CentOS)
- [ ] Lab 14: Systemd services (systemctl)
- [ ] Lab 15: Journald logs (journalctl)
- [ ] Lab 16: Text processing với sed
- [ ] Lab 17: Text processing với awk
- [ ] Lab 18: Disk usage (df, du, ncdu)
- [ ] Lab 19: Archive và compression (tar, gzip, zip)
- [ ] Lab 20: Cron jobs và scheduling

---

## 🚨 Checklist Scenarios

### Scenarios về Files & Permissions

- [ ] Scenario 1: Permission denied khi đọc config file
- [ ] Scenario 2: Không thể execute script vừa viết
- [ ] Scenario 3: User không thể truy cập shared folder
- [ ] Scenario 4: Symlink bị broken
- [ ] Scenario 5: File bị xóa nhầm, cần recovery

### Scenarios về Disk & Storage

- [ ] Scenario 6: Disk full 100%, server không hoạt động
- [ ] Scenario 7: Tìm và xóa files lớn nhất
- [ ] Scenario 8: /var/log chiếm hết disk
- [ ] Scenario 9: Inode exhaustion (hết inode dù còn disk)

### Scenarios về Processes

- [ ] Scenario 10: Process zombie ăn CPU
- [ ] Scenario 11: Memory leak - process ăn hết RAM
- [ ] Scenario 12: Too many open files error
- [ ] Scenario 13: Lệnh SSH bị disconnect, process chết
- [ ] Scenario 14: Không kill được process

### Scenarios về Services

- [ ] Scenario 15: Service không start được sau reboot
- [ ] Scenario 16: Service start failed - cách đọc logs
- [ ] Scenario 17: Port already in use
- [ ] Scenario 18: Dependency service chưa ready

### Scenarios về Users & Security

- [ ] Scenario 19: User bị lock out
- [ ] Scenario 20: Sudo không hoạt động
- [ ] Scenario 21: SSH key authentication failed

---

## ⏱️ Thời lượng

**Ước tính:** 6-8 giờ

| Phần | Thời gian |
|------|-----------|
| Lý thuyết CLI cơ bản | 1 giờ |
| Labs 1-5: Cơ bản | 1.5 giờ |
| Labs 6-11: Trung cấp | 2 giờ |
| Labs 12-20: Nâng cao | 2 giờ |
| Scenarios | 1.5 giờ |

---

## 🔗 Tài liệu tham khảo

- [Linux Journey](https://linuxjourney.com/)
- [The Linux Command Line (Book)](https://linuxcommand.org/tlcl.php)
- [ExplainShell](https://explainshell.com/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
