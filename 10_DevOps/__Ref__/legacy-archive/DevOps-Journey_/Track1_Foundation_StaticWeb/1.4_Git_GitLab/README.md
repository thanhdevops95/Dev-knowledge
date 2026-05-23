# 📦 Module 1.4: Git & GitLab

[![Duration](https://img.shields.io/badge/Duration-8--10%20hours-blue?style=flat-square)](.)
[![Level](https://img.shields.io/badge/Level-Beginner-green?style=flat-square)](.)

> **Version Control** - Manage code and collaborate effectively.
>
> *Quản lý phiên bản - Quản lý code và cộng tác hiệu quả.*

---

## 🎯 Learning Objectives (Mục tiêu học tập)

After this module, you will (Sau module này, bạn sẽ):

- ✅ Understand what Git is and why we need it (Hiểu Git là gì và tại sao cần dùng)
- ✅ Basic operations: init, add, commit, push, pull (Thao tác cơ bản)
- ✅ Branching and merging (Phân nhánh và hợp nhất)
- ✅ Handle conflicts (Xử lý xung đột)
- ✅ Work with GitLab and GitHub (Làm việc với GitLab và GitHub)

---

## 📋 Prerequisites (Điều kiện tiên quyết)

- Complete Module 1.3 (Hoàn thành Module 1.3)

---

## 📚 Content (Nội dung)

### 1. What is Git? (Git là gì?)

> 📖 **Real-world Scenario (Tình huống thực tế):**
>
> You're working on a project with 3 teammates. Everyone edits the same files. On deadline day, you try to merge everything - **DISASTER!** Conflicts everywhere, someone's code overwrote someone else's work, and no one knows which version is correct. You spend 6 hours fixing instead of presenting.
>
> *Bạn đang làm dự án với 3 người trong team. Mọi người cùng sửa những file giống nhau. Ngày deadline, bạn cố gắng ghép lại - **THẢM HỌa!** Xung đột khắp nơi, code của người này ghi đè lên của người khác, không ai biết phiên bản nào đúng. Bạn mất 6 tiếng sửa thay vì thuyết trình.*
>
> **With Git:** Everyone works on their own branch. Merge conflicts are caught early. You can see who changed what, when, and why. Problem solved in minutes!
>
> *Với Git: Mỗi người làm việc trên branch riêng. Xung đột được phát hiện sớm. Bạn thấy ai thay đổi gì, khi nào, và tại sao. Vấn đề giải quyết trong vài phút!*

**Git** is a Distributed Version Control System (DVCS). It tracks changes in source code during software development.

*Git là Hệ thống Quản lý Phiên bản Phân tán. Nó theo dõi các thay đổi trong mã nguồn trong quá trình phát triển phần mềm.*

**Key features (Tính năng chính):**

- **Distributed (Phân tán)**: Every developer has a full backup of the repository (Mỗi developer đều có bản backup đầy đủ của kho chứa).
- **Performance (Hiệu năng)**: Branching and merging are incredibly fast (Tạo nhánh và gộp nhánh cực nhanh).
- **Collaboration (Hợp tác)**: Multiple people can work on the same project simultaneously (Nhiều người có thể cùng làm việc trên một dự án).

```
┌─────────────────────────────────────────────────────────────┐
│                    GIT WORKFLOW                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Working      Staging       Local         Remote            │
│  Directory    Area          Repository    Repository        │
│                                                              │
│    Files   →  git add   →  git commit  →  git push   →     │
│  (modified)   (staged)     (committed)   (pushed)  GitLab  │
│                                                              │
│              ←  git restore --staged                         │
│    ←─────────────────────────  git pull  ←─────────────     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### 2. Git Configuration (Cấu hình Git)

```bash
# Configure user - required (Cấu hình user - bắt buộc)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Check configuration (Kiểm tra cấu hình)
git config --list

# Default branch (Branch mặc định)
git config --global init.defaultBranch main

# Configure editor - optional (Cấu hình editor - tùy chọn)
git config --global core.editor "code --wait"

# Line endings (Xử lý xuống dòng)
git config --global core.autocrlf true   # Windows
git config --global core.autocrlf input  # Linux/macOS
```

---

### 3. Basic Commands (Các lệnh cơ bản)

#### Initialize Repository (Khởi tạo Repository)

```bash
# Create new repo (Tạo repo mới)
git init

# Clone repo from GitLab (Clone repo từ GitLab)
git clone https://gitlab.com/user/repo.git
git clone git@gitlab.com:user/repo.git

# Clone repo from GitHub (Clone repo từ GitHub)
git clone https://github.com/user/repo.git
git clone git@github.com:user/repo.git
```

#### Basic Workflow (Quy trình cơ bản)

```bash
# Check status (Xem trạng thái)
git status

# Stage files (Đưa files vào staging)
git add file.txt          # One file (Một file)
git add .                 # All files (Tất cả files)

# Commit (Lưu thay đổi)
git commit -m "Add feature X"

# Push to remote (Push lên remote)
git push origin main

# Pull from remote (Pull từ remote)
git pull origin main
```

#### View History (Xem lịch sử)

```bash
git log                   # Full log (Log đầy đủ)
git log --oneline         # Compact (Gọn)
git log --oneline -10     # Last 10 commits (10 commits gần nhất)
git log --graph           # With graph (Với biểu đồ)
```

---

### 4. Branching (Phân nhánh)

```
main      ─────●─────●─────●─────────●─────►
               │                     ▲
               │     ┌──────●─────●──┘
               │     │   feature branch
               └─────┘
```

#### Working with Branches (Làm việc với branches)

```bash
# View branches (Xem branches)
git branch              # Local
git branch -a           # Local + Remote

# Create new branch (Tạo branch mới)
git branch feature-x

# Switch branch (Chuyển branch)
git checkout feature-x
git switch feature-x    # Modern syntax (Cú pháp mới)

# Create and switch - 1 command (Tạo và chuyển - 1 lệnh)
git checkout -b feature-x
git switch -c feature-x

# Delete branch (Xóa branch)
git branch -d feature-x   # Already merged (Đã merge)
git branch -D feature-x   # Force delete (Xóa cưỡng bức)
```

#### Merge (Hợp nhất)

```bash
# On main, merge feature into (Đứng ở main, merge feature vào)
git checkout main
git merge feature-x

# Merge with commit message (Merge với commit message)
git merge feature-x -m "Merge feature-x into main"
```

---

### 5. Common Git Workflow (Quy trình Git phổ biến)

#### Feature Branch Workflow

```bash
# 1. Update main (Cập nhật main)
git checkout main
git pull origin main

# 2. Create feature branch (Tạo feature branch)
git checkout -b feature/login-page

# 3. Work and commit (Làm việc và commit)
git add .
git commit -m "Add login form"
git commit -m "Add validation"

# 4. Push branch (Push branch)
git push origin feature/login-page

# 5. Create Merge Request on GitLab (Tạo Merge Request trên GitLab)
#    Or Pull Request on GitHub (Hoặc Pull Request trên GitHub)

# 6. After merge, delete branch (Sau khi merge, xóa branch)
git checkout main
git pull origin main
git branch -d feature/login-page
```

---

### 6. Handling Conflicts (Xử lý xung đột)

```bash
# When merge or pull has conflict (Khi merge hoặc pull có xung đột)
<<<<<<< HEAD
code from current branch (code từ branch hiện tại)
=======
code from other branch (code từ branch khác)
>>>>>>> feature-x

# Resolve (Giải quyết):
# 1. Edit file, remove conflict markers (Sửa file, xóa các dấu xung đột)
# 2. git add file-that-was-fixed (git add file-đã-sửa)
# 3. git commit
```

---

### 7. Undo Changes (Hoàn tác thay đổi)

```bash
# Unstage file (Bỏ stage file)
git restore --staged file.txt

# Discard changes - not committed (Bỏ thay đổi - chưa commit)
git restore file.txt

# Undo last commit - keep changes (Hoàn tác commit cuối - giữ changes)
git reset --soft HEAD~1

# Undo last commit - delete changes (Hoàn tác commit cuối - xóa changes)
# DANGEROUS! (NGUY HIỂM!)
git reset --hard HEAD~1

# Revert commit - create reverse commit (Revert commit - tạo commit ngược)
git revert abc1234
```

---

### 8. .gitignore

```bash
# File: .gitignore

# Dependencies (Thư viện)
node_modules/
vendor/
venv/

# Build outputs (Kết quả build)
dist/
build/
*.pyc

# IDE
.vscode/
.idea/

# Secrets (Bí mật)
.env
*.key
secrets/

# OS files (Files hệ điều hành)
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

---

### 9. SSH Keys Setup (Cấu hình SSH Keys)

> This course supports both **GitLab** (primary) and **GitHub**.
>
> *Khóa học hỗ trợ cả **GitLab** (chính) và **GitHub**.*

#### Generate SSH Key (Tạo SSH key)

```bash
# Generate SSH key (Tạo SSH key)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key (Thêm key)
ssh-add ~/.ssh/id_ed25519

# Copy public key (Copy public key)
cat ~/.ssh/id_ed25519.pub
```

#### For GitLab (Primary - Chính)

```bash
# Paste key to: GitLab > Preferences > SSH Keys
# (Dán key vào: GitLab > Preferences > SSH Keys)

# Test connection (Kiểm tra kết nối)
ssh -T git@gitlab.com
# Expected: Welcome to GitLab, @username!
```

#### For GitHub (Alternative - Thay thế)

```bash
# Paste key to: GitHub > Settings > SSH and GPG Keys
# (Dán key vào: GitHub > Settings > SSH and GPG Keys)

# Test connection (Kiểm tra kết nối)
ssh -T git@github.com
# Expected: Hi username! You've successfully authenticated...
```

---

### 10. GitLab vs GitHub Comparison (So sánh)

| Feature | GitLab | GitHub |
|---------|--------|--------|
| **Merge Request/Pull Request** | Merge Request (MR) | Pull Request (PR) |
| **CI/CD Config** | `.gitlab-ci.yml` | `.github/workflows/*.yml` |
| **Container Registry** | Built-in | GitHub Packages |
| **Free Private Repos** | ✅ Yes | ✅ Yes |
| **Self-hosted** | GitLab CE (free) | GitHub Enterprise (paid) |
| **Issue Tracking** | ✅ Yes | ✅ Yes |

---

> ✅ **Checkpoint - Before continuing, make sure you can answer:**
> *(Trước khi tiếp tục, hãy chắc bạn có thể trả lời:)*
>
> - [ ] What's the difference between `git add` and `git commit`? *(git add và git commit khác nhau như thế nào?)*
> - [ ] How to create a new branch and switch to it? *(Làm sao tạo branch mới và chuyển sang nó?)*
> - [ ] How to resolve a merge conflict? *(Làm sao giải quyết xung đột khi merge?)*
> - [ ] What should be in `.gitignore`? *(Những gì nên đưa vào .gitignore?)*
>
> *If you can't answer, please re-read the sections above!*

## 📝 Module Files (Các file trong Module)

| File | Description |
|------|---------------------|
| [CHEATSHEET.md](./CHEATSHEET.md) | Quick reference Git (Tra cứu nhanh Git) |
| [LABS.md](./LABS.md) | Hands-on labs (Bài thực hành) |
| [QUIZ.md](./QUIZ.md) | Knowledge check (Kiểm tra kiến thức) |
| [EXERCISES.md](./EXERCISES.md) | Exercises (Bài tập) |
| [PROJECT.md](./PROJECT.md) | Mini project (Dự án nhỏ) |
| [SOLUTIONS.md](./SOLUTIONS.md) | Solutions (Đáp án) |

---

<div align="center">

### 🔗 Module Navigation (Điều hướng Module)

| ← Previous | Current | Next → |
|:------------------:|:------------------:|:-------------:|
| [1.3 Network](../1.3_Network_Basics/) | **1.4 Git & GitLab** | [1.5 Docker](../1.5_Docker_Fundamentals/) |

---

**Master version control with Git! 📦**

*Thành thạo quản lý phiên bản với Git!*

</div>
