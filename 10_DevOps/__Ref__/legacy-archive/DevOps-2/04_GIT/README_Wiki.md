# Module 04: Git & Version Control

---

# 📚 Bảng thuật ngữ

| Thuật ngữ | Phiên âm | Giải thích |
|-----------|----------|------------|
| **Git** | /ɡɪt/ | Hệ thống quản lý phiên bản mã nguồn phổ biến nhất |
| **Repository** | - | Kho chứa - Nơi lưu trữ code và lịch sử thay đổi |
| **Commit** | - | Snapshot - Một phiên bản được lưu lại |
| **Branch** | - | Nhánh - Dòng phát triển độc lập |
| **Merge** | - | Hợp nhất - Kết hợp code từ nhánh khác |
| **Clone** | - | Sao chép repository về máy local |
| **Push** | - | Đẩy code từ local lên remote |
| **Pull** | - | Kéo code từ remote về local |
| **Staging Area** | - | Vùng chuẩn bị - Nơi chờ commit |
| **Remote** | - | Kho từ xa - GitHub, GitLab, Bitbucket |
| **Conflict** | - | Xung đột - Khi 2 người sửa cùng dòng code |
| **Tag** | - | Nhãn đánh dấu version (v1.0.0) |
| **Checkout** | - | Chuyển sang branch hoặc commit khác |
| **Revert** | - | Hoàn tác commit bằng commit mới |

---

## 🎬 Câu chuyện mở đầu

Tưởng tượng bạn đang viết code. Mọi thứ hoạt động. Bạn quyết định "cải thiện" một chút...

30 phút sau: **Code không chạy nữa.**

Bạn cố sửa, càng sửa càng tệ. Giá như có thể **quay lại phiên bản trước đó**...

Đây chính là lý do **Git** tồn tại.

---

## 📖 Git là gì?

### Version Control System (VCS)

**Git** = Hệ thống quản lý phiên bản mã nguồn

Tưởng tượng như **save game** trong video game:

- Bạn có thể save tại nhiều điểm
- Quay lại bất kỳ save nào
- Thử nghiệm mà không sợ mất progress

### Tại sao DevOps cần Git?

| Không Git | Có Git |
|-----------|--------|
| `file_v1.py`, `file_v2.py`, `file_final.py`, `file_final_REAL.py` | Một file, nhiều versions |
| "Ai đã sửa dòng này?" | `git blame` cho bạn biết |
| "Code hôm qua chạy, hôm nay không" | `git diff` xem thay đổi |
| Merge code bằng copy-paste | `git merge` tự động |
| Mất code khi đổi máy | Code trên cloud (GitHub) |

---

## 🏗️ Kiến trúc Git

### 3 vùng chính

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   │
│  │  Working    │   │   Staging   │   │    Local    │   │
│  │  Directory  │──▶│    Area     │──▶│ Repository  │   │
│  │             │   │             │   │             │   │
│  │  (Files     │   │  (Chuẩn bị  │   │  (Lịch sử   │   │
│  │   thực tế)  │   │   commit)   │   │   commits)  │   │
│  └─────────────┘   └─────────────┘   └─────────────┘   │
│        │                 │                  │            │
│        │     git add     │    git commit    │            │
│        └────────────────►└─────────────────►│            │
│                                             │            │
└─────────────────────────────────────────────┼────────────┘
                                              │
                                              │ git push
                                              ▼
                                    ┌─────────────────┐
                                    │     GitHub      │
                                    │  (Remote Repo)  │
                                    └─────────────────┘
```

### Giải thích

1. **Working Directory** - Folder chứa files bạn đang edit
2. **Staging Area** - "Sân khấu" - files chuẩn bị commit
3. **Local Repository** - Lịch sử tất cả commits trên máy bạn
4. **Remote Repository** - Copy trên GitHub (hoặc GitLab, Bitbucket)

---

## 🚀 Các lệnh cơ bản

### Khởi tạo repository

```bash
# Tạo repo mới trong folder hiện tại
git init

# Clone repo có sẵn
git clone https://github.com/username/repo.git
```

### Workflow cơ bản

```bash
# 1. Xem thay đổi
git status

# 2. Thêm files vào staging
git add filename.txt      # Một file
git add .                 # Tất cả files

# 3. Commit với message
git commit -m "Add new feature"

# 4. Push lên remote
git push origin main
```

### Xem lịch sử

```bash
# Xem tất cả commits
git log

# Xem ngắn gọn
git log --oneline

# Xem đẹp với graph
git log --oneline --graph --all
```

---

## 📝 Commit - "Save game" của Git

### Commit là gì?

**Commit** = Snapshot của code tại một thời điểm

```
Commit 1: "Initial project setup"
    │
    │  (thay đổi code)
    ▼
Commit 2: "Add user login"
    │
    │  (thay đổi code)
    ▼
Commit 3: "Fix login bug"
    │
    ▼
   ...
```

### Viết commit message tốt

**SAI:**

```
git commit -m "fix"
git commit -m "update"
git commit -m "asdfgh"
```

**ĐÚNG:**

```
git commit -m "Fix login redirect after authentication"
git commit -m "Add password validation to signup form"
git commit -m "Update README with installation instructions"
```

### Conventional Commits

Format phổ biến:

```
<type>: <description>

Types:
- feat:     Tính năng mới
- fix:      Sửa bug
- docs:     Documentation
- style:    Format code (không đổi logic)
- refactor: Tái cấu trúc code
- test:     Thêm/sửa tests
- chore:    Việc vặt (update dependencies)
```

**Ví dụ:**

```bash
git commit -m "feat: add user registration API"
git commit -m "fix: resolve null pointer in payment processing"
git commit -m "docs: update API documentation"
```

---

## 🌿 Branches - Làm việc song song

### Branch là gì?

**Branch** = Nhánh phát triển độc lập

```
main:     A---B---C---D---E
                   \
feature:            X---Y---Z
```

- `main` là nhánh chính (production)
- `feature` là nhánh để phát triển tính năng mới
- Làm trên `feature`, không ảnh hưởng `main`
- Khi xong, merge `feature` vào `main`

### Làm việc với branches

```bash
# Xem tất cả branches
git branch

# Tạo branch mới
git branch feature-login

# Chuyển sang branch
git checkout feature-login

# Tạo + chuyển (shortcut)
git checkout -b feature-login

# Xóa branch (sau khi đã merge)
git branch -d feature-login
```

### Merge branches

```bash
# Đang ở feature-login, muốn merge vào main

# 1. Chuyển về main
git checkout main

# 2. Merge feature-login vào main
git merge feature-login
```

### Git Flow - Workflow phổ biến

```
main (production)
 │
 ├── develop (development)
 │    │
 │    ├── feature/login
 │    ├── feature/payment
 │    └── feature/dashboard
 │
 └── hotfix/critical-bug
```

---

## 🔄 Remote - Làm việc với GitHub

### Thêm remote

```bash
# Xem remotes hiện có
git remote -v

# Thêm remote (thường tên origin)
git remote add origin https://github.com/username/repo.git
```

### Push và Pull

```bash
# Push lên remote
git push origin main

# Pull (lấy thay đổi từ remote)
git pull origin main

# Push lần đầu với -u để set upstream
git push -u origin main
# Sau đó chỉ cần: git push
```

### Fetch vs Pull

```bash
# Fetch: Lấy thông tin, không merge
git fetch origin

# Pull = Fetch + Merge
git pull origin main
```

---

## ⚔️ Merge Conflicts

### Khi nào xảy ra?

Khi 2 người cùng sửa một dòng code.

```bash
# Bạn sửa file.txt dòng 5: "Hello World"
# Đồng nghiệp sửa file.txt dòng 5: "Hi there"

git merge feature-branch
# CONFLICT (content): Merge conflict in file.txt
```

### Conflict trông như thế nào?

```
<<<<<<< HEAD
Hello World
=======
Hi there
>>>>>>> feature-branch
```

- Code giữa `<<<<<<< HEAD` và `=======` là của bạn
- Code giữa `=======` và `>>>>>>>` là của người kia

### Giải quyết conflict

1. **Mở file** và chọn giữ code nào (hoặc kết hợp)
2. **Xóa markers** (`<<<<`, `====`, `>>>>`)
3. **Stage và commit**

```bash
git add file.txt
git commit -m "Resolve merge conflict in file.txt"
```

---

## ⏪ Undo - Quay lại phiên bản cũ

### Chưa stage (chưa git add)

```bash
# Bỏ thay đổi trong file
git checkout -- filename.txt

# Bỏ tất cả thay đổi
git checkout -- .
```

### Đã stage (đã git add, chưa commit)

```bash
# Unstage file (giữ thay đổi trong working directory)
git reset HEAD filename.txt

# Unstage tất cả
git reset HEAD
```

### Đã commit

```bash
# Xem lịch sử
git log --oneline

# Quay lại commit cụ thể (giữ thay đổi)
git reset --soft abc1234

# Quay lại commit cụ thể (xóa thay đổi)
git reset --hard abc1234
```

### Revert (tạo commit mới để undo)

```bash
# Undo commit nhưng giữ lịch sử
git revert abc1234
# Tạo commit mới có nội dung ngược lại commit abc1234
```

---

## 🏷️ Tags - Đánh dấu version

```bash
# Tạo tag nhẹ
git tag v1.0.0

# Tạo tag với annotation
git tag -a v1.0.0 -m "Version 1.0.0 release"

# Push tags lên remote
git push origin v1.0.0
git push origin --tags  # Tất cả tags

# Xem tags
git tag

# Checkout tag
git checkout v1.0.0
```

---

## 🔧 .gitignore - Loại trừ files

### Tạo .gitignore

```bash
# .gitignore

# Dependencies
node_modules/
vendor/
venv/

# Build outputs
dist/
build/
*.pyc
__pycache__/

# IDE
.idea/
.vscode/
*.swp

# Environment
.env
*.local

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Secrets
*.pem
*.key
secrets/
```

### Templates phổ biến

- [Node.js](https://github.com/github/gitignore/blob/main/Node.gitignore)
- [Python](https://github.com/github/gitignore/blob/main/Python.gitignore)
- [Java](https://github.com/github/gitignore/blob/main/Java.gitignore)

---

## 📝 Tổng kết Module 04

### Bạn đã học

✅ Git là gì và tại sao cần  
✅ 3 vùng: Working, Staging, Repository  
✅ Commits và cách viết message tốt  
✅ Branches và merging  
✅ Remote và GitHub  
✅ Giải quyết conflicts  
✅ Undo changes  
✅ Tags và .gitignore  

### Commands cheat sheet

```bash
# Khởi tạo
git init / git clone

# Daily workflow
git status
git add .
git commit -m "message"
git push

# Branches
git branch / git checkout -b / git merge

# Undo
git checkout -- / git reset / git revert

# Info
git log --oneline / git diff / git blame
```

---

## 🚨 Lỗi thường gặp khi dùng Git

### 1. "Ủa, tôi vừa commit secrets lên Git!"

**Tình huống:** Bạn lỡ commit file chứa password, API key lên repository.

**NGUY HIỂM:** Xóa file và commit mới KHÔNG đủ — secrets vẫn còn trong Git history!

**Cách fix:**

```bash
# Cách 1: BFG Repo-Cleaner (nhanh nhất)
# Download: https://rtyley.github.io/bfg-repo-cleaner/
bfg --delete-files secrets.env
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force

# Cách 2: git filter-branch (built-in)
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch secrets.env" \
  --prune-empty --tag-name-filter cat -- --all

# SAU ĐÓ: Đổi tất cả passwords/keys đã bị lộ!
```

---

### 2. "fatal: refusing to merge unrelated histories"

**Tình huống:** Pull từ remote nhưng bị từ chối.

**Nguyên nhân:** Local repo và remote có history khác nhau (thường do tạo repo với README trên GitHub rồi link với local existing project).

**Cách fix:**

```bash
# Cho phép merge histories không liên quan
git pull origin main --allow-unrelated-histories
# Resolve conflicts nếu có
```

---

### 3. "Tôi commit nhầm branch!"

**Tình huống:** Bạn commit vào `main` thay vì `feature` branch.

**Cách fix:**

```bash
# Chưa push? Di chuyển commit sang branch mới
git branch feature-abc      # Tạo branch mới từ commit hiện tại
git reset --hard HEAD~1     # Main quay lại 1 commit
git checkout feature-abc    # Chuyển sang branch mới

# Đã push? Tạo revert commit
git revert HEAD
git push
```

---

### 4. "Merge conflict! Làm sao giải quyết?"

**Tình huống:** Git không tự động merge được vì 2 người sửa cùng dòng code.

**Cách fix:**

```bash
# Git sẽ đánh dấu conflicts trong file:
<<<<<<< HEAD
Code của bạn
=======
Code của người khác
>>>>>>> feature-branch

# Bước 1: Mở file, chọn code đúng (xóa markers)
# Bước 2: Add và commit
git add .
git commit -m "Resolve merge conflicts"

# Mẹo: Dùng VS Code có UI giải quyết conflict dễ hơn
```

---

### 5. "Tôi muốn undo commit cuối!"

**Tình huống:** Commit xong mới nhận ra sai.

**Cách fix (tùy tình huống):**

```bash
# Chưa push? Undo commit, giữ changes
git reset --soft HEAD~1

# Chưa push? Undo commit, bỏ changes
git reset --hard HEAD~1

# Đã push? Tạo revert commit (safe)
git revert HEAD
git push

# CHÚ Ý: KHÔNG dùng reset --hard nếu đã push!
# Vì sẽ gây conflict cho teammates
```

---

## ⏭️ Tiếp theo

👉 **[LABS.md - Thực hành Git](LABS.md)**
