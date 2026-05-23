# Solutions: Module 02 - Git & GitHub

> **Answer key for exercises and quiz**

---

## 📋 EXERCISE SOLUTIONS

### Section A: Multiple Choice Questions (1-10)

1. **B** - Distributed version control system
2. **C** - `git init`
3. **A** - `git add file.txt`
4. **D** - `git commit -m "message"`
5. **B** - `git push origin main`
6. **C** - Creates a new branch
7. **A** - `git merge branch-name`
8. **D** - Area where git add puts files
9. **B** - `git pull`
10. **C** - Copy of repository stored elsewhere

### Section B: Fill in the Blank (11-20)

1. `git init`
2. `git add`
3. `git commit -m "message"`
4. `git status`
5. `git log`
6. `git branch new-branch`
7. `git checkout branch-name`
8. `git merge`
9. `git clone`
10. `git push origin main`

### Section C: Hands-on Tasks (21-30)

**21. Initialize repository:**

```bash
mkdir myproject
cd myproject
git init
```

**22. Create and commit:**

```bash
echo "# My Project" > README.md
git add README.md
git commit -m "Initial commit"
```

**23. Check status:**

```bash
git status
# Shows: working tree clean
```

**24. Create branch:**

```bash
git branch feature-login
git checkout feature-login
# Or: git checkout -b feature-login
```

**25. Make changes and commit:**

```bash
echo "Login feature" > login.txt
git add login.txt
git commit -m "Add login feature"
```

**26. Merge to main:**

```bash
git checkout main
git merge feature-login
```

**27. View commit history:**

```bash
git log
git log --oneline
git log --graph --oneline
```

**28. Add remote:**

```bash
git remote add origin https://github.com/username/repo.git
git remote -v  # Verify
```

**29. Push to GitHub:**

```bash
git push -u origin main
```

**30. Clone repository:**

```bash
git clone https://github.com/username/repo.git
cd repo
```

### Section D: Debugging Scenarios (31-40)

**31. Forgot to stage file:**

```bash
# Solution
git add forgotten-file.txt
git commit --amend --no-edit
```

**32. Wrong commit message:**

```bash
# Solution
git commit --amend -m "Correct message"
```

**33. Committed to wrong branch:**

```bash
# Solution
# On wrong branch
git log  # Copy commit hash

# Switch to correct branch
git checkout correct-branch
git cherry-pick COMMIT_HASH

# Go back and remove from wrong branch
git checkout wrong-branch
git reset --hard HEAD~1
```

**34. Merge conflict:**

```bash
# Edit conflicted files, resolve markers
# <<<<<<< HEAD
# Your changes
# =======
# Their changes
# >>>>>>> branch-name

# After resolving
git add resolved-file.txt
git commit -m "Resolve merge conflict"
```

**35. Accidentally deleted file:**

```bash
# If not committed yet
git checkout -- deleted-file.txt

# If committed
git log -- deleted-file.txt
git checkout COMMIT_HASH -- deleted-file.txt
```

**36. Need to undo last commit:**

```bash
# Keep changes
git reset --soft HEAD~1

# Discard changes (CAREFUL!)
git reset --hard HEAD~1
```

**37. Want to save work without committing:**

```bash
git stash
# Do other work
git stash pop  # Restore
```

**38. Pushed sensitive data:**

```bash
# Remove file
git rm --cached sensitive.txt
git commit -m "Remove sensitive file"

# Add to .gitignore
echo "sensitive.txt" >> .gitignore
git add .gitignore
git commit -m "Add to gitignore"

# Force push (if needed)
git push --force origin main

# NOTE: Better to use git-filter-branch or BFG for history cleanup
```

**39. Diverged branches:**

```bash
# Pull with rebase
git pull --rebase origin main

# Or merge
git pull origin main
# Resolve conflicts if any
```

**40. Need specific commit from another branch:**

```bash
git checkout target-branch
git cherry-pick COMMIT_HASH
```

---

## 📝 QUIZ SOLUTIONS

1. **C** - Distributed version control system
2. **B** - `git init`
3. **A** - `git add .`
4. **D** - `git commit -m "message"`
5. **C** - `git status`
6. **B** - Hidden directory storing Git data
7. **A** - Creates new branch
8. **D** - `git merge branch-name`
9. **C** - Staging area/index
10. **B** - `git clone URL`
11. **A** - `git push origin main`
12. **D** - `git pull`
13. **C** - Platform for hosting Git repositories
14. **B** - `git remote add origin URL`
15. **A** - Fork
16. **D** - Request to merge changes
17. **C** - `git log`
18. **B** - Temporarily save uncommitted changes
19. **A** - When two branches modify same lines
20. **D** - Add, commit, push
21. **C** - `git checkout branch-name`
22. **B** - Feature branch workflow
23. **A** - `git reset --soft HEAD~1`
24. **D** - `.gitignore`
25. **C** - `git commit --amend`

---

## 🎬 SCENARIO EXPLANATIONS

### Common Git Workflows

**Feature Development Workflow:**

```bash
# 1. Create feature branch
git checkout -b feature-user-auth

# 2. Make changes
# Edit files...

# 3. Commit frequently
git add .
git commit -m "Add user model"
git commit -m "Add authentication logic"

# 4. Merge to main
git checkout main
git merge feature-user-auth

# 5. Push
git push origin main
```

**Collaboration Workflow:**

```bash
# 1. Clone repository
git clone https://github.com/team/project.git
cd project

# 2. Create branch
git checkout -b my-feature

# 3. Make changes and commit
git add .
git commit -m "Add new feature"

# 4. Push branch
git push origin my-feature

# 5. Create Pull Request on GitHub

# 6. After review, merge on GitHub

# 7. Update local main
git checkout main
git pull origin main
```

**Hotfix Workflow:**

```bash
# 1. Create hotfix branch from main
git checkout main
git checkout -b hotfix-critical-bug

# 2. Fix bug
# Edit files...
git add .
git commit -m "Fix critical bug"

# 3. Merge to main
git checkout main
git merge hotfix-critical-bug

# 4. Also merge to develop (if exists)
git checkout develop
git merge hotfix-critical-bug

# 5. Push both
git push origin main
git push origin develop

# 6. Delete hotfix branch
git branch -d hotfix-critical-bug
```

---

## 🔧 COMMON COMMANDS REFERENCE

### Setup & Config

```bash
# Set username
git config --global user.name "Your Name"

# Set email
git config --global user.email "your@email.com"

# View config
git config --list

# Set default editor
git config --global core.editor "vim"
```

### Basic Commands

```bash
# Initialize
git init

# Clone
git clone URL

# Status
git status

# Add
git add file.txt
git add .

# Commit
git commit -m "message"
git commit -am "message"  # Add + commit

# Log
git log
git log --oneline
git log --graph --all
```

### Branching

```bash
# List branches
git branch

# Create branch
git branch branch-name

# Switch branch
git checkout branch-name

# Create and switch
git checkout -b branch-name

# Merge
git merge branch-name

# Delete branch
git branch -d branch-name
```

### Remote

```bash
# Add remote
git remote add origin URL

# View remotes
git remote -v

# Push
git push origin main
git push -u origin main  # Set upstream

# Pull
git pull origin main

# Fetch
git fetch origin
```

### Undoing Changes

```bash
# Unstage file
git reset HEAD file.txt

# Discard changes
git checkout -- file.txt

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Amend last commit
git commit --amend

# Stash changes
git stash
git stash list
git stash apply
git stash pop
```

---

## 📊 GRADING RUBRIC

**Total Points: 120**

### Breakdown

- Section A (MCQ 1-10): 10 × 2 = 20 points
- Section B (Fill 11-20): 10 × 2 = 20 points
- Section C (Tasks 21-30): 10 × 5 = 50 points
- Section D (Debug 31-40): 10 × 3 = 30 points

### Grading Scale

- 108-120: Excellent (A) ⭐⭐⭐ Git master!
- 96-107: Good (B) ⭐⭐ Strong understanding
- 84-95: Pass (C) ⭐ Competent
- < 84: Review needed

### Quiz Grading

- 23-25: Expert level
- 20-22: Proficient
- 17-19: Competent
- < 17: Needs practice

---

## 💡 STUDY TIPS

**Practice these daily:**

1. `git status` - Check before every action
2. `git add` → `git commit` - Commit often
3. `git log` - Review history
4. `git branch` - Know where you are
5. `git push` / `git pull` - Stay in sync

**Common mistakes to avoid:**

- Committing without checking status
- Working directly on main branch
- Force pushing without understanding
- Forgetting to pull before starting work
- Not using .gitignore for secrets

---

<div align="center">

**Git mastery = Version control confidence! 🚀**

**Practice every day! 💪**

</div>
