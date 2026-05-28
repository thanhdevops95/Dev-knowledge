# Git Commands Cheatsheet (Quick Reference -- Tra cứu Nhanh)

> Commonly used Git commands for quick reference -- Các lệnh Git thường dùng để tra cứu nhanh

## 📋 Table of Contents -- Mục lục

- [Setup & Config](#setup--config) -- Cài đặt & Cấu hình
- [Basic Commands](#basic-commands) -- Lệnh Cơ bản
- [Branching](#branching) -- Nhánh
- [Remote](#remote) -- Remote
- [Stash](#stash) -- Stash
- [History & Diff](#history--diff) -- Lịch sử & Diff
- [Undo Changes](#undo-changes) -- Hoàn tác Thay đổi
- [Tags](#tags) -- Tags
- [Advanced](#advanced) -- Nâng cao
- [Common Workflows](#common-workflows) -- Workflows Thường dùng

## <a id="setup--config"></a> Setup & Config -- Cài đặt & Cấu hình

```bash
# Configure user -- Cấu hình người dùng
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# View config -- Xem cấu hình
git config --list
git config user.name

# Set default editor -- Đặt editor mặc định
git config --global core.editor "vim"

# Set default branch name -- Đặt tên nhánh mặc định
git config --global init.defaultBranch main

# Aliases -- Bí danh
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
```

## <a id="basic-commands"></a> Basic Commands -- Lệnh Cơ bản

```bash
# Initialize -- Khởi tạo
git init                     # Initialize new repo -- Khởi tạo repo mới
git clone URL                # Clone repository -- Clone repository
git clone URL dirname        # Clone to specific directory -- Clone đến thư mục cụ thể

# Status & Info -- Trạng thái & Thông tin
git status                   # Working tree status -- Trạng thái working tree
git status -s                # Short status -- Trạng thái ngắn gọn
git log                      # Commit history -- Lịch sử commit
git log --oneline            # Compact log -- Log ngắn gọn
git log --graph --oneline    # Visual graph -- Đồ thị trực quan
git show commit_hash         # Show commit details -- Hiển thị chi tiết commit

# Add & Commit -- Thêm & Commit
git add file.txt             # Stage specific file -- Stage file cụ thể
git add .                    # Stage all changes -- Stage tất cả thay đổi
git add -A                   # Stage all (including deleted) -- Stage tất cả (bao gồm đã xóa)
git add -p                   # Interactive staging -- Staging tương tác

git commit -m "message"      # Commit with message -- Commit với message
git commit -am "message"     # Add and commit (tracked files) -- Add và commit (files đã track)
git commit --amend           # Amend last commit -- Sửa commit cuối
git commit --amend --no-edit # Amend without changing message -- Sửa không đổi message

# Diff
git diff                     # Unstaged changes -- Thay đổi chưa stage
git diff --staged            # Staged changes -- Thay đổi đã stage
git diff branch1 branch2     # Compare branches -- So sánh nhánh
git diff commit1 commit2     # Compare commits -- So sánh commits
```

## <a id="branching"></a> Branching -- Nhánh

```bash
# List branches -- Liệt kê nhánh
git branch                   # Local branches -- Nhánh local
git branch -r                # Remote branches -- Nhánh remote
git branch -a                # All branches -- Tất cả nhánh
git branch -v                # With last commit -- Với commit cuối

# Create branch -- Tạo nhánh
git branch branch_name       # Create branch -- Tạo nhánh
git checkout -b branch_name  # Create and switch -- Tạo và chuyển
git switch -c branch_name    # Create and switch (newer) -- Tạo và chuyển (mới hơn)

# Switch branch -- Chuyển nhánh
git checkout branch_name     # Switch branch -- Chuyển nhánh
git switch branch_name       # Switch (newer syntax) -- Chuyển (cú pháp mới)

# Merge -- Merge
git merge branch_name        # Merge branch into current -- Merge nhánh vào nhánh hiện tại
git merge --no-ff branch_name  # No fast-forward -- Không fast-forward
git merge --squash branch_name # Squash commits -- Gộp commits

# Delete branch -- Xóa nhánh
git branch -d branch_name    # Delete merged branch -- Xóa nhánh đã merge
git branch -D branch_name    # Force delete -- Xóa cưỡng chế
git push origin --delete branch_name  # Delete remote branch -- Xóa nhánh remote

# Rename branch -- Đổi tên nhánh
git branch -m old_name new_name  # Rename branch -- Đổi tên nhánh
git branch -m new_name       # Rename current branch -- Đổi tên nhánh hiện tại
```

## <a id="remote"></a> Remote

```bash
# View remotes -- Xem remotes
git remote                   # List remotes -- Liệt kê remotes
git remote -v                # With URLs -- Với URLs
git remote show origin       # Detailed info -- Thông tin chi tiết

# Add/Remove remote -- Thêm/Xóa remote
git remote add origin URL    # Add remote -- Thêm remote
git remote remove origin     # Remove remote -- Xóa remote
git remote rename old new    # Rename remote -- Đổi tên remote

# Fetch & Pull
git fetch                    # Fetch from remote -- Fetch từ remote
git fetch origin             # Fetch from specific remote -- Fetch từ remote cụ thể
git pull                     # Fetch and merge -- Fetch và merge
git pull --rebase            # Fetch and rebase -- Fetch và rebase
git pull origin main         # Pull specific branch -- Pull nhánh cụ thể

# Push
git push                     # Push to remote -- Push lên remote
git push origin main         # Push to specific branch -- Push lên nhánh cụ thể
git push -u origin main      # Set upstream and push -- Đặt upstream và push
git push --force             # Force push (dangerous!) -- Force push (nguy hiểm!)
git push --force-with-lease  # Safer force push -- Force push an toàn hơn
git push --all               # Push all branches -- Push tất cả nhánh
git push --tags              # Push all tags -- Push tất cả tags
```

## <a id="stash"></a> Stash

```bash
# Stash changes -- Stash thay đổi
git stash                    # Stash changes -- Stash thay đổi
git stash save "message"     # Stash with message -- Stash với message
git stash -u                 # Include untracked files -- Bao gồm files chưa track
git stash -a                 # Include all files -- Bao gồm tất cả files

# List stashes -- Liệt kê stashes
git stash list               # List all stashes -- Liệt kê tất cả stashes

# Apply stash -- Áp dụng stash
git stash apply              # Apply latest stash -- Áp dụng stash mới nhất
git stash apply stash@{2}    # Apply specific stash -- Áp dụng stash cụ thể
git stash pop                # Apply and remove latest -- Áp dụng và xóa stash mới nhất
git stash pop stash@{2}      # Apply and remove specific -- Áp dụng và xóa stash cụ thể

# Remove stash -- Xóa stash
git stash drop               # Remove latest stash -- Xóa stash mới nhất
git stash drop stash@{2}     # Remove specific stash -- Xóa stash cụ thể
git stash clear              # Remove all stashes -- Xóa tất cả stashes

# Show stash -- Hiển thị stash
git stash show               # Show latest stash -- Hiển thị stash mới nhất
git stash show -p            # Show with diff -- Hiển thị với diff
git stash show stash@{2}     # Show specific stash -- Hiển thị stash cụ thể
```

## <a id="history--diff"></a> History & Diff -- Lịch sử & Diff

```bash
# Log
git log                      # Full log -- Log đầy đủ
git log --oneline            # Compact -- Ngắn gọn
git log --graph              # Graph view -- Xem dạng đồ thị
git log --all --graph --oneline  # All branches graph -- Đồ thị tất cả nhánh
git log -n 5                 # Last 5 commits -- 5 commits cuối
git log --since="2 weeks ago"  # Time filter -- Lọc theo thời gian
git log --author="Name"      # By author -- Theo tác giả
git log --grep="keyword"     # Search commit messages -- Tìm kiếm commit messages
git log file.txt             # File history -- Lịch sử file
git log -p file.txt          # With diffs -- Với diffs

# Show -- Hiển thị
git show commit_hash         # Show commit -- Hiển thị commit
git show HEAD                # Show latest commit -- Hiển thị commit mới nhất
git show HEAD~2              # Show 2 commits ago -- Hiển thị commit 2 lần trước
git show branch:file.txt     # Show file from branch -- Hiển thị file từ nhánh

# Blame
git blame file.txt           # Who changed what -- Ai thay đổi gì
git blame -L 10,20 file.txt  # Specific lines -- Dòng cụ thể
```

## <a id="undo-changes"></a> Undo Changes -- Hoàn tác Thay đổi

```bash
# Discard changes -- Hủy thay đổi
git checkout -- file.txt     # Discard unstaged changes -- Hủy thay đổi chưa stage
git restore file.txt         # Discard changes (newer) -- Hủy thay đổi (mới hơn)
git restore --staged file.txt  # Unstage file -- Unstage file
git reset HEAD file.txt      # Unstage file (older) -- Unstage file (cũ hơn)

# Reset commits -- Reset commits
git reset --soft HEAD~1      # Undo commit, keep changes staged -- Hoàn tác commit, giữ thay đổi đã stage
git reset --mixed HEAD~1     # Undo commit, keep changes unstaged -- Hoàn tác commit, giữ thay đổi chưa stage
git reset --hard HEAD~1      # Undo commit, discard changes -- Hoàn tác commit, hủy thay đổi

# Revert
git revert commit_hash       # Create new commit that undoes -- Tạo commit mới hoàn tác
git revert HEAD              # Revert last commit -- Hoàn tác commit cuối
git revert --no-commit HEAD~3..HEAD  # Revert multiple -- Hoàn tác nhiều commits

# Clean -- Dọn dẹp
git clean -n                 # Dry run (show what will be deleted) -- Chạy thử (hiển thị sẽ xóa gì)
git clean -f                 # Remove untracked files -- Xóa files chưa track
git clean -fd                # Remove untracked files and directories -- Xóa files và thư mục chưa track
git clean -fx                # Include ignored files -- Bao gồm files bị ignore
```

## <a id="tags"></a> Tags

```bash
# List tags -- Liệt kê tags
git tag                      # List all tags -- Liệt kê tất cả tags
git tag -l "v1.*"           # Filter tags -- Lọc tags

# Create tag -- Tạo tag
git tag v1.0.0              # Lightweight tag -- Lightweight tag
git tag -a v1.0.0 -m "Version 1.0.0"  # Annotated tag -- Annotated tag
git tag v1.0.0 commit_hash  # Tag specific commit -- Tag commit cụ thể

# Push tags -- Push tags
git push origin v1.0.0      # Push specific tag -- Push tag cụ thể
git push origin --tags      # Push all tags -- Push tất cả tags

# Delete tag -- Xóa tag
git tag -d v1.0.0           # Delete local tag -- Xóa tag local
git push origin --delete v1.0.0  # Delete remote tag -- Xóa tag remote

# Checkout tag -- Checkout tag
git checkout v1.0.0         # Checkout tag -- Checkout tag
```

## <a id="advanced"></a> Advanced -- Nâng cao

```bash
# Rebase
git rebase main             # Rebase current branch onto main -- Rebase nhánh hiện tại lên main
git rebase -i HEAD~3        # Interactive rebase last 3 commits -- Rebase tương tác 3 commits cuối
git rebase --continue       # Continue after resolving conflicts -- Tiếp tục sau khi giải quyết conflicts
git rebase --abort          # Abort rebase -- Hủy rebase

# Cherry-pick
git cherry-pick commit_hash # Apply specific commit -- Áp dụng commit cụ thể
git cherry-pick commit1 commit2  # Multiple commits -- Nhiều commits

# Reflog
git reflog                  # Show reference log -- Hiển thị reference log
git reflog show branch_name # Branch reflog -- Reflog của nhánh

# Bisect (find bug) -- Bisect (tìm bug)
git bisect start            # Start bisect -- Bắt đầu bisect
git bisect bad              # Mark current as bad -- Đánh dấu hiện tại là bad
git bisect good commit_hash # Mark commit as good -- Đánh dấu commit là good
git bisect reset            # End bisect -- Kết thúc bisect

# Submodules
git submodule add URL path  # Add submodule -- Thêm submodule
git submodule init          # Initialize submodules -- Khởi tạo submodules
git submodule update        # Update submodules -- Cập nhật submodules
git submodule update --remote  # Update to latest -- Cập nhật lên mới nhất

# Worktree
git worktree add ../path branch  # Create worktree -- Tạo worktree
git worktree list           # List worktrees -- Liệt kê worktrees
git worktree remove path    # Remove worktree -- Xóa worktree
```

## <a id="common-workflows"></a> Common Workflows -- Workflows Thường dùng

```bash
# Feature branch workflow -- Workflow nhánh feature
git checkout -b feature/new-feature
# ... make changes -- thực hiện thay đổi ...
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
# ... create pull request -- tạo pull request ...

# Fix merge conflict -- Sửa merge conflict
git pull origin main
# ... resolve conflicts in files -- giải quyết conflicts trong files ...
git add .
git commit -m "Resolve merge conflicts"
git push

# Undo last commit but keep changes -- Hoàn tác commit cuối nhưng giữ thay đổi
git reset --soft HEAD~1

# Squash last 3 commits -- Gộp 3 commits cuối
git rebase -i HEAD~3
# Change 'pick' to 'squash' for commits to squash -- Đổi 'pick' thành 'squash' cho commits cần gộp

# Update fork -- Cập nhật fork
git remote add upstream URL
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---
