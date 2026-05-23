---
module: "0"
title: "Setup Environment – Labs"
track: "0"
version: "1.0"
last_updated: "2025-12-27"
---

## MODULE 0 – Setup Environment Labs

### 1. Objective (Mục tiêu)

Trong bài lab này, bạn sẽ:

- Cài đặt và cấu hình hoàn chỉnh WSL2 trên Windows (hoặc môi trường Terminal trên Mac/Linux).
- Cài đặt Docker Desktop và verify cài đặt.
- Cấu hình Git và kết nối SSH tới GitHub.
- Setup VS Code để làm việc với WSL/Docker.

### 2. Prerequisites (Chuẩn bị)

- Máy tính kết nối Internet ổn định.
- Windows 10 (version 2004+) hoặc Windows 11.
- Quyền Administrator để cài phần mềm.

---

### 3. Labs

### 3.3.1. Environment Check ⭐ BẮT BUỘC

**Mỗi Lab phải có mục này ngay đầu tiên:**

```markdown
### 🔍 Environment Check (Trước khi bắt đầu)

Chạy các lệnh sau để kiểm tra trạng thái máy:

| Kiểm tra | Lệnh | Kết quả mong đợi |
|----------|------|------------------|
| OS Version | `winver` (Windows) | Windows 10+ hoặc 11 |
| Virtualization | Check Task Manager > Performance | Virtualization: Enabled |
| Internet | `ping google.com` | Reply from ... |

> ⚠️ **Lưu ý:** Nếu chưa bật ảo hóa (Virtualization) trong BIOS, bạn sẽ không cài được WSL2/Docker.
```

### Lab 1: Cài đặt WSL2 (Windows Subsystem for Linux)

**Bước 1: Chạy lệnh cài đặt**
Mở PowerShell với quyền Admin (Right-click > Run as Administrator) và chạy:

```powershell
wsl --install
```

**Bước 2: Khởi động lại**
Restart máy tính. Sau khi khởi động lại, cửa sổ Ubuntu sẽ tự động mở ra để tiếp tục cài đặt.

**Bước 3: Tạo User Linux**
Nhập `Username` và `Password` cho hệ điều hành Linux (Ubuntu).
*Lưu ý: Khi nhập password sẽ không hiện ký tự.*

**Verification:**
Mở PowerShell và chạy:

```powershell
wsl -l -v
```

**Output mong đợi:**

```text
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

### Lab 2: Cài đặt Docker Desktop

**Bước 1: Tải và Cài đặt**

- Tải [Docker Desktop for Windows](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe).
- Chạy file installer. Đảm bảo tích chọn "Use WSL 2 instead of Hyper-V".

**Bước 2: Settings WSL Integration**

- Mở Docker Desktop Dashboard.
- Vào **Settings (biểu tượng bánh răng) > Resources > WSL integration**.
- Bật "Enable integration with my default WSL distro".
- Bật switch ở "Ubuntu".
- Nhấn **Apply & Restart**.

**Verification:**
Mở terminal **Ubuntu (WSL)** và chạy:

```bash
docker run hello-world
```

**Output mong đợi:**

```text
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

### Lab 3: Setup Git & VS Code

**Bước 1: Cấu hình Git Global**
Trong terminal Ubuntu:

```bash
git config --global user.name "Ten Cua Ban"
git config --global user.email "email@example.com"
```

**Bước 2: Cài VS Code và Extension**

- Cài VS Code trên Windows.
- Mở VS Code, vào Extensions (Ctrl+Shift+X), cài pack **"WSL"** (Microsoft).

**Bước 3: Mở dự án từ WSL**
Trong terminal Ubuntu:

```bash
mkdir devops-course
cd devops-course
code .
```

VS Code sẽ mở ra với trạng thái kết nối tới WSL (WSL: Ubuntu).

---

### 4. Output Mẫu

Khi chạy `docker version` trong Ubuntu:

```text
Client: Docker Engine - Community
 Version:           24.0.x
 ...
Server: Docker Desktop
 Engine:
  Version:          24.0.x
```

---

### 5. Troubleshooting (Xử lý lỗi)

| Lỗi | Nguyên nhân | Cách khắc phục |
|-----|-------------|----------------|
| `wsl: command not found` | Windows cũ hoặc chưa update | Update Windows lên bản mới nhất |
| `docker command not found` (trong WSL) | Chưa bật WSL Integration | Làm lại Bước 2 của Lab 2 |
| `VS Code "Shell integration failed"` | VS Code server lỗi | Restart WSL: `wsl --shutdown` rồi mở lại |

---

### 6. Cleanup (Dọn dẹp)

Không cần dọn dẹp nhiều vì đây là setup môi trường lâu dài.
Nếu muốn xóa container test:

```bash
docker rm $(docker ps -a -q -f ancestor=hello-world)
```

---

### 7. References (Tham khảo)

- [Manual Installation Steps for Older WSL](https://learn.microsoft.com/en-us/windows/wsl/install-manual)
- [Docker Desktop WSL 2 Backend](https://docs.docker.com/desktop/windows/wsl/)
- [GLOSSARY](../../resources/GLOSSARY.md)

### 8. Navigation Footer ⭐ BẮT BUỘC

---

[⬅️ CHEATSHEET](./CHEATSHEET.md) | [📚 Mục lục](../../README.md) | [EXERCISES ➡️](./EXERCISES.md)
