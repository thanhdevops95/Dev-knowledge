# 🧱 Git — Kiểm soát phiên bản

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Công cụ bắt buộc với mọi lập trình viên

---

## Git là gì?

**Git** là hệ thống kiểm soát phiên bản phân tán (Distributed Version Control System). Nó giúp bạn:
- Theo dõi **lịch sử thay đổi** của code
- Làm việc **song song** với nhiều người trên cùng dự án
- **Quay lại** phiên bản cũ khi có lỗi
- Tạo **nhánh** để phát triển tính năng riêng biệt

---

## Cài đặt

```bash
# macOS
brew install git

# Ubuntu/Debian
sudo apt install git

# Windows
# Tải tại: https://git-scm.com/download/win
```

Cấu hình ban đầu:
```bash
git config --global user.name "Tên của bạn"
git config --global user.email "email@example.com"
git config --global core.editor "code --wait"   # dùng VS Code
```

---

## Các khái niệm cốt lõi

| Khái niệm | Giải thích |
|---|---|
| **Repository (repo)** | Thư mục dự án được Git theo dõi |
| **Commit** | Một "ảnh chụp" trạng thái code tại một thời điểm |
| **Branch** | Nhánh phát triển song song |
| **Merge** | Gộp 2 nhánh lại với nhau |
| **Remote** | Repo trên server (GitHub, GitLab...) |
| **Clone** | Tải repo từ remote về máy |
| **Pull** | Lấy thay đổi mới từ remote |
| **Push** | Đẩy thay đổi lên remote |

---

## Workflow cơ bản

```
Working Directory  →  Staging Area  →  Local Repo  →  Remote Repo
     (edit)           (git add)        (git commit)    (git push)
```

---

## Lệnh thường dùng

### Khởi tạo & Clone
```bash
git init                        # Khởi tạo repo mới
git clone <url>                 # Clone repo về máy
git clone <url> my-folder       # Clone vào thư mục cụ thể
```

### Xem trạng thái
```bash
git status                      # Xem file nào đã thay đổi
git log --oneline               # Xem lịch sử commit ngắn gọn
git log --oneline --graph       # Xem dạng cây nhánh
git diff                        # Xem thay đổi chưa staged
git diff --staged               # Xem thay đổi đã staged
```

### Add & Commit
```bash
git add file.txt                # Stage 1 file
git add .                       # Stage tất cả thay đổi
git add -p                      # Stage từng phần (interactive)
git commit -m "feat: add login" # Commit với message
git commit --amend              # Sửa commit cuối
```

### Branches
```bash
git branch                      # Liệt kê các nhánh
git branch feature/login        # Tạo nhánh mới
git checkout feature/login      # Chuyển sang nhánh
git switch feature/login        # Cách mới (Git 2.23+)
git checkout -b feature/login   # Tạo và chuyển sang nhánh mới
git merge feature/login         # Merge nhánh vào nhánh hiện tại
git branch -d feature/login     # Xóa nhánh (đã merge)
git branch -D feature/login     # Xóa nhánh (force)
```

### Remote
```bash
git remote -v                   # Xem các remote
git remote add origin <url>     # Thêm remote
git push origin main            # Push lên nhánh main
git push -u origin main         # Push và set upstream
git pull                        # Pull thay đổi từ remote
git fetch                       # Fetch nhưng chưa merge
```

### Undo
```bash
git restore file.txt            # Bỏ thay đổi chưa staged
git restore --staged file.txt   # Unstage file
git revert <commit-hash>        # Tạo commit đảo ngược
git reset --soft HEAD~1         # Undo commit, giữ staged
git reset --mixed HEAD~1        # Undo commit, giữ ở working dir
git reset --hard HEAD~1         # Undo commit, xóa hết (⚠️ nguy hiểm)
```

### Stash
```bash
git stash                       # Lưu tạm thay đổi
git stash pop                   # Lấy lại thay đổi
git stash list                  # Liệt kê stash
git stash drop stash@{0}        # Xóa 1 stash
```

---

## Conventional Commits (Chuẩn đặt tên commit)

```
<type>(<scope>): <description>

feat: thêm tính năng mới
fix: sửa lỗi
docs: cập nhật tài liệu
style: format code (không đổi logic)
refactor: cải thiện code (không thêm feature, không fix bug)
test: thêm/sửa test
chore: cập nhật dependency, config
```

**Ví dụ:**
```
feat(auth): add Google OAuth login
fix(api): resolve null pointer in user endpoint
docs(readme): update installation guide
```

---

## .gitignore

File `.gitignore` khai báo những file/thư mục Git sẽ bỏ qua:

```gitignore
# Dependencies
node_modules/
.venv/
vendor/

# Build output
dist/
build/
*.pyc
__pycache__/

# Environment & secrets
.env
.env.local
*.key

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db
```

> 💡 Tham khảo template: [gitignore.io](https://www.toptal.com/developers/gitignore)

---

## Git Flow — Quy trình làm việc phổ biến

```
main (production)
  └── develop (integration)
        ├── feature/login
        ├── feature/payment
        └── hotfix/fix-crash
```

1. `main` — Code chạy trên production
2. `develop` — Tích hợp tất cả feature
3. `feature/*` — Phát triển từng tính năng
4. `hotfix/*` — Sửa lỗi khẩn cấp trên production

---

## Bài tập thực hành

- [ ] Tạo repo mới, thêm file, commit và push lên GitHub
- [ ] Tạo 2 nhánh, merge lại và giải quyết conflict
- [ ] Thực hành `git rebase` và so sánh với `git merge`
- [ ] Đóng góp vào 1 repo open source (tạo Pull Request đầu tiên)

---

## Tài nguyên thêm

- [Pro Git Book (free)](https://git-scm.com/book) — Sách chính thức, đầy đủ nhất
- [Learn Git Branching](https://learngitbranching.js.org/) — Học tương tác trực quan
- [Oh My Git!](https://ohmygit.org/) — Game học Git
