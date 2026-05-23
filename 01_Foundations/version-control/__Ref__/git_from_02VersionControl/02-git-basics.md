# 🔀 Git cơ bản — Quản lý mã nguồn

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Kỹ năng đầu tiên mọi developer phải học

---

## Tại sao cần Git?

- **Lịch sử:** Quay lại bất kỳ phiên bản nào — giống "Save game" cho code
- **Cộng tác:** Nhiều người cùng sửa 1 dự án mà không đè code nhau
- **Nhánh:** Thử nghiệm tính năng mới mà không ảnh hưởng code chính

---

## 1. Cấu trúc Git

```
Working Directory ──► Staging Area ──► Local Repo ──► Remote Repo
   (thư mục code)     (git add)       (git commit)   (git push)

   Sửa file     →   Chọn file    →   Lưu snapshot  →  Đẩy lên server
   chưa track       chuẩn bị          vào lịch sử      (GitHub, GitLab)
```

---

## 2. Lệnh cơ bản

```bash
# === KHỞI TẠO ===
git init                           # Tạo repo mới
git clone https://github.com/user/repo.git  # Clone repo có sẵn

# === WORKFLOW HÀNG NGÀY ===
git status                         # Xem trạng thái files
git diff                           # Xem thay đổi chi tiết

git add file.js                    # Stage 1 file
git add .                          # Stage tất cả thay đổi

git commit -m "feat: thêm tính năng login"   # Commit
git commit -am "fix: sửa bug validation"     # Add + commit (files đã tracked)

git push                           # Đẩy lên remote
git pull                           # Kéo từ remote về (fetch + merge)

# === XEM LỊCH SỬ ===
git log --oneline                  # Lịch sử ngắn gọn
git log --graph --oneline --all    # Đồ thị nhánh đẹp
git show abc1234                   # Xem chi tiết 1 commit

# === HOÀN TÁC ===
git checkout -- file.js            # Bỏ thay đổi chưa stage
git restore file.js                # (Git 2.23+) Tương tự
git reset HEAD file.js             # Unstage file
git restore --staged file.js       # (Git 2.23+) Tương tự
git reset --soft HEAD~1            # Undo commit, giữ changes trong staging
git reset --hard HEAD~1            # ⚠️ Undo commit + XÓA changes!
git revert abc1234                 # Tạo commit đảo ngược (an toàn cho shared branch)
```

---

## 3. Branching — Nhánh

```bash
git branch                         # Liệt kê branches
git branch feature/login           # Tạo branch mới
git checkout feature/login         # Chuyển sang branch
git checkout -b feature/login      # Tạo + chuyển (1 lệnh)
git switch feature/login           # (Git 2.23+) Chuyển branch
git switch -c feature/login        # (Git 2.23+) Tạo + chuyển

git merge feature/login            # Merge branch vào branch hiện tại
git branch -d feature/login        # Xóa branch đã merge
git branch -D feature/login        # Xóa branch chưa merge (force)
```

```
main:     A ── B ── C ──────── F (merge commit)
                \              /
feature:         D ── E ──────
```

---

## 4. Merge vs Rebase

### Merge — Giữ lịch sử nguyên vẹn

```bash
git checkout main
git merge feature/login
# Tạo merge commit, giữ toàn bộ lịch sử
```

```
main:     A ── B ── C ──── M (merge commit)
                \         /
feature:         D ── E ──
```

### Rebase — Lịch sử sạch, thẳng hàng

```bash
git checkout feature/login
git rebase main
# "Di chuyển" commits của feature lên đầu main
```

```
Trước rebase:
main:     A ── B ── C
                \
feature:         D ── E

Sau rebase:
main:     A ── B ── C
                     \
feature:              D' ── E'   (commits mới, hash khác!)
```

> ⚠️ **Quy tắc vàng:** KHÔNG rebase branch đã push (shared branch)! Chỉ rebase branch cá nhân.

---

## 5. Xử lý Conflict

```bash
# Conflict xảy ra khi 2 người sửa cùng dòng
git merge feature/login
# Auto-merging file.js
# CONFLICT (content): Merge conflict in file.js

# Mở file — Git đánh dấu conflict:
<<<<<<< HEAD
console.log("Code trên main");
=======
console.log("Code trên feature");
>>>>>>> feature/login

# Fix: chọn code đúng, xóa markers
console.log("Code đã chọn");

# Đánh dấu đã resolve + commit
git add file.js
git commit -m "fix: resolve merge conflict"
```

---

## 6. Stash — Cất code tạm

```bash
# Đang code dở feature A, cần switch sang fix bug
git stash                          # Cất thay đổi hiện tại
git stash save "WIP: feature login"# Cất kèm message

git checkout hotfix/bug            # Switch sang branch khác
# ... fix bug, commit, push ...

git checkout feature/login         # Quay lại
git stash pop                      # Lấy lại code đã cất + xóa stash
git stash apply                    # Lấy lại nhưng KHÔNG xóa stash
git stash list                     # Xem danh sách stash
git stash drop stash@{0}           # Xóa 1 stash
```

---

## 7. .gitignore

```gitignore
# Dependencies
node_modules/
venv/
__pycache__/

# Build output
dist/
build/
*.o
*.exe

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
```

---

## 8. Commit Message Convention

```bash
# Format: <type>(<scope>): <description>

feat: thêm chức năng đăng nhập         # Feature mới
fix: sửa bug validation email           # Fix bug
docs: cập nhật README                    # Documentation
style: format code theo prettier         # Style (không đổi logic)
refactor: tách UserService thành modules # Refactor
test: thêm unit test cho auth           # Tests
chore: update dependencies              # Maintenance

# Breaking change
feat!: đổi API response format          # ! = breaking change

# Ví dụ đầy đủ
feat(auth): thêm đăng nhập Google OAuth

- Tích hợp Google OAuth 2.0
- Thêm callback route /auth/google/callback
- Lưu user vào database khi đăng nhập lần đầu

Closes #42
```

---

## 9. Git Flow vs Trunk-based

### Git Flow — Dự án release theo version

```
main ────────────────●──────────────────●── (production)
                    / \                / \
release ──────────●   ●──────────────●   │
                 /                        │
develop ──●──●──●──●──●──●──●──●──●──●───│
          \     /      \        /         │
feature    ●──●         ●──●──●           │
                                          │
hotfix ───────────────────────────────●───●
```

### Trunk-based — Deploy liên tục (CI/CD)

```
main ──●──●──●──●──●──●──●──●──●── (deploy từng commit)
       \  /  \  /      \  /
short   ●     ●         ●     (feature branches ngắn, <1 ngày)
```

---

## Các lỗi thường gặp

```
❌ Sai: git push --force trên shared branch → mất code người khác
✅ Đúng: Dùng git push --force-with-lease (an toàn hơn)

❌ Sai: Commit .env chứa secrets
✅ Đúng: Thêm .env vào .gitignore TRƯỚC commit đầu tiên

❌ Sai: Commit message "fix" hoặc "update" → không ai hiểu
✅ Đúng: Message rõ ràng: "fix(auth): sửa lỗi token expired"

❌ Sai: 1 commit chứa 10 thay đổi khác nhau
✅ Đúng: Mỗi commit 1 mục đích rõ ràng (atomic commits)
```

---

## Bài tập thực hành

- [ ] Tạo repo, thêm file, commit, push lên GitHub
- [ ] Tạo branch, sửa code, merge và xử lý conflict
- [ ] Dùng stash: cất code → switch branch → lấy lại
- [ ] Revert 1 commit sai bằng `git revert`

---

## Tài nguyên thêm

- [Git Cheat Sheet (GitHub)](https://education.github.com/git-cheat-sheet-education.pdf) — PDF tra cứu
- [Learn Git Branching](https://learngitbranching.js.org/) — Game tương tác cực hay
- [Oh Shit, Git!?!](https://ohshitgit.com/) — Sửa lỗi Git phổ biến
