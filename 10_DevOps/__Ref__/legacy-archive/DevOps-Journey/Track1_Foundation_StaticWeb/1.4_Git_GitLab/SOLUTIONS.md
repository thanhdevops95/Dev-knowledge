# ✅ Solutions: Git & GitLab

> **Solutions for Exercises. Try to solve it yourself first!**
>
> *Đáp án cho Exercises. Hãy thử tự giải trước!*

---

## Exercise 1: Repository Setup

```bash
# Trên GitHub: Create new repository với README, .gitignore, LICENSE

# Clone
git clone https://github.com/username/project.git
cd project

# Create structure
mkdir -p src tests docs .github/workflows

# Add placeholder files
touch src/.gitkeep tests/.gitkeep docs/.gitkeep

# Commit
git add .
git commit -m "chore: add project structure"
git push origin main
```

---

## Exercise 2: Branching Strategy

```bash
# Create develop branch
git checkout -b develop
git push -u origin develop

# Feature auth
git checkout -b feature/auth develop
echo "Authentication module" > src/auth.js
git add . && git commit -m "feat: add authentication"
git checkout develop && git merge feature/auth
git branch -d feature/auth

# Feature api
git checkout -b feature/api develop
echo "API endpoints" > src/api.js
git add . && git commit -m "feat: add API endpoints"
git checkout develop && git merge feature/api
git branch -d feature/api

# Release
git checkout -b release/1.0 develop
echo "1.0.0" > VERSION
git add . && git commit -m "chore: prepare release 1.0.0"

# Merge to main
git checkout main
git merge release/1.0
git tag -a v1.0.0 -m "Release version 1.0.0"

# Merge back to develop
git checkout develop
git merge release/1.0
git branch -d release/1.0

# Push all
git push origin main develop --tags
```

---

## Exercise 3: Conflict Resolution

```bash
# Setup
echo '{"setting": "original"}' > config.json
git add config.json && git commit -m "Add config"

# Branch 1
git checkout -b change-1
echo '{"setting": "value-from-branch-1"}' > config.json
git commit -am "Update config in branch 1"

# Branch 2
git checkout main
git checkout -b change-2
echo '{"setting": "value-from-branch-2"}' > config.json
git commit -am "Update config in branch 2"

# Merge branch 1 (no conflict)
git checkout main
git merge change-1

# Merge branch 2 (conflict!)
git merge change-2
# CONFLICT in config.json

# Resolve manually - edit file to:
# {"setting": "merged-value"}

git add config.json
git commit -m "Merge branch 'change-2' - resolved conflict"
```

---

## Exercise 4: Interactive Rebase

```bash
# Create messy commits
echo "1" > file.txt && git add . && git commit -m "wip"
echo "2" >> file.txt && git add . && git commit -m "more stuff"
echo "3" >> file.txt && git add . && git commit -m "fix thing"
echo "4" >> file.txt && git add . && git commit -m "update"
echo "5" >> file.txt && git add . && git commit -m "done"

# Interactive rebase last 5 commits
git rebase -i HEAD~5

# In editor, change to:
# pick -> reword (for first)
# pick -> squash (for second)
# pick -> reword
# pick (keep)
# pick (keep)

# Save and follow prompts to rewrite messages

# Force push (with lease for safety)
git push --force-with-lease origin main
```

---

## Exercise 5: Git Hooks

### pre-commit

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for TODO comments
if grep -rn "TODO" --include="*.js" --include="*.py" .; then
    echo "❌ Found TODO comments. Please resolve before committing."
    exit 1
fi

echo "✅ Pre-commit checks passed"
exit 0
```

### commit-msg

```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_msg=$(cat "$1")
pattern="^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
    echo "❌ Commit message must follow conventional commits format:"
    echo "   type(scope): description"
    echo "   Example: feat(auth): add login functionality"
    exit 1
fi

echo "✅ Commit message format valid"
exit 0
```

### pre-push

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "Running tests before push..."

# Run tests (example with npm)
if ! npm test 2>/dev/null; then
    echo "❌ Tests failed. Push aborted."
    exit 1
fi

echo "✅ All tests passed"
exit 0
```

```bash
# Make hooks executable
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/commit-msg
chmod +x .git/hooks/pre-push
```

---

## Exercise 6: Collaboration Workflow

```bash
# Fork on GitHub UI

# Clone your fork
git clone https://github.com/YOUR_USERNAME/repo.git
cd repo

# Add upstream
git remote add upstream https://github.com/ORIGINAL_OWNER/repo.git

# Create feature branch
git checkout -b feature/my-contribution

# Make changes
echo "My contribution" > contribution.md
git add . && git commit -m "feat: add contribution"

# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main
git checkout feature/my-contribution
git rebase main

# Push to your fork
git push origin feature/my-contribution

# Create PR on GitHub UI
```

---

**[← Back to Exercises](./EXERCISES.md)** | **[Back to README →](./README.md)**
