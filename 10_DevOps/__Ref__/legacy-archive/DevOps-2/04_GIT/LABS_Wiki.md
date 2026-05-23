# Module 04: Git Labs

---

## 🎯 Mục tiêu

Sau labs này, bạn sẽ:

- Thực hành Git workflow hoàn chỉnh
- Làm việc với branches
- Giải quyết merge conflicts
- Sử dụng Git như một DevOps

---

## 🔧 Lab 1: First Repository

### 🎬 Bối cảnh

Tạo repo đầu tiên cho dự án Counter App.

### Bước 1: Cấu hình Git

```bash
# Config user info (lần đầu dùng Git)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Kiểm tra
git config --list
```

### Bước 2: Tạo repository

```bash
cd ~
mkdir my-first-repo
cd my-first-repo

# Khởi tạo Git
git init

# Xem thư mục .git được tạo
ls -la
```

### Bước 3: Tạo file đầu tiên

```bash
echo "# My First Project" > README.md
echo "This is my first Git repository!" >> README.md

cat README.md
```

### Bước 4: First commit

```bash
# Xem status
git status
# Output: Untracked files: README.md

# Add to staging
git add README.md

# Xem status lại
git status
# Output: Changes to be committed: new file: README.md

# Commit
git commit -m "Initial commit: add README"

# Xem lịch sử
git log --oneline
```

### ✅ Checkpoint Lab 1

- [ ] Tạo được repo với `git init`
- [ ] Hiểu flow: edit → add → commit
- [ ] Xem được log

---

## 📝 Lab 2: Multiple Commits

### Bước 1: Thêm nhiều files

```bash
# Tạo app.py
cat > app.py << 'EOF'
def hello():
    print("Hello, World!")

if __name__ == "__main__":
    hello()
EOF

# Commit
git add app.py
git commit -m "feat: add main app file"
```

### Bước 2: Sửa file và commit

```bash
# Sửa app.py
cat > app.py << 'EOF'
def hello(name="World"):
    print(f"Hello, {name}!")

def goodbye(name="World"):
    print(f"Goodbye, {name}!")

if __name__ == "__main__":
    hello("DevOps")
    goodbye("DevOps")
EOF

# Xem thay đổi
git diff

# Commit
git add app.py
git commit -m "feat: add goodbye function and parameter support"
```

### Bước 3: Xem history

```bash
git log --oneline

# Output:
# abc1234 feat: add goodbye function and parameter support
# def5678 feat: add main app file
# 9876fed Initial commit: add README
```

### Bước 4: Xem chi tiết một commit

```bash
git show abc1234
```

### ✅ Checkpoint Lab 2

- [ ] Tạo nhiều commits
- [ ] Dùng `git diff` xem thay đổi
- [ ] Dùng `git show` xem chi tiết

---

## 🌿 Lab 3: Working with Branches

### 🎬 Bối cảnh

Thêm tính năng mới mà không ảnh hưởng code hiện tại.

### Bước 1: Tạo feature branch

```bash
# Xem branch hiện tại
git branch
# * main

# Tạo và chuyển sang branch mới
git checkout -b feature/add-config

# Kiểm tra
git branch
#   main
# * feature/add-config
```

### Bước 2: Làm việc trên feature branch

```bash
# Tạo config file
cat > config.py << 'EOF'
# Configuration
DEBUG = True
APP_NAME = "My App"
VERSION = "1.0.0"
EOF

git add config.py
git commit -m "feat: add configuration file"

# Sửa app.py để dùng config
cat > app.py << 'EOF'
from config import APP_NAME, VERSION

def hello(name="World"):
    print(f"Hello from {APP_NAME} v{VERSION}!")
    print(f"Hello, {name}!")

if __name__ == "__main__":
    hello("DevOps")
EOF

git add app.py
git commit -m "feat: integrate config into app"

# Xem log của branch này
git log --oneline
```

### Bước 3: Quay lại main

```bash
git checkout main

# Xem files - config.py không có!
ls

# Vì config.py chỉ tồn tại trên feature branch
```

### Bước 4: Merge feature vào main

```bash
# Đảm bảo đang ở main
git checkout main

# Merge feature branch
git merge feature/add-config

# Xem log
git log --oneline --graph
```

### Bước 5: Xóa feature branch (đã merge)

```bash
git branch -d feature/add-config

git branch
# * main
```

### ✅ Checkpoint Lab 3

- [ ] Tạo và chuyển branches
- [ ] Làm việc độc lập trên branch
- [ ] Merge branch vào main

---

## ⚔️ Lab 4: Resolve Merge Conflicts

### 🎬 Bối cảnh

Hai người cùng sửa một file - Git không biết chọn thay đổi nào.

### Bước 1: Tạo tình huống conflict

```bash
# Tạo branch A
git checkout -b feature/update-version

# Sửa config.py
sed -i 's/VERSION = "1.0.0"/VERSION = "2.0.0"/' config.py
git add config.py
git commit -m "bump version to 2.0.0"

# Quay lại main
git checkout main

# Tạo branch B từ main (không có thay đổi của A)
git checkout -b feature/fix-version

# Sửa config.py khác đi
sed -i 's/VERSION = "1.0.0"/VERSION = "1.0.1"/' config.py
git add config.py
git commit -m "bump version to 1.0.1"

# Merge A vào main
git checkout main
git merge feature/update-version
# Thành công!

# Thử merge B vào main
git merge feature/fix-version
# CONFLICT!
```

### Bước 2: Xem conflict

```bash
git status
# both modified: config.py

cat config.py
```

**Output:**

```python
# Configuration
DEBUG = True
APP_NAME = "My App"
<<<<<<< HEAD
VERSION = "2.0.0"
=======
VERSION = "1.0.1"
>>>>>>> feature/fix-version
```

### Bước 3: Giải quyết conflict

```bash
# Edit file và chọn version đúng
cat > config.py << 'EOF'
# Configuration
DEBUG = True
APP_NAME = "My App"
VERSION = "2.0.0"
EOF

# Mark as resolved
git add config.py

# Complete merge
git commit -m "Merge feature/fix-version, keep v2.0.0"
```

### ✅ Checkpoint Lab 4

- [ ] Hiểu khi nào xảy ra conflict
- [ ] Đọc được conflict markers
- [ ] Giải quyết và hoàn thành merge

---

## 🔗 Lab 5: Working with Remote (GitHub)

### 🎬 Bối cảnh

Push code lên GitHub để backup và collaborate.

### Bước 1: Tạo repo trên GitHub

1. Vào github.com
2. Click "New repository"
3. Name: `my-first-repo`
4. **KHÔNG** tick "Add README" (vì đã có local)
5. Click "Create repository"

### Bước 2: Connect local repo với GitHub

```bash
# Thêm remote (copy URL từ GitHub)
git remote add origin https://github.com/YOUR_USERNAME/my-first-repo.git

# Kiểm tra
git remote -v
```

### Bước 3: Push lên GitHub

```bash
# Push lần đầu
git push -u origin main

# Kiểm tra trên GitHub - code đã có!
```

### Bước 4: Clone repo (giả lập máy khác)

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/my-first-repo.git my-repo-clone
cd my-repo-clone

# Xem nội dung
ls
git log --oneline
```

### Bước 5: Pull changes

```bash
# Trên repo gốc, tạo thay đổi
cd ~/my-first-repo
echo "New line" >> README.md
git add README.md
git commit -m "docs: update README"
git push

# Trên clone, pull changes
cd ~/my-repo-clone
git pull origin main

# Xem file đã update
cat README.md
```

### ✅ Checkpoint Lab 5

- [ ] Tạo repo trên GitHub
- [ ] Push code lên
- [ ] Clone và pull changes

---

## ⏪ Lab 6: Undo Changes

### Bước 1: Undo changes chưa stage

```bash
# Sửa file
echo "Bad change" >> app.py

# Xem thay đổi
git diff

# Undo
git checkout -- app.py

# Kiểm tra - thay đổi đã biến mất
git diff
```

### Bước 2: Undo staged changes

```bash
# Sửa và stage
echo "Bad change" >> app.py
git add app.py

git status
# Changes to be committed: modified app.py

# Unstage
git reset HEAD app.py

git status
# Changes not staged: modified app.py

# Undo file change
git checkout -- app.py
```

### Bước 3: Undo last commit (keep changes)

```bash
# Tạo commit xấu
echo "Mistake" >> app.py
git add app.py
git commit -m "oops"

# Undo commit, giữ thay đổi
git reset --soft HEAD~1

git status
# Changes to be committed: modified app.py

# Sửa lại rồi commit đúng
git checkout -- app.py
```

### Bước 4: Revert commit (safe way)

```bash
# Tạo commit
echo "Feature X" >> app.py
git add app.py
git commit -m "feat: add feature X"

# Sau này phát hiện feature X có bug, cần undo
# Nhưng muốn giữ lịch sử

git revert HEAD
# Tạo commit mới undo thay đổi của commit trước
```

### ✅ Checkpoint Lab 6

- [ ] Undo changes chưa stage
- [ ] Unstage changes
- [ ] Revert commits

---

## 🏷️ Lab 7: Tags

### Bước 1: Tạo release

```bash
# Đảm bảo code ổn định
git log --oneline

# Tạo tag
git tag -a v1.0.0 -m "First stable release"

# Xem tags
git tag

# Xem chi tiết tag
git show v1.0.0
```

### Bước 2: Push tag lên GitHub

```bash
git push origin v1.0.0

# Push tất cả tags
git push origin --tags
```

### Bước 3: Checkout tag

```bash
# Xem code tại version cụ thể
git checkout v1.0.0

# Quay lại main
git checkout main
```

### ✅ Checkpoint Lab 7

- [ ] Tạo annotated tags
- [ ] Push tags
- [ ] Checkout tags

---

## 📋 Lab 8: .gitignore

### Bước 1: Tạo files không muốn track

```bash
# Virtual environment
python3 -m venv venv

# Config local
echo "SECRET_KEY=abc123" > .env

# Build output
mkdir build
touch build/app.bin

# Logs
touch app.log

git status
# Rất nhiều files mới!
```

### Bước 2: Tạo .gitignore

```bash
cat > .gitignore << 'EOF'
# Virtual environment
venv/

# Environment variables
.env
*.local

# Build
build/
dist/

# Logs
*.log

# Python
__pycache__/
*.pyc

# IDE
.idea/
.vscode/
EOF

git status
# Chỉ còn .gitignore!

git add .gitignore
git commit -m "chore: add .gitignore"
```

### ✅ Checkpoint Lab 8

- [ ] Tạo .gitignore
- [ ] Hiểu patterns trong .gitignore

---

## 🎓 Tổng kết Labs

| Lab | Skill | Commands |
|-----|-------|----------|
| 1 | Init & commit | `git init`, `git add`, `git commit` |
| 2 | Multiple commits | `git diff`, `git log`, `git show` |
| 3 | Branches | `git branch`, `git checkout`, `git merge` |
| 4 | Conflicts | Manual resolve, `git add` |
| 5 | Remote | `git remote`, `git push`, `git pull` |
| 6 | Undo | `git reset`, `git revert`, `git checkout` |
| 7 | Tags | `git tag`, `git push --tags` |
| 8 | Ignore | `.gitignore` |

---

## ⏭️ Tiếp theo

👉 **[SCENARIOS.md - Tình huống Git thực tế](SCENARIOS.md)**
