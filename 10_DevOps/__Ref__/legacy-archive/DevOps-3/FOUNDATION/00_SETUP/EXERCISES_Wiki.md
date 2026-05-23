# Exercises: Module 00 - SETUP

> **Bài tập kiểm tra Environment Setup**

**Mục đích:** Verify môi trường đã setup đúng  
**Thời gian:** 15 phút

---

## 📋 EXERCISE 1: Verify WSL2 (Windows Only)

**Task:** Kiểm tra WSL2 đã cài đặt đúng

```bash
wsl --version
```

**Expected:** Version 2.x.x hiển thị

```bash
wsl -l -v
```

**Expected:** Ubuntu với VERSION = 2

---

## 📋 EXERCISE 2: Verify Shell

**Task:** Kiểm tra shell environment

```bash
echo $SHELL
echo $USER
echo $HOME
```

**Expected:**

- SHELL: /bin/bash hoặc /bin/zsh
- USER: username của bạn
- HOME: /home/username

---

## 📋 EXERCISE 3: Verify Git

**Task:** Kiểm tra Git cài đặt

```bash
git --version
git config --global user.name
git config --global user.email
```

**Expected:** Git version 2.x.x và config đã set

---

## 📋 EXERCISE 4: Verify VS Code

**Task:** Mở VS Code từ terminal

```bash
code --version
code .
```

**Expected:** VS Code version hiển thị và editor mở

---

## 📋 EXERCISE 5: Verify Docker

**Task:** Kiểm tra Docker hoạt động

```bash
docker --version
docker run hello-world
```

**Expected:** "Hello from Docker!" message

---

## 📋 EXERCISE 6: Create Directory Structure

**Task:** Tạo folder structure chuẩn

```bash
mkdir -p ~/DevOpsTraining/PROJECTS
mkdir -p ~/DevOpsTraining/notes
ls -la ~/DevOpsTraining
```

**Expected:** Thấy các folders đã tạo

---

## 📋 EXERCISE 7: Test Internet Connectivity

**Task:** Kiểm tra network

```bash
ping -c 3 google.com
curl -I https://api.github.com
```

**Expected:** Ping successful, HTTP 200

---

## 📋 EXERCISE 8: Run Verification Script

**Task:** Chạy script verify tự động

```bash
cd ~/DevOpsTraining/FOUNDATION/00_SETUP
./scripts/verify-linux.sh
```

**Expected:** All checks ✅

---

## 📊 GRADING

- **8/8:** Perfect setup! ⭐⭐⭐
- **6-7/8:** Minor issues, fixable
- **<6/8:** Review setup steps

---

**Xem SOLUTIONS.md nếu gặp vấn đề!**
