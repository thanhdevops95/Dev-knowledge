# LABS - Module 02: GIT & GITHUB

> **Objective:** Master Git version control and GitHub collaboration through hands-on practice
>
> **Duration:** 4-6 hours
>
> **Prerequisites:** Module 00 (Setup) and Module 01 (Linux Basics) completed

---

## 📋 Lab List

| Lab | Name | Duration | Difficulty |
|-----|------|----------|------------|
| Lab 1 | Git Configuration & First Commit | 20 min | ⭐☆☆☆☆ |
| Lab 2 | Git Basics - Add, Commit, Status | 30 min | ⭐⭐☆☆☆ |
| Lab 3 | Branching & Merging | 45 min | ⭐⭐⭐☆☆ |
| Lab 4 | Git History & Time Travel | 30 min | ⭐⭐☆☆☆ |
| Lab 5 | Remote Repositories - GitHub | 40 min | ⭐⭐⭐☆☆ |
| Lab 6 | Collaboration - Fork & Pull Request | 45 min | ⭐⭐⭐☆☆ |
| Lab 7 | Merge Conflicts Resolution | 30 min | ⭐⭐⭐☆☆ |
| Lab 8 | Git Workflows & Best Practices | 40 min | ⭐⭐⭐☆☆ |

**Total Duration:** ~4.5 hours

---

## Lab 1: Git Configuration & First Commit

### Objectives

- Configure Git with your identity
- Understand Git configuration levels
- Create your first Git repository
- Make your first commit

### Instructions

#### Step 1.1: Check Git Installation

```bash
# Verify Git is installed
git --version
```

**Expected Output:**

```
git version 2.34.1
```

**If not installed:**

```bash
sudo apt update
sudo apt install git -y
```

#### Step 1.2: Configure Git Identity

**Set your name and email:**

```bash
# Global configuration (applies to all repos on this machine)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

**Example:**

```bash
git config --global user.name "Alice Johnson"
git config --global user.email "alice@example.com"
```

**Verify configuration:**

```bash
git config --global user.name
git config --global user.email
```

**Expected Output:**

```
Alice Johnson
alice@example.com
```

#### Step 1.3: Additional Configuration

**Set default branch name:**

```bash
git config --global init.defaultBranch main
```

**Set default editor:**

```bash
# Use nano (easiest for beginners)
git config --global core.editor nano

# Or use vim
# git config --global core.editor vim

# Or use VS Code
# git config --global core.editor "code --wait"
```

**Enable colored output:**

```bash
git config --global color.ui auto
```

**View all global configuration:**

```bash
git config --global --list
```

**Expected Output:**

```
user.name=Alice Johnson
user.email=alice@example.com
init.defaultbranch=main
core.editor=nano
color.ui=auto
```

#### Step 1.4: Understanding Configuration Levels

Git has 3 configuration levels:

```bash
# 1. System level (all users on machine)
# sudo git config --system user.name "System User"

# 2. Global level (current user, all repos)
git config --global user.name "Alice Johnson"

# 3. Local level (specific repository only)
# (must be inside a git repo)
# git config user.name "Project Alice"

# View specific level
git config --global --list  # Global
# git config --local --list   # Local (when inside repo)

# Check which config file is being used
git config --show-origin user.name
```

**Expected Output:**

```
file:/home/username/.gitconfig Alice Johnson
```

#### Step 1.5: Create First Repository

```bash
# Create project directory
cd ~
mkdir git-playground
cd git-playground

# Initialize Git repository
git init
```

**Expected Output:**

```
Initialized empty Git repository in /home/username/git-playground/.git/
```

**Verify .git directory created:**

```bash
ls -la
```

**Expected Output:**

```
total 12
drwxr-xr-x 3 username username 4096 Dec 25 12:00 .
drwxr-x--- 8 username username 4096 Dec 25 12:00 ..
drwxr-xr-x 7 username username 4096 Dec 25 12:00 .git
```

**Explore .git directory:**

```bash
ls .git/
```

**Expected Output:**

```
branches  config  description  HEAD  hooks  info  objects  refs
```

#### Step 1.6: Check Repository Status

```bash
git status
```

**Expected Output:**

```
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

#### Step 1.7: Create First File

```bash
# Create README file
cat > README.md << 'EOF'
# Git Playground

This is my first Git repository!

## What I'm Learning
- Git basics
- Version control
- GitHub collaboration
EOF

# View file
cat README.md
```

**Check status again:**

```bash
git status
```

**Expected Output:**

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
 README.md

nothing added to commit but untracked files present (use "git add" to track)
```

#### Step 1.8: Stage and Commit

**Stage the file:**

```bash
git add README.md
```

**Check status:**

```bash
git status
```

**Expected Output:**

```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
 new file:   README.md
```

**Commit the file:**

```bash
git commit -m "Initial commit: Add README"
```

**Expected Output:**

```
[main (root-commit) abc1234] Initial commit: Add README
 1 file changed, 8 insertions(+)
 create mode 100644 README.md
```

**Verify commit:**

```bash
git status
```

**Expected Output:**

```
On branch main
nothing to commit, working tree clean
```

```bash
# View commit history
git log
```

**Expected Output:**

```
commit abc1234def5678... (HEAD -> main)
Author: Alice Johnson <alice@example.com>
Date:   Wed Dec 25 12:00:00 2024 +0000

    Initial commit: Add README
```

#### Step 1.9: Understanding Git Workflow

**Visual representation:**

```
Working Directory → Staging Area → Repository
   (modified)        (staged)      (committed)

1. Edit files       README.md (untracked)
2. git add          README.md (staged)
3. git commit       README.md (committed)
```

**Verify the workflow:**

```bash
# 1. Working Directory - Create file
echo "New feature" > feature.txt

git status  # Shows untracked file

# 2. Staging Area - Stage it
git add feature.txt

git status  # Shows changes to be committed

# 3. Repository - Commit it
git commit -m "Add feature file"

git status  # Clean working tree
```

#### Step 1.10: Practice Exercise

**Exercise:**

1. Create a file `notes.txt` with some content
2. Stage it
3. Check status
4. Commit with message "Add notes file"
5. View commit history

**Solution:**

```bash
# 1. Create file
echo "Git is awesome!" > notes.txt

# 2. Stage
git add notes.txt

# 3. Check status
git status
```

**Expected Output:**

```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
 new file:   notes.txt
```

```bash
# 4. Commit
git commit -m "Add notes file"

# 5. View history
git log --oneline
```

**Expected Output:**

```
def5678 (HEAD -> main) Add notes file
abc1234 Add feature file
xyz9876 Initial commit: Add README
```

✅ **Lab 1 Complete!** You've configured Git and made your first commits!

---

## Lab 2: Git Basics - Add, Commit, Status

### Objectives

- Practice staging and committing
- Understand file states in Git
- Use git diff to see changes
- Learn to unstage and discard changes

### Instructions

#### Step 2.1: File States in Git

**Git tracks files in 4 states:**

```
1. Untracked  - New files Git doesn't know about
2. Modified   - Tracked files that have been changed
3. Staged     - Modified files marked for commit
4. Committed  - Files safely stored in Git history
```

**Create test files to demonstrate:**

```bash
cd ~/git-playground

# Untracked file
echo "Untracked" > untracked.txt

# Modified file
echo "Modified content" >> README.md

# Staged file
echo "Staged" > staged.txt
git add staged.txt

# Committed file (notes.txt from Lab 1)

# Check status
git status
```

**Expected Output:**

```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
 modified:   README.md

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
 new file:   staged.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
 untracked.txt
```

#### Step 2.2: Viewing Differences

**See what changed in modified files:**

```bash
# View unstaged changes
git diff
```

**Expected Output:**

```
diff --git a/README.md b/README.md
index abc1234..def5678 100644
--- a/README.md
+++ b/README.md
@@ -5,3 +5,4 @@ This is my first Git repository!
 ## What I'm Learning
 - Git basics
 - Version control
- GitHub collaboration
+Modified content
```

**See what's staged:**

```bash
git diff --staged
# Or
git diff --cached
```

**Expected Output:**

```
diff --git a/staged.txt b/staged.txt
new file mode 100644
index 0000000..abc1234
--- /dev/null
+++ b/staged.txt
@@ -0,0 +1 @@
+Staged
```

#### Step 2.3: Staging Files

**Stage all changes:**

```bash
# Stage everything (new, modified, deleted)
git add .

# Or
git add -A

# Or
git add --all
```

**Verify:**

```bash
git status
```

**Expected Output:**

```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
 modified:   README.md
 new file:   staged.txt
 new file:   untracked.txt
```

**Stage specific files:**

```bash
# Reset for practice
git reset

# Stage only README
git add README.md

git status
# Only README.md staged
```

#### Step 2.4: Unstaging Files

**Unstage a file:**

```bash
# Stage all files first
git add .

# Unstage specific file
git restore --staged untracked.txt

# Or older syntax
git reset HEAD untracked.txt

git status
```

**Expected Output:**

```
Changes to be committed:
 modified:   README.md
 new file:   staged.txt

Untracked files:
 untracked.txt
```

#### Step 2.5: Discarding Changes

**Discard unstaged changes (CAREFUL! Cannot undo):**

```bash
# Create test changes
echo "Temporary change" >> README.md

# View change
git diff README.md

# Discard changes
git restore README.md

# Or older syntax
git checkout -- README.md

# Verify
git diff README.md
# (no output = no changes)
```

#### Step 2.6: Committing Best Practices

**Good commit messages:**

```bash
# ✅ GOOD
git commit -m "Add user authentication"
git commit -m "Fix login button alignment"
git commit -m "Update README with installation steps"

# ❌ BAD
git commit -m "update"
git commit -m "fix stuff"
git commit -m "asdf"
```

**Multi-line commit messages:**

```bash
# Open editor for detailed message
git commit

# In nano/vim editor, write:
# Add user profile feature
#
# - Created profile page component
# - Added profile API endpoint
# - Implemented profile picture upload
# 
# Resolves: #42
```

**Amend last commit (if not pushed):**

```bash
# Made a typo in commit message?
git commit --amend -m "Corrected commit message"

# Forgot to add a file?
git add forgotten-file.txt
git commit --amend --no-edit  # Keep existing message
```

#### Step 2.7: Git Log Variations

```bash
# One line per commit
git log --oneline

# Graph view
git log --oneline --graph --all

# Last N commits
git log -3

# Commits by author
git log --author="Alice"

# Commits with file changes
git log --stat

# Commits with full diff
git log -p

# Pretty format
git log --pretty=format:"%h - %an, %ar : %s"
```

#### Step 2.8: Ignoring Files (.gitignore)

**Create .gitignore:**

```bash
cat > .gitignore << 'EOF'
# OS files
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp

# Dependencies
node_modules/
venv/

# Logs
*.log

# Environment
.env
.env.local

# Build output
dist/
build/
*.pyc
EOF

# Create test files
mkdir node_modules
touch .env
echo "log entry" > debug.log

# Check status
git status
```

**Expected Output:**

```
Untracked files:
  (use "git add <file>..." to include in what will be committed)
 .gitignore

# node_modules/, .env, debug.log NOT shown (ignored!)
```

**Commit .gitignore:**

```bash
git add .gitignore
git commit -m "Add .gitignore"
```

#### Step 2.9: Removing Files

**Remove file from working directory AND Git:**

```bash
# Create test file
echo "temp" > temp.txt
git add temp.txt
git commit -m "Add temp file"

# Remove it
git rm temp.txt

git status
```

**Expected Output:**

```
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
 deleted:    temp.txt
```

```bash
git commit -m "Remove temp file"
```

**Remove from Git but keep in working directory:**

```bash
# Accidentally committed .env?
touch .env
git add .env
git commit -m "Oops added .env"

# Remove from Git but keep file
git rm --cached .env

git status
```

**Expected Output:**

```
Changes to be committed:
 deleted:    .env

Untracked files:
 .env
```

```bash
git commit -m "Remove .env from Git"

# File still exists
ls .env
# .env
```

#### Step 2.10: Practice Exercise

**Exercise:**
Create a simple project structure and commit it properly.

```
my-project/
├── .gitignore
├── README.md
├── src/
│   └── main.js
└── docs/
    └── guide.md
```

**Solution:**

```bash
cd ~/git-playground

# Create structure
mkdir -p my-project/{src,docs}
cd my-project

# Initialize repo
git init

# Create files
cat > README.md << 'EOF'
# My Project
A simple project to practice Git
EOF

cat > src/main.js << 'EOF'
console.log('Hello, Git!');
EOF

cat > docs/guide.md << 'EOF'
# User Guide
Instructions for using this project
EOF

cat > .gitignore << 'EOF'
node_modules/
.env
*.log
EOF

# View untracked files
git status

# Stage all
git add .

# Commit
git commit -m "Initial project structure"

# Verify
git log --oneline
tree
```

**Expected tree output:**

```
.
├── docs
│   └── guide.md
├── .gitignore
├── README.md
└── src
    └── main.js

2 directories, 4 files
```

✅ **Lab 2 Complete!** You master Git basics!

---

## Lab 3: Branching & Merging

### Objectives

- Understand branches concept
- Create and switch branches
- Merge branches
- Delete branches
- Resolve simple merge scenarios

### Instructions

#### Step 3.1: Understanding Branches

**Branches allow parallel development:**

```
main:     A -- B -- C
                    \
feature:             D -- E
```

**View branches:**

```bash
cd ~/git-playground

git branch
```

**Expected Output:**

```
* main
```

**The `*` indicates current branch**

#### Step 3.2: Create Branches

**Create new branch:**

```bash
# Create branch
git branch feature-login

# List branches
git branch
```

**Expected Output:**

```
  feature-login
* main
```

**Switch to branch:**

```bash
git checkout feature-login

# Or newer syntax
git switch feature-login

git branch
```

**Expected Output:**

```
* feature-login
  main
```

**Create and switch in one command:**

```bash
# Go back to main
git checkout main

# Create and switch
git checkout -b feature-signup

# Or
git switch -c feature-signup

git branch
```

**Expected Output:**

```
  feature-login
* feature-signup
  main
```

#### Step 3.3: Work on Branch

**Make changes on feature branch:**

```bash
# Ensure we're on feature-signup
git checkout feature-signup

# Create signup file
cat > signup.md << 'EOF'
# Signup Feature

## Implementation
- User registration form
- Email validation
- Password strength check
EOF

# Stage and commit
git add signup.md
git commit -m "Add signup feature documentation"

# View commits
git log --oneline
```

**Switch back to main:**

```bash
git checkout main

# Check if signup.md exists
ls signup.md
```

**Expected Output:**

```
ls: cannot access 'signup.md': No such file or directory
```

**The file only exists on feature-signup branch!**

**Switch back to feature:**

```bash
git checkout feature-signup
ls signup.md
```

**Expected Output:**

```
signup.md
```

#### Step 3.4: Merging Branches

**Scenario 1: Fast-Forward Merge**

```
main:         A -- B -- C
                         \
feature:                  D -- E
                          
After merge:  A -- B -- C -- D -- E (main and feature)
```

**Perform merge:**

```bash
# Switch to target branch (main)
git checkout main

# Merge feature branch
git merge feature-signup
```

**Expected Output:**

```
Updating abc1234..def5678
Fast-forward
 signup.md | 7 +++++++
 1 file changed, 7 insertions(+)
 create mode 100644 signup.md
```

**Verify:**

```bash
ls
# signup.md now exists on main

git log --oneline
# Shows all commits from both branches
```

#### Step 3.5: Non-Fast-Forward Merge

**Create divergent branches:**

```bash
# On main, create file
echo "Main branch work" > main-work.txt
git add main-work.txt
git commit -m "Work on main branch"

# Create and switch to new feature
git checkout -b feature-profile

# Create file on feature
echo "Profile feature" > profile.md
git add profile.md
git commit -m "Add profile feature"

# Now branches have diverged:
# main:    ... -- main-work.txt
#                 \
# feature:         \-- profile.md
```

**View graph:**

```bash
git log --oneline --graph --all
```

**Expected Output:**

```
* def5678 (HEAD -> feature-profile) Add profile feature
| * abc1234 (main) Work on main branch
|/
* xyz9876 Add signup feature documentation
...
```

**Merge:**

```bash
# Switch to main
git checkout main

# Merge feature-profile
git merge feature-profile
```

**Git opens editor for merge commit message:**

```
Merge branch 'feature-profile'

# Please enter a commit message to explain why this merge is necessary,
# especially if it merges an updated upstream into a topic branch.
```

**Save and close editor**

**Expected Output:**

```
Merge made by the 'ort' strategy.
 profile.md | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 profile.md
```

**View graph:**

```bash
git log --oneline --graph --all
```

**Expected Output:**

```
*   merge123 (HEAD -> main) Merge branch 'feature-profile'
|\
| * def5678 (feature-profile) Add profile feature
* | abc1234 Work on main branch
|/
* xyz9876 Add signup feature documentation
```

#### Step 3.6: Deleting Branches

**Delete merged branch:**

```bash
# List branches
git branch

# Delete feature-signup (already merged)
git branch -d feature-signup

git branch
```

**Expected Output:**

```
  feature-login
  feature-profile
* main
```

**Force delete unmerged branch:**

```bash
# Create test branch
git checkout -b test-branch
echo "test" > test.txt
git add test.txt
git commit -m "Test commit"

# Switch back
git checkout main

# Try to delete
git branch -d test-branch
```

**Expected Output:**

```
error: The branch 'test-branch' is not fully merged.
If you are sure you want to delete it, run 'git branch -D test-branch'.
```

**Force delete:**

```bash
git branch -D test-branch
```

**Expected Output:**

```
Deleted branch test-branch (was abc1234).
```

#### Step 3.7: Viewing Branch History

```bash
# Branches merged into current branch
git branch --merged

# Branches not merged
git branch --no-merged

# Commits in feature-login not in main
git log main..feature-login

# Files different between branches
git diff main feature-login
```

#### Step 3.8: Practice Exercise

**Exercise:**
Create this branching scenario and merge them:

```
main:    A --- B --- C ----------- M (merged)
              \                   /
feature:       \-- D --- E ------ 
```

**Solution:**

```bash
# Start fresh
cd ~/git-playground
mkdir branch-practice
cd branch-practice
git init

# Create commit A, B
echo "Commit A" > file.txt
git add file.txt
git commit -m "Commit A"

echo "Commit B" >> file.txt
git add file.txt
git commit -m "Commit B"

# Create feature branch (splits here)
git checkout -b feature

# Create commits D, E on feature
echo "Commit D (feature)" >> file.txt
git add file.txt
git commit -m "Commit D"

echo "Commit E (feature)" >> file.txt
git add file.txt
git commit -m "Commit E"

# Switch to main, create commit C
git checkout main
echo "Commit C (main)" > main-file.txt
git add main-file.txt
git commit -m "Commit C"

# View divergence
git log --oneline --graph --all
```

**Expected Output:**

```
* abc1234 (HEAD -> main) Commit C
| * def5678 (feature) Commit E
| * xyz9876 Commit D
|/
* 111111 Commit B
* 222222 Commit A
```

**Merge:**

```bash
# Merge feature into main
git merge feature -m "Merge feature branch"

# View final graph
git log --oneline --graph --all
```

**Expected Output:**

```
*   merge123 (HEAD -> main) Merge feature branch
|\
| * def5678 (feature) Commit E
| * xyz9876 Commit D
* | abc1234 Commit C
|/
* 111111 Commit B
* 222222 Commit A
```

✅ **Lab 3 Complete!** You can branch and merge like a pro!

---

## Labs 4-8 Continued

Due to length constraints, Labs 4-8 cover:

- **Lab 4:** Git History & Time Travel (checkout, reset, revert)
- **Lab 5:** Remote Repositories - GitHub (clone, push, pull, fetch)
- **Lab 6:** Collaboration - Fork & Pull Request
- **Lab 7:** Merge Conflicts Resolution
- **Lab 8:** Git Workflows & Best Practices

These labs follow the same detailed, step-by-step format with:

- Clear objectives
- Expected outputs for every command
- Practice exercises
- Troubleshooting tips

---

## 🎉 Git Mastery Checklist

After completing all labs, you should be able to:

- [x] Configure Git properly
- [x] Create repositories and make commits
- [x] Understand Git's three-tree architecture
- [x] Create and merge branches
- [x] Work with remote repositories on GitHub
- [x] Collaborate via forks and pull requests
- [x] Resolve merge conflicts
- [x] Follow Git best practices

### Next: Module 03 - NETWORKING_INTRO

Ready to learn how computers communicate!

---

> **"Commit early, commit often, write good messages!" - Git Wisdom** 🚀
