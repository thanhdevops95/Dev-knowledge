# Module 02: GIT & GITHUB - Version Control Mastery

> **Thời gian học:** 1-2 tuần
>
> **Prerequisite:** Module 01 (Linux Basics)
>
> **Difficulty:** ⭐⭐⭐☆☆

---

## 📋 Mục lục

1. [Version Control là gì?](#1-version-control-là-gì)
2. [Git Fundamentals](#2-git-fundamentals)
3. [Git Internals](#3-git-internals)
4. [Branching & Merging](#4-branching--merging)
5. [Remote Repositories](#5-remote-repositories)
6. [GitHub Essentials](#6-github-essentials)
7. [Collaboration Workflows](#7-collaboration-workflows)
8. [Best Practices](#8-best-practices)
9. [Troubleshooting](#9-troubleshooting)

---

## 🎯 Learning Objectives

Sau khi hoàn thành module này, bạn sẽ:

- ✅ Hiểu **tại sao cần Version Control** và các loại VCS
- ✅ Master **Git basics:** init, add, commit, push, pull
- ✅ Hiểu **Git internals:** objects, refs, HEAD
- ✅ Thành thạo **branching & merging strategies**
- ✅ Làm việc với **remote repositories** (GitHub)
- ✅ Sử dụng **Pull Requests** cho collaboration
- ✅ Resolve **merge conflicts** một cách tự tin
- ✅ Apply **Git workflows** cho team projects

---

## 1. Version Control là gì?

### 1.1. Vấn đề không có Version Control

**Scenario: Phát triển phần mềm không có VCS**

```
project/
├── app.py
├── app_backup.py
├── app_final.py
├── app_final_v2.py
├── app_really_final.py
├── app_really_final_fixed.py
└── app_use_this_one.py
```

**Problems:**

- ❌ Không biết version nào đang dùng
- ❌ Không biết ai đã thay đổi gì, khi nào
- ❌ Không thể rollback về version cũ dễ dàng
- ❌ Khó collaborate: "Đừng edit file này, tôi đang sửa!"
- ❌ Mất công backup manual

**Email collaboration nightmare:**

```
From: Alice
To: Bob
Subject: RE: RE: FW: Code update

Attached: app_v5_alice_fixes.zip

Bob, tôi đã fix bug login. Nhưng đừng merge code của 
bạn vào vì tôi cũng sửa function đó. Hãy đợi tôi 
xong rồi bạn làm tiếp...
```

### 1.2. Version Control System Benefits

**VCS giải quyết:**

- ✅ **History:** Mọi thay đổi được ghi lại
- ✅ **Collaboration:** Nhiều người cùng làm parallel
- ✅ **Backup:** Distributed copies
- ✅ **Branching:** Thử nghiệm mà không ảnh hưởng code chính
- ✅ **Rollback:** Quay về version cũ bất kỳ lúc nào

**With Git:**

```bash
# Xem history
git log

# Ai đã sửa dòng này?
git blame app.py

# Quay về commit 3 ngày trước
git checkout abc123

# Multiple people edit cùng file
# Git tự động merge (hoặc báo conflict để resolve)
```

### 1.3. Types of VCS

#### Centralized VCS (CVCS)

**Examples:** SVN (Subversion), Perforce, CVS

**Architecture:**

```
        Central Server
             │
    ┌────────┼────────┐
    │        │        │
  Alice    Bob    Charlie
  (copy)  (copy)  (copy)
```

**Workflow:**

1. Checkout code from central server
2. Make changes locally
3. Commit back to server

**Pros:**

- ✅ Simple model
- ✅ Fine-grained access control

**Cons:**

- ❌ Single point of failure (server down = no work)
- ❌ Slow (every operation needs server)
- ❌ No offline commits

#### Distributed VCS (DVCS)

**Examples:** Git, Mercurial

**Architecture:**

```
     GitHub (Remote)
           │
    ┌──────┼──────┐
    │      │      │
  Alice   Bob  Charlie
  (full) (full) (full)
  clone  clone  clone
```

**Workflow:**

1. Clone entire repository (full history)
2. Work offline, commit locally
3. Push to remote when ready

**Pros:**

- ✅ Fast (most operations local)
- ✅ Offline work
- ✅ Every clone is a backup
- ✅ Flexible workflows

**Cons:**

- ❌ Steeper learning curve
- ❌ Large repos can be slow to clone

**Why Git won:**

- **Performance:** Extremely fast
- **Branching:** Cheap and easy
- **Open Source:** Free, Linux kernel uses it
- **GitHub:** Hosting + social coding platform

---

## 2. Git Fundamentals

### 2.1. Git Basics

#### What is Git?

**Git** = Distributed Version Control System created by Linus Torvalds (2005)

**Philosophy:**

- **Content-addressable filesystem:** Data là nội dung, không phải tên file
- **Snapshots, not diffs:** Mỗi commit = full snapshot, không phải delta
- **Cryptographic integrity:** SHA-1 hashes ensure data integrity

#### Three States

**Files trong Git có 3 states:**

```
Working Directory → Staging Area → Repository
   (modified)       (staged)       (committed)

    [edit]    →    [git add]  →   [git commit]
```

**1. Working Directory:**

- Files bạn đang edit
- Untracked hoặc modified

**2. Staging Area (Index):**

- Files ready to commit
- "Preparing the next snapshot"

**3. Repository (.git directory):**

- Committed history
- Permanent record

**Example:**

```bash
# Edit file (Working Directory)
echo "Hello Git" > file.txt

# Stage file (Staging Area)
git add file.txt

# Commit (Repository)
git commit -m "Add file.txt"
```

### 2.2. Basic Commands

#### `git init` - Initialize Repository

```bash
# Create new repo
mkdir my-project
cd my-project
git init

# Output:
# Initialized empty Git repository in /path/to/my-project/.git/
```

**What happens:**

- Creates `.git/` directory
- Contains all Git metadata

#### `git clone` - Copy Remote Repository

```bash
# Clone from GitHub
git clone https://github.com/user/repo.git

# Clone to specific folder
git clone https://github.com/user/repo.git my-folder

# Clone specific branch
git clone -b develop https://github.com/user/repo.git
```

#### `git status` - Check State

```bash
git status

# Output example:
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   file.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        newfile.txt
```

#### `git add` - Stage Changes

```bash
# Stage specific file
git add file.txt

# Stage all changes
git add .

# Stage all .py files
git add *.py

# Interactive staging
git add -p  # Patch mode, choose hunks
```

#### `git commit` - Save Snapshot

```bash
# Commit with message
git commit -m "Add login feature"

# Commit with detailed message
git commit -m "Add login feature" -m "Implemented OAuth2 authentication"

# Stage and commit in one step (tracked files only)
git commit -am "Fix bug in logout"

# Open editor for commit message
git commit
```

**Good commit messages:**

```
✅ Add user authentication
✅ Fix null pointer exception in login
✅ Refactor database connection pooling

❌ Update
❌ Fix stuff
❌ Changes
```

#### `git log` - View History

```bash
# Full log
git log

# One line per commit
git log --oneline

# Graph view (shows branches)
git log --oneline --graph --all

# Last 5 commits
git log -5

# Commits by author
git log --author="Alice"

# Commits in date range
git log --since="2 weeks ago"

# Files changed in each commit
git log --stat
```

#### `git diff` - Show Changes

```bash
# Unstaged changes
git diff

# Staged changes
git diff --staged

# Compare branches
git diff main..develop

# Compare commits
git diff abc123..def456
```

---

## 3. Git Internals

### 3.1. Git Objects

**Git stores everything as objects:**

#### 1. Blob (Binary Large Object)

**Stores file contents**

```bash
# Create file
echo "Hello Git" > file.txt

# Git stores contents as blob
git add file.txt
git commit -m "Add file"

# View blob
git cat-file -p <blob-hash>
# Output: Hello Git
```

#### 2. Tree

**Stores directory structure**

```bash
# Tree object contains:
# - Blob references (files)
# - Tree references (subdirectories)
# - File permissions

# View tree
git cat-file -p <tree-hash>
# Output:
# 100644 blob a906cb...  file.txt
# 040000 tree b8ef5a...  folder/
```

#### 3. Commit

**Stores commit metadata**

```bash
# Commit object contains:
# - Tree reference (snapshot)
# - Parent commit(s)
# - Author & committer
# - Timestamp
# - Commit message

# View commit
git cat-file -p HEAD
# Output:
# tree 4b825dc...
# parent a1b2c3d...
# author Alice <alice@example.com> 1703500000 +0700
# committer Alice <alice@example.com> 1703500000 +0700
#
# Add login feature
```

#### 4. Tag

**Stores release points**

```bash
# Lightweight tag (pointer to commit)
git tag v1.0

# Annotated tag (object with metadata)
git tag -a v1.0 -m "Release version 1.0"
```

### 3.2. References (Refs)

**Pointers to commits:**

```
.git/refs/
├── heads/              # Local branches
│   ├── main
│   └── develop
├── remotes/            # Remote branches
│   └── origin/
│       ├── main
│       └── develop
└── tags/               # Tags
    └── v1.0
```

**Special refs:**

```bash
HEAD                    # Current branch/commit
ORIG_HEAD               # Previous HEAD (before dangerous operation)
FETCH_HEAD              # Last fetched branch
MERGE_HEAD              # Commit being merged
```

**View refs:**

```bash
# Show HEAD
cat .git/HEAD
# Output: ref: refs/heads/main

# Show branch commit
cat .git/refs/heads/main
# Output: a1b2c3d4e5f6...
```

### 3.3. Index (Staging Area)

**Binary file `.git/index`:**

- Tracks staged files
- File metadata (path, mode, hash)
- Prepared for next commit

**View index:**

```bash
git ls-files --stage

# Output:
# 100644 a906cb... 0   file.txt
# 100644 b8ef5a... 0   folder/another.txt
```

---

## 4. Branching & Merging

### 4.1. Branches Concept

**Branch = Movable pointer to commits**

```
main:      A---B---C
                    ↑
                  HEAD
```

**Create branch:**

```
main:      A---B---C
                    ↑
                  main

feature:   A---B---C
                    ↑
                  feature, HEAD
```

**Work on branch:**

```
main:      A---B---C

feature:   A---B---C---D---E
                            ↑
                          feature, HEAD
```

### 4.2. Branch Commands

```bash
# List branches
git branch

# Create branch
git branch feature-login

# Switch branch
git checkout feature-login
# Or (newer syntax):
git switch feature-login

# Create and switch in one command
git checkout -b feature-login
# Or:
git switch -c feature-login

# Delete branch
git branch -d feature-login

# Force delete (unmerged changes)
git branch -D feature-login

# Rename branch
git branch -m old-name new-name
```

### 4.3. Merging Strategies

#### Fast-Forward Merge

**When target branch has no new commits:**

```
Before:
main:      A---B
feature:   A---B---C---D
                        ↑
                      feature

After merge:
main:      A---B---C---D
                        ↑
                    main, feature
```

**Command:**

```bash
git checkout main
git merge feature-login

# Output:
# Fast-forward
#  file.txt | 1 +
#  1 file changed, 1 insertion(+)
```

#### Three-Way Merge

**When both branches have new commits:**

```
Before:
         C---D  (feature)
        /
    A---B
         \
          E---F  (main)

After merge:
         C---D
        /     \
    A---B      G  (merge commit)
         \    /
          E--F
```

**Command:**

```bash
git checkout main
git merge feature-login

# Git creates merge commit G
# Merge commit has 2 parents: F and D
```

#### Rebase

**Rewrite history to linear:**

```
Before:
         C---D  (feature)
        /
    A---B---E---F  (main)

After rebase:
                C'--D'  (feature, rebased)
               /
    A---B---E---F  (main)
```

**Command:**

```bash
git checkout feature
git rebase main

# Replays C, D on top of F
# C', D' are new commits (different hashes)
```

**Merge vs Rebase:**

| Aspect | Merge | Rebase |
|--------|-------|--------|
| **History** | Preserves exact history | Rewrites history |
| **Graph** | Shows parallel work | Linear |
| **Use case** | Public branches | Local cleanup |
| **Safety** | Safe (no rewrite) | Dangerous on public branches |

**Golden rule:** Never rebase public/shared branches!

### 4.4. Merge Conflicts

**Happens when:**

- Same lines edited in both branches
- File deleted in one, modified in other

**Example conflict:**

```bash
git merge feature

# Output:
# Auto-merging file.txt
# CONFLICT (content): Merge conflict in file.txt
# Automatic merge failed; fix conflicts and then commit the result.
```

**Conflict markers in file:**

```
Normal content here...

<<<<<<< HEAD (current branch)
This is from main branch
=======
This is from feature branch
>>>>>>> feature

More normal content...
```

**Resolve:**

```bash
# 1. Edit file, choose version:
# - Keep HEAD version
# - Keep incoming version  
# - Combine both
# - Write completely new

# 2. Remove conflict markers (<<<, ===, >>>)

# Example resolved:
This is combined from both branches

# 3. Stage resolved file
git add file.txt

# 4. Complete merge
git commit -m "Merge feature into main"
```

**Or use tools:**

```bash
# Visual merge tool
git mergetool

# VS Code, Sublime Merge, GitKraken have built-in conflict resolution
```

---

## 5. Remote Repositories

### 5.1. Remote Basics

**Remote = URL to another repository**

```bash
# View remotes
git remote -v

# Output:
# origin  https://github.com/user/repo.git (fetch)
# origin  https://github.com/user/repo.git (push)
```

**Add remote:**

```bash
git remote add origin https://github.com/user/repo.git
```

**Remove remote:**

```bash
git remote remove origin
```

**Rename remote:**

```bash
git remote rename origin upstream
```

### 5.2. Push & Pull

#### `git push` - Upload Local Commits

```bash
# Push to remote
git push origin main

# Push all branches
git push --all

# First push, set upstream
git push -u origin main

# Force push (DANGEROUS, rewrites history)
git push --force

# Safer force push (checks remote hasn't changed)
git push --force-with-lease
```

#### `git pull` - Download & Merge

```bash
# Pull = fetch + merge
git pull origin main

# Equivalent to:
git fetch origin
git merge origin/main

# Pull with rebase (cleaner history)
git pull --rebase origin main
```

#### `git fetch` - Download Only (No Merge)

```bash
# Fetch all branches
git fetch origin

# Fetch specific branch
git fetch origin main

# View fetched branches (không merge)
git log origin/main

# Diff with local
git diff main origin/main
```

### 5.3. Tracking Branches

**Local branch tracks remote branch:**

```bash
# Set upstream for current branch
git branch --set-upstream-to=origin/main

# Or during first push:
git push -u origin main

# View tracking
git branch -vv

# Output:
# * main    a1b2c3d [origin/main: ahead 2, behind 1] Latest commit
```

---

## 6. GitHub Essentials

### 6.1. GitHub vs Git

**Git:**

- Version control tool (command-line)
- Works locally
- Open source

**GitHub:**

- Web-based hosting service for Git
- Social coding platform
- Additional features: Issues, PRs, Actions, Wikis
- Microsoft-owned (since 2018)

**Alternatives:** GitLab, Bitbucket, Gitea

### 6.2. Creating Repository

**On GitHub:**

```
1. Click "New repository"
2. Name: my-project  
3. Description: (optional)
4. Public/Private
5. Initialize with README (optional)
6. Create
```

**Push existing local repo:**

```bash
# Add remote
git remote add origin https://github.com/user/my-project.git

# Push
git push -u origin main
```

### 6.3. Clone via HTTPS vs SSH

#### HTTPS

```bash
git clone https://github.com/user/repo.git

# Pro: Easy, works everywhere
# Con: Need to enter credentials (or use credential helper)
```

#### SSH

```bash
git clone git@github.com:user/repo.git

# Pro: No password needed (use SSH key)
# Con: Need to setup SSH key first
```

**Setup SSH key (đã làm trong Module 00):**

```bash
# Generate key (if not done)
ssh-keygen -t ed25519 -C "email@example.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copy public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub:
# Settings → SSH and GPG keys → New SSH key → Paste
```

### 6.4. README.md

**Project's face on GitHub:**

```markdown
# Project Name

Brief description

## Installation

\`\`\`bash
git clone https://github.com/user/repo.git
cd repo
npm install
\`\`\`

## Usage

\`\`\`bash
npm start
\`\`\`

## Contributing

Pull requests are welcome!

## License

MIT
```

**Markdown essentials:**

```markdown
# Heading 1
## Heading 2

**bold** *italic*

- List item
- Another item

1. Numbered
2. List

[Link](https://example.com)

![Image](image.png)

\`inline code\`

\`\`\`python
# Code block
print("Hello")
\`\`\`
```

### 6.5. .gitignore

**Tell Git to ignore files:**

```bash
# Create .gitignore
cat > .gitignore << 'EOF'
# Node modules
node_modules/

# Environment variables
.env

# Build output
dist/
build/

# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Logs
*.log
EOF

git add .gitignore
git commit -m "Add .gitignore"
```

**Templates:** <https://github.com/github/gitignore>

---

## 7. Collaboration Workflows

### 7.1. Fork & Pull Request

**Open source contribution workflow:**

```
1. Fork repository (GitHub)
   → Creates copy under your account

2. Clone your fork
   git clone https://github.com/YOU/repo.git

3. Create feature branch
   git checkout -b fix-typo

4. Make changes, commit
   git commit -m "Fix typo in README"

5. Push to your fork
   git push origin fix-typo

6. Open Pull Request on GitHub
   → From: YOUR/repo:fix-typo
   → To: ORIGINAL/repo:main

7. Discuss, review, merge
```

### 7.2. Pull Request Best Practices

**Good PR:**

- ✅ Small, focused changes
- ✅ Clear title and description
- ✅ Reference issues (#42)
- ✅ Tests pass (CI)
- ✅ Screenshots (if UI changes)

**Example PR description:**

```markdown
## What
Fixes #42 - Login button not working on mobile

## Why  
Button was cut off on small
screens

## How
- Changed fixed width to percentage
- Added media query for mobile

## Testing
Tested on iPhone 12, Chrome mobile, Firefox Android

## Screenshots
Before:
![before](url)

After:
![after](url)
```

### 7.3. Code Review

**Reviewer checks:**

- ✅ Code quality
- ✅ Tests
- ✅ Performance
- ✅ Security
- ✅ Follows style guide

**Actionable comments:**

```
❌ "This is bad"
✅ "Consider using a Map here for O(1) lookup instead of array.find()"

❌ "Wrong approach"
✅ "This works but recursion may cause stack overflow for large inputs. 
   Suggestion: use iteration instead"
```

---

## 8. Best Practices

### 8.1. Commit Often

```
✅ Many small commits
❌ One huge commit at end of day

✅ git commit -m "Add login UI"
   git commit -m "Add login validation"
   git commit -m "Add login API integration"

❌ git commit -m "Add entire login feature 2000 lines"
```

### 8.2. Write Clear Messages

```
✅ Add user authentication with OAuth2
✅ Fix memory leak in image upload
✅ Refactor database queries for performance

❌ Update
❌ Fix
❌ Changes
❌ asdfg
```

### 8.3. Branch Naming

```
✅ feature/user-auth
✅ bugfix/login-crash  
✅ hotfix/security-patch
✅ refactor/database-layer

❌ branch1
❌ test
❌ new-stuff
```

### 8.4. Never Commit Secrets

```bash
# ❌ DON'T commit:
.env
config/production.yml
private-key.pem

# ✅ Add to .gitignore
echo ".env" >> .gitignore

# If already committed:
git rm --cached .env
git commit -m "Remove .env from git"

# Then rotate the exposed secret immediately!
```

---

## 9. Troubleshooting

### 9.1. Undo Changes

```bash
# Unstage file
git restore --staged file.txt

# Discard working directory changes
git restore file.txt

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Undo pushed commit (create new commit that reverts)
git revert abc123
```

### 9.2. Common Issues

**Issue: "fatal: not a git repository"**

```bash
# Fix: Initialize git
git init
```

**Issue: "Your branch is behind origin/main"**

```bash
# Fix: Pull updates
git pull origin main
```

**Issue: "error: failed to push some refs"**

```bash
# Someone else pushed first
# Fix: Pull, resolve conflicts, push
git pull origin main
# Resolve conflicts if any
git push origin main
```

**Issue: Large file causing slow push**

```bash
# Find large files
git rev-list --objects --all | grep "$(git verify-pack -v .git/objects/pack/*.idx | sort -k 3 -n | tail 10)"

# Remove from history (advanced)
git filter-branch --tree-filter 'rm -f large-file.zip' HEAD
```

---

## 📚 Tổng kết

### Key Takeaways

1. **Git = DVCS** - Fast, distributed, cheap branching
2. **Three states:** Working Dir → Staging → Repository
3. **Commits = snapshots**, not diffs
4. **Branching = cheap** - Create liberally
5. **Merge vs Rebase** - Merge for shared branches, rebase for local cleanup
6. **GitHub ≠ Git** - GitHub is hosting + collaboration platform
7. **Pull Requests** - Standard workflow for contributions

### Checklist

- [ ] Initialize and clone repositories
- [ ] Stage and commit changes with clear messages
- [ ] View history with `git log`
- [ ] Understand Git object model (blob, tree, commit)
- [ ] Create and merge branches
- [ ] Resolve merge conflicts
- [ ] Push and pull with remotes
- [ ] Fork and create Pull Requests
- [ ] Write good README and .gitignore

### Next: Module 03 - NETWORKING_INTRO

👉 Time to understand how computers communicate!

---

> **Git is your time machine. Use it wisely.** ⏰🔀
