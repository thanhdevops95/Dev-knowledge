# Linux Setup Guide

> 🐧 Guide to set up DevOps environment on Linux (Ubuntu/Debian)
>
> *Hướng dẫn thiết lập môi trường DevOps trên Linux (Ubuntu/Debian)*

---

## Track 1 Setup

### Method 1: Automatic (Recommended) - Cách 1: Tự động (Khuyến nghị)

```bash
chmod +x ./scripts/linux/setup_track1.sh
./scripts/linux/setup_track1.sh
```

### Method 2: Manual (Cách 2: Thủ công)

#### Step 1: Update system (Bước 1: Cập nhật hệ thống)

```bash
sudo apt update && sudo apt upgrade -y
```

#### Step 2: Install Git (Bước 2: Cài đặt Git)

```bash
sudo apt install -y git
```

#### Step 3: Install Docker (Bước 3: Cài đặt Docker)

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Verify Track 1

```bash
./scripts/linux/verify_track1.sh
```

---

## 🔗 Navigation

[⬅️ macOS Setup](./MACOS_SETUP.md) | [README ➡️](./README.md)
