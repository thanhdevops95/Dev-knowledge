# 📋 Git Cheatsheet — Tra cứu nhanh lệnh Git

> `[BEGINNER → ADVANCED]` — Bảng tổng hợp lệnh Git thường dùng nhất, xếp theo workflow.

---

## 1. Setup & Config

```bash
# Cài đặt thông tin user (bắt buộc sau khi cài Git)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Editor mặc định
git config --global core.editor "code --wait"    # VS Code
git config --global core.editor "vim"            # Vim

# Default branch name
git config --global init.defaultBranch main

# Xem toàn bộ config
git config --list --show-origin

# Aliases — tạo shortcut
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status
git config --global alias.lg "log --oneline --graph --all --decorate"
git config --global alias.last "log -1 HEAD"
```

---

## 2. Khởi tạo & Clone

```bash
# Tạo repo mới
git init
git init my-project      # Tạo folder + init

# Clone repo
git clone <url>
git clone <url> my-folder           # Clone vào folder cụ thể
git clone --depth 1 <url>           # Shallow clone (chỉ commit mới nhất)
git clone --branch dev <url>        # Clone branch cụ thể
git clone --recurse-submodules <url> # Clone + submodules
```

---

## 3. Staging & Commit

```bash
# Xem trạng thái
git status
git status -s          # Short format

# Stage files
git add <file>         # Stage 1 file
git add .              # Stage tất cả thay đổi
git add -p             # Stage interactive (chọn từng hunk)
git add -A             # Stage tất cả (including deleted)

# Unstage
git restore --staged <file>    # Unstage file (giữ changes)
git reset HEAD <file>          # Cách cũ (pre-2.23)

# Commit
git commit -m "message"
git commit -am "message"       # Stage tracked files + commit
git commit --amend             # Sửa commit cuối (message + files)
git commit --amend --no-edit   # Thêm files vào commit cuối, giữ message

# Discard changes
git restore <file>             # Discard changes in working dir
git checkout -- <file>         # Cách cũ
```

---

## 4. Branches

```bash
# Xem branches
git branch                     # Local branches
git branch -a                  # Tất cả (local + remote)
git branch -v                  # Với last commit

# Tạo & switch
git checkout -b feature/login  # Tạo + switch (cách cũ)
git switch -c feature/login    # Tạo + switch (cách mới, Git 2.23+)
git switch main                # Switch branch

# Rename
git branch -m old-name new-name
git branch -m new-name         # Rename current branch

# Delete
git branch -d feature/login    # Delete (đã merge)
git branch -D feature/login    # Force delete (chưa merge)
git push origin --delete feature/login  # Delete remote branch

# Track remote branch
git checkout --track origin/develop
```

---

## 5. Merge & Rebase

```bash
# Merge
git merge feature/login                # Merge branch vào current
git merge --no-ff feature/login        # Force merge commit
git merge --squash feature/login       # Squash all commits into 1
git merge --abort                      # Abort merge conflict

# Rebase
git rebase main                        # Rebase current onto main
git rebase -i HEAD~3                   # Interactive rebase 3 commits
git rebase --abort                     # Abort rebase
git rebase --continue                  # Continue after resolving conflict

# Interactive rebase commands:
# pick   = use commit
# reword = use commit, edit message
# squash = meld into previous commit
# fixup  = like squash, discard message
# drop   = remove commit
```

---

## 6. Remote

```bash
# Xem remotes
git remote -v

# Thêm remote
git remote add origin <url>
git remote add upstream <url>          # Fork workflow

# Fetch & Pull
git fetch                              # Download changes, don't merge
git fetch --all                        # Fetch all remotes
git pull                               # Fetch + merge
git pull --rebase                      # Fetch + rebase (cleaner)

# Push
git push                               # Push current branch
git push origin main                   # Push specific branch
git push -u origin feature/login       # Push + set upstream
git push --force-with-lease            # Safe force push
git push --tags                        # Push all tags

# Sync fork with upstream
git fetch upstream
git merge upstream/main
git push origin main
```

---

## 7. Stash — Tạm lưu thay đổi

```bash
git stash                     # Stash changes
git stash -m "WIP: login"     # Stash with message
git stash -u                  # Include untracked files
git stash list                # List all stashes
git stash pop                 # Apply + remove latest stash
git stash apply stash@{2}     # Apply specific stash (keep in list)
git stash drop stash@{0}      # Delete specific stash
git stash clear               # Delete all stashes
git stash show -p stash@{0}   # Show stash diff
```

---

## 8. Log & History

```bash
# Basic log
git log                        # Full log
git log --oneline              # One line per commit
git log --oneline --graph --all # Visual branch graph ⭐
git log -n 5                   # Last 5 commits
git log -p                     # Show diffs

# Filter log
git log --author="name"
git log --since="2024-01-01"
git log --until="2024-06-01"
git log --grep="fix"           # Search commit messages
git log -- <file>              # History of specific file
git log --follow -- <file>     # Even across renames

# Diff
git diff                       # Working dir vs staging
git diff --staged              # Staging vs last commit
git diff main..feature         # Between branches
git diff HEAD~3..HEAD          # Last 3 commits
git diff --stat                # Summary only

# Blame
git blame <file>               # Who changed each line
git blame -L 10,20 <file>      # Lines 10-20 only

# Show specific commit
git show <commit-hash>
git show HEAD~2                # 2 commits ago
```

---

## 9. Undo & Fix Mistakes

```bash
# ⚠️ MỨC ĐỘ NGUY HIỂM: Thấp → Cao

# Sửa commit message cuối
git commit --amend -m "new message"

# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Undo last commit, keep changes in working dir
git reset HEAD~1              # Mixed (default)

# Undo last commit, DISCARD changes ⚠️
git reset --hard HEAD~1

# Revert commit (tạo commit mới đảo ngược — safe cho shared branches)
git revert <commit-hash>
git revert HEAD               # Revert last commit

# Cherry-pick: lấy commit từ branch khác
git cherry-pick <commit-hash>
git cherry-pick <hash1> <hash2>  # Multiple commits

# Reflog: xem TOÀN BỘ history (kể cả đã reset/delete)
git reflog
git checkout <reflog-hash>     # Recover "lost" commits
```

---

## 10. Tags

```bash
# Tạo tag
git tag v1.0.0                        # Lightweight tag
git tag -a v1.0.0 -m "Release 1.0"    # Annotated tag (recommended)
git tag -a v1.0.0 <commit-hash>       # Tag specific commit

# Xem tags
git tag                               # List all tags
git tag -l "v1.*"                     # Filter tags
git show v1.0.0                       # Tag details

# Push tags
git push origin v1.0.0                # Push specific tag
git push --tags                       # Push all tags

# Delete tags
git tag -d v1.0.0                     # Delete local
git push origin --delete v1.0.0       # Delete remote
```

---

## 11. Advanced — Bisect, Worktree, Submodule

```bash
# Bisect: binary search for bug-introducing commit
git bisect start
git bisect bad                    # Current commit is bad
git bisect good <commit-hash>     # Last known good commit
# Git checks out middle commit → test → mark good/bad
git bisect good                   # or: git bisect bad
# Repeat until found
git bisect reset                  # Return to original state

# Worktree: multiple working dirs for same repo
git worktree add ../hotfix main   # New worktree from main
git worktree list
git worktree remove ../hotfix

# Submodule
git submodule add <url> path/to/submodule
git submodule update --init --recursive
git submodule foreach git pull origin main
```

---

## 12. .gitignore Patterns

```bash
# .gitignore
node_modules/         # Directory
*.log                 # All .log files
!important.log        # Exception: DO track this
dist/                 # Build output
.env                  # Environment variables
.env.local
*.pyc                 # Python bytecode
__pycache__/
.DS_Store             # macOS
Thumbs.db             # Windows
.idea/                # JetBrains IDE
.vscode/settings.json # VS Code (keep extensions.json)

# Global gitignore
git config --global core.excludesFile ~/.gitignore_global
```

---

## 13. Tips & Tricks

```bash
# Tìm commit đã delete file
git log --diff-filter=D -- <file-path>

# Khôi phục file đã delete
git checkout <commit-hash>^ -- <file-path>

# Clean untracked files
git clean -n          # Dry run (xem sẽ xóa gì)
git clean -fd         # Force delete untracked files + dirs

# Count lines of code changed
git diff --stat HEAD~10..HEAD

# Export repo as archive
git archive --format=zip HEAD -o project.zip

# Shallow clone → unshallow
git fetch --unshallow

# Search code in all commits
git log -S "function_name" --all

# Auto-correct typos
git config --global help.autocorrect 20  # 2 second delay
```

---

## 14. Conventional Commits

```bash
# Format: <type>(<scope>): <description>
feat(auth): add Google OAuth login
fix(api): handle null response from payment gateway
docs(readme): update installation instructions
style(ui): fix button alignment on mobile
refactor(db): extract query builder into service
test(auth): add unit tests for JWT validation
chore(deps): update express to v4.18.2
ci(actions): add Node 20 to test matrix
perf(query): add index for user_email lookup
build(docker): optimize multi-stage build

# Breaking change
feat(api)!: change response format for /users endpoint
```

---

## Tài nguyên thêm

- [Git Official Docs](https://git-scm.com/doc) — Reference đầy đủ
- [Oh Shit, Git!?!](https://ohshitgit.com/) — Cứu khi Git rối
- [Git Flight Rules](https://github.com/k88hudson/git-flight-rules) — FAQ kiểu "Tôi muốn..."
- [Conventional Commits](https://www.conventionalcommits.org/) — Chuẩn commit message
- [Learn Git Branching](https://learngitbranching.js.org/) — Interactive visual tutorial
