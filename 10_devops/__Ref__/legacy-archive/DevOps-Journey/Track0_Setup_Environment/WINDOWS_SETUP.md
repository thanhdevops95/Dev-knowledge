# Windows Setup Guide

> 🪟 Guide to set up DevOps environment on Windows 10/11
>
> *Hướng dẫn thiết lập môi trường DevOps trên Windows 10/11*

---

## Track 1 Setup

### Method 1: Automatic (Recommended) - Cách 1: Tự động (Khuyến nghị)

```powershell
# Open PowerShell as Administrator (Mở PowerShell với quyền Administrator)
Set-ExecutionPolicy Bypass -Scope Process -Force
.\scripts\windows\setup_track1.ps1
```

### Method 2: Manual (Cách 2: Thủ công)

#### Step 1: Install WSL2 (Bước 1: Cài đặt WSL2)

1. Open PowerShell as Administrator *(Mở PowerShell với quyền Administrator)*
2. Run the command *(Chạy lệnh)*:

   ```powershell
   wsl --install
   ```

3. Restart your computer *(Khởi động lại máy tính)*

#### Step 2: Install Docker Desktop (Bước 2: Cài đặt Docker Desktop)

1. Download from [Docker Desktop](https://www.docker.com/products/docker-desktop/) *(Tải từ Docker Desktop)*
2. Run the installer *(Chạy installer)*
3. Start Docker Desktop *(Khởi động Docker Desktop)*

#### Step 3: Install Git (Bước 3: Cài đặt Git)

1. Download from [Git SCM](https://git-scm.com/download/win) *(Tải từ Git SCM)*
2. Run installer with default options *(Chạy installer với default options)*

#### Step 4: Install VS Code (Bước 4: Cài đặt VS Code)

1. Download from [VS Code](https://code.visualstudio.com/) *(Tải từ VS Code)*
2. Install extensions: Docker, Remote WSL *(Cài đặt extensions: Docker, Remote WSL)*

### Verify Track 1

```powershell
.\scripts\windows\verify_track1.ps1
```

---

## Track 2 Setup

*(Content will be added / Nội dung sẽ được bổ sung)*

---

## Track 3 Setup

*(Content will be added / Nội dung sẽ được bổ sung)*

---

## Track 4 Setup

*(Content will be added / Nội dung sẽ được bổ sung)*

---

## 🔗 Navigation

[⬅️ README](./README.md) | [macOS Setup ➡️](./MACOS_SETUP.md)
