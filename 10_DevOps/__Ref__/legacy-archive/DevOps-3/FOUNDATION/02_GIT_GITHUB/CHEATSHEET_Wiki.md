# Git & GitHub - Cheatsheet

> **Quick reference for version control**

---

## ⚙️ SETUP & CONFIG

```bash
# Install verification
git --version

# Initial configuration
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --global init.defaultBranch main

# View config
git config --list
git config user.name
git config user.email

# Set default editor
git config --global core.editor "code --wait"    # VS Code
git config --global core.editor "vim"            # Vim
git config --global core.editor "nano"           # Nano
```

---

## 📂 REPOSITORY CREATION

```bash
# Initialize new repo
git init

# Clone existing repo
git clone https://github.com/user/repo.git
git clone https://github.com/user/repo.git my-folder

# Clone specific branch
git clone -b branch-name https://github.com/user/repo.git
```

---

## 📊 STATUS & INFO

```bash
# Check status
git status
git status -s              # Short format

# View changes
git diff                   # Unstaged changes
git diff --staged          # Staged changes
git diff HEAD              # All changes
git diff branch1..branch2  # Compare branches

# Show commit
git show                   # Latest commit
git show commitID          # Specific commit
git show HEAD~3            # 3 commits ago
```

---

## 📝 STAGING & COMMITTING

```bash
# Stage files
git add file.txt           # Single file
git add file1 file2        # Multiple files
git add .                  # All files in current dir
git add *.js               # All .js files
git add -A                 # All changes (including deletions)

# Unstage
git restore --staged file  # Unstage file
git reset HEAD file        # Old way

# Commit
git commit -m "message"                    # With message
git commit -am "message"                   # Add + commit (tracked files)
git commit --amend -m "new message"        # Modify last commit
git commit --amend --no-edit               # Amend without changing message

# Discard changes
git restore file           # Discard unstaged changes
git checkout -- file       # Old way
git restore .              # Discard all unstaged changes
```

---

## 📜 HISTORY & LOGS

```bash
# View history
git log                    # Full history
git log --oneline          # Compact
git log --graph            # Visual graph
git log --all              # All branches
git log -n 5               # Last 5 commits
git log --since="2 weeks"  # Last 2 weeks
git log --author="John"    # By author

# Combined (most useful)
git log --oneline --graph --all --decorate

# Search commits
git log --grep="bug"       # Commits mentioning "bug"
git log -S "function"      # Commits adding/removing "function"

# File history
git log -- file.txt        # History of specific file
git log -p file.txt        # With patches (changes)
```

---

## 🔀 BRANCHING

```bash
# List branches
git branch                 # Local branches
git branch -a              # All branches (local + remote)
git branch -r              # Remote branches only

# Create branch
git branch branch-name

# Switch branch
git checkout branch-name       # Old way
git switch branch-name         # New way (Git 2.23+)

# Create + switch
git checkout -b new-branch     # Old way
git switch -c new-branch       # New way

# Rename branch
git branch -m old-name new-name    # Rename branch
git branch -m new-name             # Rename current branch

# Delete branch
git branch -d branch-name      # Safe delete (merged only)
git branch -D branch-name      # Force delete
```

---

## 🔗 MERGING

```bash
# Merge branch into current
git merge branch-name

# Merge with message
git merge branch-name -m "Merge message"

# Abort merge (if conflicts)
git merge --abort

# Continue after resolving conflicts
git add resolved-file
git commit                 # Complete merge
```

---

## 🌐 REMOTE REPOSITORIES

```bash
# View remotes
git remote                 # List remotes
git remote -v              # With URLs

# Add remote
git remote add origin https://github.com/user/repo.git
git remote add upstream https://github.com/original/repo.git

# Change remote URL
git remote set-url origin https://new-url.git

# Remove remote
git remote remove origin

# Rename remote
git remote rename old-name new-name
```

---

## ⬆️ PUSHING

```bash
# Push to remote
git push origin main               # Push main branch
git push origin branch-name        # Push specific branch
git push -u origin main            # Push + set upstream
git push                           # After upstream set

# Push all branches
git push --all origin

# Push tags
git push --tags

# Force push (DANGEROUS!)
git push --force                   # Overwrite remote
git push --force-with-lease        # Safer force push

# Delete remote branch
git push origin --delete branch-name
```

---

## ⬇️ PULLING & FETCHING

```bash
# Fetch (download without merge)
git fetch origin           # Fetch from origin
git fetch --all            # Fetch from all remotes

# Pull (fetch + merge)
git pull                   # Pull current branch
git pull origin main       # Pull specific branch
git pull --rebase          # Pull with rebase instead of merge

# Pull with specific strategy
git pull --ff-only         # Fast-forward only (fail if not possible)
```

---

## ↩️ UNDOING CHANGES

```bash
# Undo uncommitted changes
git restore file           # Discard changes in file
git restore .              # Discard all changes

# Undo last commit (keep changes)
git reset HEAD~1           # Soft reset
git reset --soft HEAD~1    # Keep changes staged

# Undo last commit (discard changes)
git reset --hard HEAD~1    # DANGEROUS!

# Undo specific commit (create new commit)
git revert commitID        # Safe for pushed commits

# Reset to specific commit
git reset --hard commitID  # DANGEROUS! Loses all changes

# Undo git add
git restore --staged file
git reset HEAD file
```

---

## 🏷️ TAGGING

```bash
# List tags
git tag
git tag -l "v1.*"          # Search tags

# Create tag
git tag v1.0.0                        # Lightweight tag
git tag -a v1.0.0 -m "Version 1.0"    # Annotated tag

# Tag specific commit
git tag v0.9 commitID

# Push tags
git push origin v1.0.0     # Push single tag
git push --tags            # Push all tags

# Delete tag
git tag -d v1.0.0          # Delete local
git push origin --delete v1.0.0    # Delete remote

# Checkout tag
git checkout v1.0.0        # Detached HEAD state
```

---

## 🔍 SEARCHING

```bash
# Search in files
git grep "pattern"         # Search in tracked files
git grep -n "function"     # With line numbers
git grep -c "TODO"         # Count occurrences

# Find commits
git log --grep="bug fix"   # Commit messages
git log -S "function"      # Code changes
```

---

## 🗑️ REMOVING FILES

```bash
# Remove file from Git AND filesystem
git rm file.txt
git commit -m "Remove file"

# Remove from Git only (keep local file)
git rm --cached file.txt
git commit -m "Untrack file"

# Remove directory
git rm -r folder/
```

---

## 📦 STASHING

```bash
# Save changes temporarily
git stash                  # Stash changes
git stash save "message"   # With message

# List stashes
git stash list

# Apply stash
git stash apply            # Apply latest, keep stash
git stash apply stash@{2}  # Apply specific stash
git stash pop              # Apply + remove from stash

# Drop stash
git stash drop             # Remove latest
git stash drop stash@{1}   # Remove specific

# Clear all stashes
git stash clear
```

---

## 🔄 REBASING

```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase (edit history)
git rebase -i HEAD~3       # Last 3 commits

# Continue after resolving conflicts
git add resolved-file
git rebase --continue

# Abort rebase
git rebase --abort

# Skip current commit
git rebase --skip
```

---

## 🔍 DEBUGGING

```bash
# Find commit that introduced bug (binary search)
git bisect start
git bisect bad             # Current commit is bad
git bisect good commitID   # Known good commit
# Git checks out middle commit, test it
git bisect good            # If works
git bisect bad             # If broken
# Repeat until found
git bisect reset           # End bisect

# Blame (who changed what)
git blame file.txt         # Show who changed each line
git blame -L 10,20 file    # Lines 10-20 only
```

---

## 📄 .gitignore PATTERNS

```gitignore
# Comments start with #

# Ignore specific file
secret.txt

# Ignore file type
*.log
*.tmp

# Ignore directory
node_modules/
dist/
build/

# Ignore in specific directory
/config/local.env

# Ignore everywhere
**/temp/

# Exception (don't ignore)
!important.log

# Ignore files with pattern
*.[oa]              # .o and .a files
*~                  # Backup files
```

**Common .gitignore:**

```gitignore
# Dependencies
node_modules/
vendor/
venv/

# Build outputs
dist/
build/
*.pyc
__pycache__/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Secrets
.env
*.key
*.pem
config/local.*

# Logs
*.log
logs/
```

---

## 🤝 PULL REQUEST WORKFLOW

```bash
# 1. Fork on GitHub (if not collaborator)

# 2. Clone YOUR fork
git clone https://github.com/YOUR-USERNAME/repo.git

# 3. Add upstream (original repo)
git remote add upstream https://github.com/ORIGINAL-OWNER/repo.git

# 4. Create feature branch
git checkout -b feature/my-feature

# 5. Make changes & commit
git add .
git commit -m "Add feature"

# 6. Push to YOUR fork
git push origin feature/my-feature

# 7. Create PR on GitHub

# 8. Keep fork updated with upstream
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## 💡 ALIASES (Add to ~/.gitconfig)

```bash
# Add these to [alias] section in ~/.gitconfig

[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = restore --staged
    last = log -1 HEAD
    visual = log --oneline --graph --all --decorate
    amend = commit --amend --no-edit
    undo = reset HEAD~1
    aliases = config --get-regexp ^alias\.
```

**Usage after setup:**

```bash
git st                     # Instead of git status
git co main                # Instead of git checkout main
git visual                 # Pretty log
```

---

## 🚨 EMERGENCY COMMANDS

```bash
# "I committed to wrong branch!"
git branch feature/correct-branch    # Create branch with commit
git reset --hard HEAD~1              # Remove from current
git checkout feature/correct-branch  # Switch to correct

# "I want to undo public commit!" (NEVER use reset for pushed!)
git revert commitID                  # Creates new commit

# "I accidentally committed secrets!"
git rm --cached .env
echo ".env" >> .gitignore
git commit --amend -m "Remove secrets"
git push --force
# THEN: Rotate all credentials immediately!

# "Help! Everything is broken!"
git reflog                 # Find where you were before
git reset --hard HEAD@{5}  # Go back to that state
```

---

## 📊 USEFUL COMBOS

```bash
# View all commits since yesterday
git log --since="1 day ago" --oneline

# See what changed in last commit
git show HEAD

# List files in last commit
git diff-tree --no-commit-id --name-only -r HEAD

# Count commits by author
git shortlog -sn

# View file at specific commit
git show commitID:path/to/file

# Compare with specific commit
git diff commitID file.txt

# Checkout file from another branch
git checkout branch-name -- file.txt
```

---

## ⚙️ CONFIGURATION TIPS

```bash
# Better merge conflict markers
git config --global merge.conflictstyle diff3

# Always push current branch
git config --global push.default current

# Colorful output
git config --global color.ui auto

# Cache credentials (15 min)
git config --global credential.helper cache

# Cache credentials (1 hour)
git config --global credential.helper 'cache --timeout=3600'

# Auto-correct typos
git config --global help.autocorrect 1
```

---

<div align="center">

**Bookmark this! You'll use it daily! 🔖**

**Practice → Mastery → DevOps Career! 💪**

</div>
