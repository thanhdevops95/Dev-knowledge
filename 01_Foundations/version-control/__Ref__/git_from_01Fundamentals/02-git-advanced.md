# Git Advanced

> **Tags:** `git` `rebase` `cherry-pick` `bisect` `hooks` `workflow`
> **Level:** Intermediate | **Prerequisite:** `git/01-git-basics.md`

---

## 1. Interactive Rebase

`git rebase -i` là công cụ mạnh nhất để làm sạch lịch sử trước khi merge/push.

```bash
# Rebase 5 commits cuối
git rebase -i HEAD~5

# Rebase từ ancestor (dùng khi muốn chỉnh tất cả commits từ điểm phân nhánh)
git rebase -i $(git merge-base HEAD main)
```

### Các lệnh trong interactive rebase
```
pick   abc1234 feat: add login page     ← giữ nguyên
reword def5678 fix typo                  ← giữ commit nhưng đổi message
edit   ghi9012 WIP stuff                 ← dừng lại để amend
squash jkl3456 more login stuff          ← gộp vào commit trước (giữ message)
fixup  mno7890 fix lint                  ← gộp vào commit trước (bỏ message)
drop   pqr1234 debug print               ← xóa commit này
exec   npm test                          ← chạy command sau mỗi commit
```

### Ví dụ thực tế: squash WIP commits
```bash
# Trước rebase: 4 commits WIP
# abc1234 WIP: login form
# def5678 WIP: fix validation
# ghi9012 WIP: cleanup
# jkl3456 WIP: add tests

git rebase -i HEAD~4
# Trong editor:
pick abc1234 WIP: login form
squash def5678 WIP: fix validation
squash ghi9012 WIP: cleanup
squash jkl3456 WIP: add tests

# Sau rebase: 1 commit gọn
# abc1234 feat: add login form with validation and tests
```

### ⚠️ Quy tắc vàng
**KHÔNG rebase commits đã push lên shared branch** — rebase thay đổi commit hashes, gây diverge cho người khác.

```bash
# Safe to rebase:
git rebase -i HEAD~5       # Chưa push
git rebase -i origin/main  # Local commits chưa push

# Nguy hiểm:
git push --force origin feature/login  # Chỉ dùng khi chắc chắn branch là của mình
git push --force-with-lease            # An toàn hơn: check xem có ai push mới không
```

---

## 2. Cherry-pick

Áp dụng 1 (hoặc nhiều) commit cụ thể từ branch khác:

```bash
# Cherry-pick 1 commit
git cherry-pick abc1234

# Cherry-pick range (không include abc1234, include def5678)
git cherry-pick abc1234..def5678

# Cherry-pick range (include cả abc1234)
git cherry-pick abc1234^..def5678

# Cherry-pick không tự commit (giữ changes ở staging)
git cherry-pick -n abc1234

# Cherry-pick với edit message
git cherry-pick -e abc1234
```

### Use cases
- **Hotfix**: fix bug trên `main`, cherry-pick vào release branch
- **Selective feature**: chỉ lấy 1 commit từ feature branch dang dở
- **Backport**: apply security patch cho version cũ hơn

```bash
# Hotfix workflow
git checkout main
git commit -m "fix: critical security bug" # SHA: abc1234
git checkout release/v2.1
git cherry-pick abc1234
git tag v2.1.1
git push origin release/v2.1 --tags
```

---

## 3. Git Bisect — Tìm Commit Gây Bug

`git bisect` dùng **binary search** trên lịch sử commits để tìm commit đầu tiên gây ra bug.

```bash
git bisect start
git bisect bad              # Commit hiện tại có bug
git bisect good v2.0.0      # Commit này OK (không có bug)

# Git tự checkout commit ở giữa
# Bạn test → nói cho git biết:
git bisect good    # Commit này OK
git bisect bad     # Commit này có bug

# Git tiếp tục binary search...
# Sau ~log2(n_commits) steps → tìm ra commit đầu tiên gây bug
# Ví dụ: 1000 commits → ~10 steps

git bisect reset   # Quay về HEAD ban đầu
```

### Tự động hóa với script
```bash
git bisect start HEAD v2.0.0
git bisect run npm test   # Chạy test: exit 0 = good, exit 1 = bad

# Hoặc script tùy chỉnh:
cat > test.sh << 'EOF'
#!/bin/bash
python -c "import mymodule; assert mymodule.feature_x() == expected"
EOF
git bisect run bash test.sh
```

---

## 4. Reflog — "Undo" Bất Cứ Điều Gì

`git reflog` ghi lại MỌI thay đổi của HEAD — kể cả rebase, reset, cherry-pick:

```bash
git reflog
# Kết quả:
# abc1234 HEAD@{0}: rebase -i (finish): returning to refs/heads/feature
# def5678 HEAD@{1}: rebase -i (squash): feat: add login
# ghi9012 HEAD@{2}: rebase -i (start): checkout abc1234
# jkl3456 HEAD@{3}: commit: WIP: add tests
# mno7890 HEAD@{4}: commit: WIP: cleanup

# Khôi phục commit bị xóa nhầm khi rebase
git reset --hard HEAD@{4}

# Hoặc checkout commit đó
git checkout mno7890
```

### Khôi phục sau `git reset --hard`
```bash
git reset --hard HEAD~3    # Oops! Xóa nhầm 3 commits!
git reflog                  # Tìm SHA trước khi reset
git reset --hard abc1234   # Khôi phục lại
```

---

## 5. Git Stash

```bash
git stash                          # Lưu working directory + index
git stash push -m "WIP: login"     # Lưu với message
git stash save --include-untracked # Bao gồm files chưa tracked
git stash list                     # Xem tất cả stashes
git stash pop                      # Apply stash mới nhất + xóa stash
git stash apply stash@{2}          # Apply stash cụ thể (giữ trong stash list)
git stash drop stash@{2}           # Xóa stash cụ thể
git stash clear                    # Xóa tất cả stashes
git stash branch new-feature       # Tạo branch mới từ stash
```

---

## 6. Submodules

Git submodule = repo 1 embedded trong repo khác, track 1 commit cụ thể:

```bash
# Thêm submodule
git submodule add https://github.com/user/lib.git libs/lib

# Clone repo có submodules
git clone --recurse-submodules https://github.com/user/main-repo

# Hoặc sau khi clone thông thường
git submodule init
git submodule update

# Update submodule lên commit mới nhất
git submodule update --remote

# Xóa submodule (phức tạp hơn add)
git submodule deinit libs/lib
git rm libs/lib
rm -rf .git/modules/libs/lib
```

### Nhược điểm submodules
- Dễ gây confusion cho team members
- `git clone` bình thường không get submodule content
- Thay thế: **git subtree**, **package managers (npm/pip/go modules)**

---

## 7. Pre-commit Hooks

Git hooks = scripts chạy tự động trước/sau git events:

```
.git/hooks/
├── pre-commit         ← chạy trước khi commit (lint, test)
├── commit-msg         ← validate commit message format
├── pre-push           ← chạy trước khi push (run tests)
├── post-merge         ← sau khi merge (npm install nếu package.json thay đổi)
└── prepare-commit-msg ← tự động thêm branch name vào commit message
```

### Dùng pre-commit tool (Python)
```bash
pip install pre-commit

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff           # Lint Python
      - id: ruff-format    # Format Python

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: detect-private-key   # Chặn commit private keys!

  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.20.0
    hooks:
      - id: commitizen         # Enforce conventional commits

pre-commit install            # Cài vào .git/hooks
pre-commit run --all-files    # Chạy thủ công trên tất cả files
```

### Self-written hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Không cho commit vào main trực tiếp
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$BRANCH" = "main" ]; then
    echo "❌ Direct commit to main is not allowed!"
    exit 1
fi

# Chạy lint
npm run lint
if [ $? -ne 0 ]; then
    echo "❌ Lint failed. Fix errors before committing."
    exit 1
fi

echo "✅ Pre-commit checks passed"
exit 0
```

---

## 8. .gitattributes

```gitattributes
# Auto-normalize line endings
*           text=auto

# Force LF cho shell scripts
*.sh        text eol=lf
*.py        text eol=lf

# Force CRLF cho Windows batch files  
*.bat       text eol=crlf

# Binary files — không diff, không merge
*.png       binary
*.jpg       binary
*.pdf       binary
*.zip       binary

# Custom diff driver
*.md        diff=markdown
```

---

## 9. Advanced Git Config

```bash
# ~/.gitconfig

[alias]
    # Shorthand
    st = status -sb
    co = checkout
    br = branch --sort=-committerdate
    
    # Pretty log
    lg = log --oneline --graph --decorate --all
    
    # Quick amend (không edit message)
    amend = commit --amend --no-edit
    
    # Undo last commit (giữ changes)
    undo = reset HEAD~1 --mixed
    
    # Wipe working directory
    wipe = !git add -A && git commit -qm 'WIPE SAVEPOINT' && git reset HEAD~1 --hard
    
    # Show files changed in last commit
    changed = show --stat --name-only

[core]
    editor = nvim
    pager = delta          # Better diff viewer
    
[diff]
    tool = vimdiff
    colorMoved = zebra     # Hiện moved code khác màu với changed code

[merge]
    conflictstyle = zdiff3  # Better conflict markers (shows base too)
    
[pull]
    rebase = true          # git pull = git fetch + git rebase (instead of merge)
    
[push]
    autoSetupRemote = true  # Auto set upstream on push

[rerere]
    enabled = true          # Remember resolved merge conflicts
```

---

## 10. Useful Advanced Commands

```bash
# Tìm ai đã viết dòng code này
git blame -L 42,60 src/main.py
git blame -w -C src/main.py   # ignore whitespace, detect code moved between files

# Tìm commit đã xóa function
git log -S "function_name" --all  # Pickaxe search
git log -G "regex" --all          # Regex search

# Xem diff giữa 2 branches
git diff main..feature/new
git diff main...feature/new  # Three dots: diff from common ancestor

# Tìm dangling commits (bị "mất")
git fsck --lost-found

# Compact repository (chạy garbage collection)
git gc --aggressive --prune=now

# Xem file ở commit cụ thể mà không checkout
git show abc1234:src/config.py

# Áp dụng 1 file từ branch khác
git checkout feature/new -- src/specific-file.py

# Thống kê code changes
git shortlog -sn --all        # Commits by author
git log --stat                # Files changed per commit
```

---

## 11. Git Internals (Hiểu để Debug)

```bash
# Git object types: blob (file), tree (directory), commit, tag
git cat-file -t abc1234       # Xem type của object
git cat-file -p abc1234       # Xem content của object

# Commits là immutable, linked list
# abc1234 → parent: def5678 → parent: ghi9012

# Branch là pointer đến commit
cat .git/refs/heads/main      # abc1234\n

# HEAD là pointer đến branch (hoặc commit trong detached HEAD)
cat .git/HEAD                 # ref: refs/heads/main
```

---

## 12. Cheatsheet

```bash
# Interactive rebase
git rebase -i HEAD~N              # Rebase N commits

# Cherry-pick
git cherry-pick <sha>             # Apply 1 commit
git cherry-pick <sha1>..<sha2>   # Apply range
git cherry-pick --abort           # Hủy cherry-pick

# Bisect
git bisect start; git bisect bad; git bisect good <tag>
git bisect run <test-script>
git bisect reset

# Reflog
git reflog                         # Xem lịch sử HEAD
git reset --hard HEAD@{N}          # Khôi phục

# Stash
git stash push -m "message"
git stash pop

# Hooks
pre-commit install
pre-commit run --all-files
```

---

*Tài liệu liên quan: `git/01-git-basics.md` | `git/03-git-workflows.md` | `git/04-github-gitlab.md`*
