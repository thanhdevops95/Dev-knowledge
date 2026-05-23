---
module: "0"
title: "Setup Environment"
track: "0"
version: "1.0"
last_updated: "2025-12-27"
author: "DevOps Team"
---

## MODULE 0 – Setup Environment

### 1. Giới thiệu

- Mô tả ngắn gọn về mục tiêu chuẩn bị môi trường.
- Tại sao môi trường chuẩn bị quan trọng cho toàn bộ khóa học.

### 2. Mục tiêu học tập

- [ ] Hiểu và cài đặt WSL2 / Docker Desktop / Git.
- [ ] Kiểm tra môi trường bằng các lệnh kiểm tra.
- [ ] Thiết lập cấu hình VS Code và các extension cần thiết.

### 3. Architecture Diagram (Sơ đồ kiến trúc)

**Ưu tiên sử dụng Mermaid.js**:

```mermaid
graph LR
    User -->|SSH/WSL| Windows[Windows OS]
    Windows -->|Docker Desktop| Docker[Docker Engine]
    Windows -->|Git| Git[Git CLI]
    Windows -->|VS Code| VS[VS Code]a
```

### 4. Lý thuyết chi tiết

- Hướng dẫn cài đặt WSL2, Docker Desktop, Git, VS Code.
- Cấu hình môi trường (PATH, Docker daemon, etc.).
- Các công cụ bổ trợ (Node.js, Python, etc.) nếu cần.

### 5. Bước thực hành ngắn (Quick Practice)

- **Bước 1:** Cài đặt WSL2 và khởi động lại.
- **Bước 2:** Cài Docker Desktop, bật Docker daemon.
- **Bước 3:** Kiểm tra phiên bản:

  ```bash
  wsl --list --verbose
  docker version
  git --version
  code --version
  ```

- **Bước 4:** Tạo thư mục dự án mẫu và mở bằng VS Code.

### 6. Tham khảo (References)

- [WSL2 Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
- [Docker Desktop Installation](https://docs.docker.com/desktop/install/windows-install/)
- [Git for Windows](https://git-scm.com/download/win)
- [VS Code Download](https://code.visualstudio.com/Download)

### 7. Navigation Footer (Điều hướng) ⭐ BẮT BUỘC

---

[⬅️ README của khoá học](../README.md) | [📚 Mục lục](../README.md) | [📄 CHEATSHEET](./CHEATSHEET.md)
