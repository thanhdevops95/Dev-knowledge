---
module: "0"
title: "Setup Environment – Cheatsheet"
track: "0"
version: "1.0"
last_updated: "2025-12-27"
---

## MODULE 0 – Setup Environment Cheatsheet

### Quick Reference

- **WSL2:** Windows Subsystem for Linux - chạy Linux kernel ngay trên Windows.
- **Docker Desktop:** Ứng dụng quản lý Docker (Engine, Compose, Kubernetes) trên Windows/Mac.
- **VS Code:** Code Editor khuyên dùng với extension Remote - WSL/Docker.

---

### Common Commands

#### WSL (Windows Subsystem for Linux)

| Command | Description | Example |
|---------|-------------|---------|
| `wsl --install` | Cài đặt WSL mặc định (Ubuntu) | `wsl --install` |
| `wsl --list --online` | Xem danh sách distro có sẵn | `wsl -l -o` |
| `wsl --install -d <Distro>` | Cài đặt distro cụ thể | `wsl --install -d Debian` |
| `wsl --list --verbose` | Xem các distro đã cài và version | `wsl -l -v` |
| `wsl --shutdown` | Tắt hoàn toàn WSL VM | `wsl --shutdown` |
| `wsl` | Truy cập vào distro mặc định | `wsl` |

#### Docker Basic Check

| Command | Description | Example |
|---------|-------------|---------|
| `docker version` | Kiểm tra Client & Server info | `docker version` |
| `docker info` | Xem thông tin chi tiết hệ thống Docker | `docker info` |
| `docker run hello-world` | Test chạy container đầu tiên | `docker run hello-world` |
| `docker system prune` | Dọn dẹp data không dùng | `docker system prune` |

#### Git Configuration

| Command | Description | Example |
|---------|-------------|---------|
| `git config --global user.name` | Cài đặt tên hiển thị | `git config --global user.name "Huy Nguyen"` |
| `git config --global user.email` | Cài đặt email | `git config --global user.email "huy@email.com"` |
| `git config --list` | Xem toàn bộ config | `git config -l` |
| `ssh-keygen -t ed25519` | Tạo SSH Key cho GitHub/GitLab | `ssh-keygen -t ed25519 -C "email"` |

---

### Snippets / Config Samples

#### `.gitconfig` Aliases

```ini
[alias]
    st = status
    co = checkout
    ci = commit
    br = branch
    lg = log --oneline --graph --decorate
```

#### `.wslconfig` (Tối ưu RAM cho WSL2)

File: `%UserProfile%/.wslconfig` (Windows)

```ini
[wsl2]
memory=4GB   # Giới hạn RAM cho WSL2
processors=2 # Giới hạn số core CPU
swap=2GB     # Giới hạn swap file
```

---

### Common Errors & Fixes

| Error | Cause | Solution |
|-------|-------|----------|
| `WslRegisterDistribution failed with error: 0x800701bc` | Kernel WSL2 chưa update | Tải gói update kernel WSL2 từ Microsoft |
| `docker: error during connect...` | Docker Desktop chưa chạy | Mở Docker Desktop, chờ icon xanh lá |
| `git@github.com: Permission denied (publickey)` | Chưa thêm SSH key vào GitHub | Copy nội dung `.pub` key vào GitHub Settings |
| `Virtualization not enabled` | BIOS chưa bật ảo hóa | Vào BIOS enable Intel VT-x hoặc AMD-V |

---

### References

- [WSL Basic Commands](https://learn.microsoft.com/en-us/windows/wsl/basic-commands)
- [Docker CLI Cheat Sheet](https://docs.docker.com/get-started/docker_cheatsheet.pdf)
- [Git Cheat Sheet (GitHub)](https://education.github.com/git-cheat-sheet-education.pdf)

### Navigation Footer ⭐ BẮT BUỘC

---

[⬅️ README](./README.md) | [📚 Mục lục](../../README.md) | [LABS ➡️](./LABS.md)
