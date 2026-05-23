# 🤝 Contributing to DevOps Journey

Thank you for your interest in contributing to **DevOps Journey**! All contributions are welcome and appreciated.

---

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How to Contribute](#-how-to-contribute)
- [Pull Request Process](#-pull-request-process)
- [Coding Standards](#-coding-standards)
- [Commit Convention](#-commit-convention)
- [Documentation Guidelines](#-documentation-guidelines)
- [Reporting Bugs](#-reporting-bugs)
- [Feature Requests](#-feature-requests)
- [Community](#-community)

---

## 📜 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). By participating, you agree to abide by these rules.

### Basic Rules

- ✅ Respect all contributors
- ✅ Welcome constructive feedback
- ✅ Focus on what's best for the community
- ✅ Show empathy towards others

---

## 🚀 How to Contribute

### Types of Contributions Welcome

| Type | Description |
|------|-------------|
| 📝 **Content** | Write/update module content |
| 🐛 **Bug fixes** | Fix typos, broken links |
| 🔬 **Labs** | Add new hands-on labs |
| ❓ **Quizzes** | Add knowledge check questions |
| 🌐 **Translations** | Translate to other languages |
| 🖼️ **Diagrams** | Add illustration images |
| 📖 **Documentation** | Improve documentation |

### Quick Start

```bash
# 1. Fork repository
# Click "Fork" button on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/DevOps-Journey.git
cd DevOps-Journey

# 3. Add upstream remote
git remote add upstream https://github.com/thanhlehoang0107/DevOps-Journey.git

# 4. Create a branch
git checkout -b feature/your-feature-name

# 5. Make your changes
# ... edit files ...

# 6. Commit changes
git add .
git commit -m "feat: add new lab for Docker module"

# 7. Push to your fork
git push origin feature/your-feature-name

# 8. Create Pull Request
# Go to GitHub and click "New Pull Request"
```

---

## 🔄 Pull Request Process

### Before Creating PR

- [ ] Sync fork with latest upstream
- [ ] Create new branch from `main`
- [ ] Test your content/code
- [ ] Ensure no spelling errors
- [ ] Update documentation if needed

### PR Checklist

```markdown
## Description
<!-- Brief description of changes -->

## Type of Change
- [ ] 📝 Content update
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 📖 Documentation
- [ ] 🔧 Configuration

## Testing
<!-- How did you test this? -->

## Screenshots (if applicable)
<!-- Add screenshots if relevant -->

## Checklist
- [ ] I have read the Contributing Guidelines
- [ ] Code/Content follows project standards
- [ ] No typos
- [ ] Links work correctly
```

### Review Process

1. **Automated Checks** - GitHub Actions checks format
2. **Maintainer Review** - Review within 2-3 business days
3. **Feedback** - Make changes if needed
4. **Merge** - PR is merged into main

---

## 📏 Coding Standards

### Markdown Files

```markdown
# Heading 1 (only 1 per file)

## Heading 2

### Heading 3

- Bullet points with `-`
- Don't mix `-` and `*`

1. Numbered lists
2. Use correct order

`inline code` for short commands

​```bash
# Code blocks for multi-line
docker run -d nginx
​```

| Column 1 | Column 2 |
|----------|----------|
| Data     | Data     |
```

### File Naming

```
✅ Good:
README.md
LABS.md
docker-compose.yml
my_script.sh

❌ Bad:
readme.MD
Labs.Md
Docker Compose.yml
my script.sh
```

### Images

- Place in `images/` folder of the module
- Use `.png` or `.webp` format
- Filename lowercase with dashes: `docker-architecture.png`
- Resize images appropriately (max 1200px width)

---

## 💬 Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

| Type | Description |
|------|-------------|
| `feat` | Add new feature/content |
| `fix` | Fix bug/error |
| `docs` | Documentation changes |
| `style` | Formatting, no code changes |
| `refactor` | Restructure, no behavior change |
| `test` | Add/fix tests |
| `chore` | Maintenance tasks |

### Examples

```bash
# Good commits
git commit -m "feat(track1): add Docker networking lab"
git commit -m "fix(track2): correct typo in Kubernetes guide"
git commit -m "docs: update README with new badge"
git commit -m "chore: update .gitignore"

# Bad commits
git commit -m "update"
git commit -m "fix stuff"
git commit -m "WIP"
```

---

## 📖 Documentation Guidelines

### README.md Structure

Each module README should have:

```markdown
# Module Title

> Brief description

---

## 🎯 Learning Objectives
- Objective 1
- Objective 2

---

## 📋 Prerequisites
- Prerequisite 1

---

## 📚 Content

### Topic 1
...

### Topic 2
...

---

## 🔗 Related Resources
- [Link 1](url)
- [Link 2](url)

---

## ➡️ Next Steps
- Link to next module
```

### LABS.md Structure

```markdown
# Labs: Module Name

## Lab 1: Lab Title

### Objectives
- What students will learn

### Prerequisites
- What's needed before starting

### Steps

#### Step 1: Title
​```bash
command here
​```

Expected output:
​```
output here
​```

#### Step 2: Title
...

### Verification
How to verify the lab is complete

### Cleanup
​```bash
# Commands to clean up resources
​```

---

## Lab 2: Next Lab Title
...
```

---

## 🐛 Reporting Bugs

### Create a Bug Report

1. **Check existing issues** - See if bug has already been reported
2. **Create new issue** with template:

```markdown
## Bug Description
<!-- Clear description of the bug -->

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. See error

## Expected Behavior
<!-- What you expected to happen -->

## Actual Behavior
<!-- What actually happened -->

## Screenshots
<!-- If applicable -->

## Environment
- OS: [e.g. Windows 11]
- Browser: [e.g. Chrome 120]
- Tool version: [e.g. Docker 24.0]

## Additional Context
<!-- Any other information -->
```

---

## 💡 Feature Requests

### Create a Feature Request

```markdown
## Feature Description
<!-- Describe the feature you want -->

## Problem it Solves
<!-- What problem does this solve? -->

## Proposed Solution
<!-- How do you propose to implement this? -->

## Alternatives Considered
<!-- Other alternatives you've considered -->

## Additional Context
<!-- Images, links, examples... -->
```

---

## 🏷️ Labels

| Label | Description |
|-------|-------------|
| `good first issue` | Suitable for newcomers |
| `help wanted` | Need help |
| `bug` | Bug to fix |
| `enhancement` | Feature request |
| `documentation` | Related to docs |
| `track-1` ... `track-5` | Specific track |

---

## 👥 Community

### Maintainers

- **ThanhRòm** - [@thanhlehoang0107](https://github.com/thanhlehoang0107)

### Contributors

<!-- Contributors will be listed automatically -->

Thank you to all contributors! 🙏

---

## ❓ Questions?

If you have questions:

1. Check [existing issues](https://github.com/thanhlehoang0107/DevOps-Journey/issues)
2. Create a new issue with label `question`
3. Email: <thanhlehoang0107@gmail.com>

---

<div align="center">

**Thank you for contributing to DevOps Journey! 🚀**

</div>
