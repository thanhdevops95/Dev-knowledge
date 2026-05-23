# Module 04: GIT & VERSION CONTROL

> **"Code không có Git như nhà không có móng - sụp bất cứ lúc nào"**

---

## 🎯 Mục tiêu

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu Git hoạt động như thế nào (internals)
- ✅ Thành thạo Git workflow hàng ngày
- ✅ Branching, merging, rebasing chuyên nghiệp
- ✅ Xử lý merge conflicts
- ✅ Pull Requests và Code Review
- ✅ Git hooks cho tự động hóa
- ✅ Gitflow và Trunk-based development
- ✅ Khôi phục và undo mistakes

---

## 📚 Thuật ngữ

| Thuật ngữ | Tiếng Anh | Nghĩa |
|-----------|-----------|-------|
| Repository | Repository (Repo) | Kho chứa code |
| Commit | Commit | Snapshot của thay đổi |
| Branch | Branch | Nhánh phát triển |
| Merge | Merge | Gộp branches |
| Rebase | Rebase | Chuyển base của branch |
| Pull | Git Pull | Kéo changes từ remote |
| Push | Git Push | Đẩy changes lên remote |
| Clone | Git Clone | Copy repo về local |
| Fork | Fork | Copy repo sang account khác |
| Remote | Remote | Repo ở server (origin) |
| HEAD | HEAD | Con trỏ tới commit hiện tại |
| Stash | Git Stash | Lưu tạm changes |
| Tag | Git Tag | Đánh dấu version |
| PR | Pull Request | Yêu cầu merge code |
| MR | Merge Request | GitLab gọi là MR |
| Conflict | Merge Conflict | Xung đột khi merge |
| Staging | Staging Area | Vùng chuẩn bị commit |

---

## ✅ Checklist Labs

### Labs Git cơ bản

- [ ] Lab 1: Git init và first commit
- [ ] Lab 2: Git status, diff, log
- [ ] Lab 3: Staging area - add, reset
- [ ] Lab 4: Commit message best practices
- [ ] Lab 5: .gitignore patterns

### Labs Remote & Collaboration

- [ ] Lab 6: Git remote - add, remove, rename
- [ ] Lab 7: Git clone, fetch, pull
- [ ] Lab 8: Git push - first push và subsequent
- [ ] Lab 9: Fork và upstream sync
- [ ] Lab 10: SSH keys setup cho GitHub/GitLab

### Labs Branching

- [ ] Lab 11: Create và switch branches
- [ ] Lab 12: Branch listing và management
- [ ] Lab 13: Delete local và remote branches
- [ ] Lab 14: Branch naming conventions

### Labs Merging

- [ ] Lab 15: Fast-forward merge
- [ ] Lab 16: Three-way merge
- [ ] Lab 17: Merge conflicts - detection
- [ ] Lab 18: Merge conflicts - resolution
- [ ] Lab 19: Merge strategies (ours, theirs)

### Labs Rebase & Advanced

- [ ] Lab 20: Git rebase cơ bản
- [ ] Lab 21: Interactive rebase (squash, edit, reorder)
- [ ] Lab 22: Rebase vs Merge - when to use
- [ ] Lab 23: Cherry-pick commits
- [ ] Lab 24: Git bisect - tìm bug

### Labs Undo & Recovery

- [ ] Lab 25: Git reset (soft, mixed, hard)
- [ ] Lab 26: Git revert
- [ ] Lab 27: Git reflog - recovery
- [ ] Lab 28: Recover deleted branch
- [ ] Lab 29: Amend last commit
- [ ] Lab 30: Git stash - save và apply

### Labs Workflows

- [ ] Lab 31: Gitflow workflow
- [ ] Lab 32: Trunk-based development
- [ ] Lab 33: Feature branch workflow
- [ ] Lab 34: Release branching

### Labs GitHub/GitLab

- [ ] Lab 35: Create Pull Request
- [ ] Lab 36: Code Review process
- [ ] Lab 37: Merge PR với squash
- [ ] Lab 38: Protected branches
- [ ] Lab 39: GitHub Actions basics (preview)

### Labs Git Hooks

- [ ] Lab 40: Pre-commit hook
- [ ] Lab 41: Commit-msg hook (format check)
- [ ] Lab 42: Pre-push hook
- [ ] Lab 43: Husky và lint-staged setup

### Labs Advanced

- [ ] Lab 44: Git submodules
- [ ] Lab 45: Git LFS (Large File Storage)
- [ ] Lab 46: Git blame và git log advanced
- [ ] Lab 47: Git worktree
- [ ] Lab 48: Signing commits với GPG

---

## 🚨 Checklist Scenarios

### Scenarios về Commits

- [ ] Scenario 1: Commit nhầm file secrets
- [ ] Scenario 2: Commit message sai, cần sửa
- [ ] Scenario 3: Commit vào wrong branch
- [ ] Scenario 4: Cần split 1 commit thành nhiều commits

### Scenarios về Branches

- [ ] Scenario 5: Branch outdated, cần update từ main
- [ ] Scenario 6: Delete branch nhầm
- [ ] Scenario 7: Branch diverged quá xa, khó merge

### Scenarios về Merge Conflicts

- [ ] Scenario 8: Same line edited by 2 people
- [ ] Scenario 9: File deleted vs modified
- [ ] Scenario 10: Binary file conflict
- [ ] Scenario 11: Merge conflict trong package-lock.json
- [ ] Scenario 12: Rebase conflict chain

### Scenarios về Recovery

- [ ] Scenario 13: Git reset --hard nhầm
- [ ] Scenario 14: Mất commits sau rebase
- [ ] Scenario 15: Force push ghi đè code người khác
- [ ] Scenario 16: Cần rollback production deployment

### Scenarios về Collaboration

- [ ] Scenario 17: PR conflicts cần update
- [ ] Scenario 18: Code review feedback implementation
- [ ] Scenario 19: Hotfix cần merge vào nhiều branches
- [ ] Scenario 20: Sync fork with upstream changes

### Scenarios về CI/CD Integration

- [ ] Scenario 21: Commit message không theo convention
- [ ] Scenario 22: Pre-commit hook fail
- [ ] Scenario 23: Branch protection block merge
- [ ] Scenario 24: Build failed on PR

---

## ⏱️ Thời lượng

**Ước tính:** 4-6 giờ

| Phần | Thời gian |
|------|-----------|
| Git cơ bản (Labs 1-10) | 1.5 giờ |
| Branching & Merging (Labs 11-24) | 2 giờ |
| Undo & Workflows (Labs 25-39) | 1.5 giờ |
| Advanced (Labs 40-48) | 1 giờ |
| Scenarios | 1 giờ |

---

## 🔗 Tài liệu tham khảo

- [Pro Git Book (Free)](https://git-scm.com/book/en/v2)
- [Learn Git Branching (Interactive)](https://learngitbranching.js.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📖 Nội dung

👉 **[Bắt đầu học: README.md](README.md)**
