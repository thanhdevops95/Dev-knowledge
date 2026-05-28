# 📋 Git & GitLab - Cheatsheet

> **Quick Reference for Git Commands**
>
> *Tra cứu nhanh các lệnh Git*

---

## 🚀 Basic Commands (Lệnh cơ bản)

```bash
git init                    # Initialize repository (Khởi tạo repo)
git clone <url>             # Clone repository (Clone repo)
git status                  # Check status (Kiểm tra trạng thái)
git add .                   # Stage all changes (Stage tất cả)
git commit -m "message"     # Commit changes (Commit thay đổi)
git push origin main        # Push to remote (Push lên remote)
git pull origin main        # Pull from remote (Pull từ remote)
```

---

## 🌿 Branching (Phân nhánh)

```bash
git branch                  # List branches (Liệt kê branches)
git branch feature-x        # Create branch (Tạo branch)
git checkout feature-x      # Switch branch (Chuyển branch)
git checkout -b feature-x   # Create and switch (Tạo và chuyển)
git switch -c feature-x     # Modern syntax (Cú pháp mới)
git merge feature-x         # Merge branch (Hợp nhất branch)
git branch -d feature-x     # Delete branch (Xóa branch)
```

---

## ↩️ Undo Changes (Hoàn tác)

```bash
git restore file.txt        # Discard changes (Bỏ thay đổi)
git restore --staged file   # Unstage file (Bỏ stage)
git reset --soft HEAD~1     # Undo commit, keep changes (Giữ changes)
git reset --hard HEAD~1     # Undo commit, delete changes (Xóa changes)
git revert <commit>         # Create reverse commit (Tạo commit ngược)
```

---

## 📜 History (Lịch sử)

```bash
git log                     # Full log (Log đầy đủ)
git log --oneline           # Compact log (Log gọn)
git log --graph             # With graph (Có biểu đồ)
git diff                    # Show changes (Xem thay đổi)
git show <commit>           # Show commit details (Chi tiết commit)
```

---

## 🔗 Remote - GitLab/GitHub

```bash
# GitLab (Primary - Chính)
git remote add origin git@gitlab.com:user/repo.git
ssh -T git@gitlab.com       # Test connection (Kiểm tra kết nối)

# GitHub (Alternative - Thay thế)
git remote add origin git@github.com:user/repo.git
ssh -T git@github.com       # Test connection (Kiểm tra kết nối)

# Remote management (Quản lý remote)
git remote -v               # List remotes (Liệt kê remotes)
git remote set-url origin <url>  # Change URL (Đổi URL)
```

---

## 🏷️ Tags

```bash
git tag v1.0.0              # Create tag (Tạo tag)
git tag -a v1.0.0 -m "msg"  # Annotated tag (Tag có chú thích)
git push origin v1.0.0      # Push tag (Push tag)
git push origin --tags      # Push all tags (Push tất cả tags)
```

---

## 🔗 Navigation

| ← Previous | Current | Next → |
|------------|---------|--------|
| [README](./README.md) | **Cheatsheet** | [LABS](./LABS.md) |

---

*Last Updated: 2025-12-30*
