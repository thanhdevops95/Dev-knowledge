# 🔀 Git nâng cao — Workflows & Recovery

> `[INTERMEDIATE]` — Kỹ thuật Git cho team production

---

## 1. Interactive Rebase — Viết lại lịch sử

```bash
# Gộp 3 commits cuối thành 1 (squash)
git rebase -i HEAD~3

# Editor mở:
pick abc1234 feat: thêm login form
pick def5678 fix: sửa typo
pick ghi9012 style: format code

# Sửa thành:
pick abc1234 feat: thêm login form
squash def5678 fix: sửa typo
squash ghi9012 style: format code
# → 3 commits gộp thành 1 commit sạch

# Đổi thứ tự commits
pick ghi9012 style: format code
pick abc1234 feat: thêm login form

# Sửa commit message
reword abc1234 feat: thêm login form
# → Editor mở để sửa message

# Xóa commit
drop def5678 fix: sửa typo
```

---

## 2. Cherry-pick — Chọn commit cụ thể

```bash
# Lấy 1 commit từ branch khác
git cherry-pick abc1234

# Ví dụ: fix bug trên develop, cần đưa lên main ngay
git checkout main
git cherry-pick abc1234        # Chỉ lấy commit fix bug
git push origin main

# Cherry-pick nhiều commits
git cherry-pick abc1234 def5678

# Cherry-pick không auto-commit (review trước)
git cherry-pick --no-commit abc1234
```

---

## 3. Bisect — Tìm commit gây bug

```bash
# Bug xuất hiện, không biết commit nào gây ra
git bisect start
git bisect bad                   # Commit hiện tại có bug
git bisect good v1.0.0           # Commit cũ không bug

# Git checkout commit giữa → test
# Nếu có bug:
git bisect bad
# Nếu OK:
git bisect good

# Lặp lại → Git tìm ra exact commit gây bug!
# (Binary search: 1000 commits → chỉ cần ~10 bước)

git bisect reset                 # Quay lại branch gốc

# Tự động! (chạy script test)
git bisect start HEAD v1.0.0
git bisect run npm test          # Auto test mỗi commit
```

---

## 4. Worktrees — Nhiều branches cùng lúc

```bash
# Mở branch khác trong thư mục riêng (không cần stash!)
git worktree add ../hotfix-branch hotfix/bug-123

# Làm việc = 2 folders = 2 branches SONG SONG
# ../myproject     → feature/login
# ../hotfix-branch → hotfix/bug-123

# Xong → xóa worktree
git worktree remove ../hotfix-branch
```

---

## 5. Reflog — Cỗ máy thời gian

```bash
# Reflog ghi lại MỌI hành động (kể cả reset --hard!)
git reflog
# abc1234 HEAD@{0}: reset: moving to HEAD~3
# def5678 HEAD@{1}: commit: feat: important feature
# ghi9012 HEAD@{2}: commit: fix: bug fix

# Khôi phục commit đã "mất"
git reset --hard def5678         # Quay lại commit quan trọng!

# Khôi phục branch đã xóa
git branch recovered-branch HEAD@{5}
```

---

## 6. Advanced Merge Strategies

```bash
# Merge commit (default) — giữ lịch sử merge
git merge feature/login

# Squash merge — gộp tất cả commits thành 1
git merge --squash feature/login
git commit -m "feat: thêm tính năng login"
# ✅ History sạch, 1 commit rõ ràng

# Rebase merge — replay commits lên main
git checkout feature/login
git rebase main
git checkout main
git merge feature/login         # Fast-forward (thẳng hàng)

# Ours/Theirs — resolve conflict tự động
git merge -X ours feature        # Giữ code của mình
git merge -X theirs feature      # Lấy code của feature
```

---

## 7. Hooks — Tự động hóa

```bash
# .git/hooks/ hoặc dùng Husky (npm)

# Pre-commit: chạy lint trước commit
npx husky add .husky/pre-commit "npx lint-staged"

# Commit-msg: validate format
npx husky add .husky/commit-msg 'npx commitlint --edit "$1"'

# Pre-push: chạy tests trước push
npx husky add .husky/pre-push "npm test"
```

```json
// package.json — lint-staged
{
    "lint-staged": {
        "*.{js,ts,jsx,tsx}": ["eslint --fix", "prettier --write"],
        "*.{css,md,json}": ["prettier --write"]
    }
}
```

---

## 8. Git Aliases — Tăng tốc

```bash
# ~/.gitconfig
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    lg = log --graph --oneline --decorate --all
    unstage = reset HEAD --
    last = log -1 HEAD
    amend = commit --amend --no-edit
    wip = !git add -A && git commit -m "WIP"
    undo = reset --soft HEAD~1
    cleanup = !git branch --merged | grep -v main | xargs git branch -d
```

---

## Recovery Cheat Sheet

| Tình huống | Giải pháp |
|---|---|
| Commit sai branch | `git stash` → `git checkout correct` → `git stash pop` |
| Commit message sai | `git commit --amend -m "đúng"` |
| Quên thêm file vào commit | `git add file` → `git commit --amend --no-edit` |
| Push nhầm | `git revert HEAD` → `git push` (an toàn) |
| Reset --hard nhầm | `git reflog` → `git reset --hard HEAD@{n}` |
| Merge conflict quá phức tạp | `git merge --abort` → xử lý lại |
| Branch đã xóa | `git reflog` → `git branch recovery HEAD@{n}` |

---

## Bài tập thực hành

- [ ] Interactive rebase: squash 5 commits thành 2
- [ ] Cherry-pick: lấy 1 commit fix từ develop sang main
- [ ] Git bisect: tìm commit gây fail test trong 50 commits
- [ ] Setup Husky: pre-commit lint + pre-push test

---

## Tài nguyên thêm

- [Pro Git Book](https://git-scm.com/book/en/v2) — Free, comprehensive
- [Oh Shit, Git!?!](https://ohshitgit.com/) — Recovery guide
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules) — FAQ cho mọi tình huống
