# macOS Setup Guide

> 🍎 Guide to set up DevOps environment on macOS
>
> *Hướng dẫn thiết lập môi trường DevOps trên macOS*

---

## Track 1 Setup

### Method 1: Automatic (Recommended) - Cách 1: Tự động (Khuyến nghị)

```bash
chmod +x ./scripts/macos/setup_track1.sh
./scripts/macos/setup_track1.sh
```

### Method 2: Manual (Cách 2: Thủ công)

#### Step 1: Install Homebrew (Bước 1: Cài đặt Homebrew)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install tools (Bước 2: Cài đặt các tools)

```bash
brew install git
brew install --cask docker
brew install --cask visual-studio-code
```

### Verify Track 1

```bash
./scripts/macos/verify_track1.sh
```

---

## 🔗 Navigation

[⬅️ Windows Setup](./WINDOWS_SETUP.md) | [Linux Setup ➡️](./LINUX_SETUP.md)
