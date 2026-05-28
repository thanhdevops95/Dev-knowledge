# Contributing to DevOps Training

First off, thank you for considering contributing to DevOps Training! ❤️

This project is built by the community, for the community. Every contribution helps make DevOps education better and more accessible.

## 🤝 Ways to Contribute

### 1. 📝 Improve Documentation

- Fix typos or grammar errors
- Add clarifications or examples
- Translate to other languages
- Add diagrams or illustrations

### 2. 💡 Add Content

- New scenarios and real-world examples
- Additional exercises
- Quiz questions
- Lab improvements

### 3. 🐛 Report Bugs

- Broken links
- Incorrect commands or code
- Setup issues
- Errors in examples

### 4. ✨ Suggest Features

- New modules or topics
- Tools or technologies to cover
- Better project ideas
- Learning path improvements

---

## 📋 How to Contribute

### Quick Contributions (Typos, small fixes)

1. **Find the file** you want to edit on GitHub
2. **Click the pencil icon** (✏️) to edit
3. **Make your changes**
4. **Scroll down** and describe your changes
5. **Click "Propose changes"**
6. **Create pull request**

Done! We'll review and merge.

### Larger Contributions (New content, refactoring)

1. **Fork the repository**

   ```bash
   # On GitHub: Click "Fork" button
   ```

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR-USERNAME/DevOpsTraining.git
   cd DevOpsTraining
   ```

3. **Create a branch**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-you-are-fixing
   ```

4. **Make your changes**
   - Follow our [Style Guide](#style-guide)
   - Test your changes
   - Update relevant docs

5. **Commit your changes**

   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

6. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create Pull Request**
   - Go to original repo on GitHub
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill in PR template
   - Submit!

---

## 📐 Style Guide

### Markdown Files

**Headings:**

```markdown
# H1 - Module/File Title

## H2 - Major Sections

### H3 - Subsections

#### H4 - Sub-subsections
```

**Code Blocks:**

```markdown
Use triple backticks with language:

```\bash
echo "Example command"
\```

```python
print("Example Python")
\```
```

**Emphasis:**

- **Bold** for important terms
- *Italic* for emphasis
- `Code` for commands, file names, variables

**Lists:**

- Use `-` for unordered lists
- Use `1.` for ordered lists
- Indent with 2 spaces for nested lists

### Vietnamese Language

- Sử dụng tiếng Việt có dấu đầy đủ
- Technical terms: Giữ nguyên tiếng Anh, giải thích bằng tiếng Việt
  - ❌ "Bộ chứa" (confusing)
  - ✅ "Container - vùng chứa cô lập để chạy ứng dụng"

### Code Examples

**Always include:**

- Comments explaining what code does
- Expected output
- Error handling (if applicable)

**Good example:**

```bash
# Check if Docker is installed
docker --version

# Expected output:
# Docker version 24.0.7, build afdd53b
```

**Bad example:**

```bash
docker --version
```

### Labs & Exercises

**Format:**

```markdown
## Lab X: [Descriptive Title]

**Time:** X minutesObjective:** What student will learn

**Prerequisites:** What they need before starting

**Steps:**
1. Step 1 with clear instruction
   ```bash
   command here
   ```

   **Expected output:**

   ```
   output here
   ```

1. Step 2...

**Verification:**
How to check if lab completed successfully

**Troubleshooting (if needed):**
Common errors and fixes

```

---

## ✅ Pull Request Guidelines

### Before Submitting

- [ ] Read existing content to match style
- [ ] Test all commands and code examples
- [ ] Check all links work
- [ ] Run spell check
- [ ] Format markdown properly
- [ ] Add yourself to Contributors (if first PR)

### PR Title Format

Use conventional commits format:

- `docs: Fix typo in Module 01 README`
- `feat: Add new scenario for Docker networking`
- `fix: Correct kubectl command in Lab 05`
- `content: Add exercises for Kubernetes module`

### PR Description Template

When creating PR, use this template:

```markdown
## Description
Brief description of what this PR does

## Type of Change
- [ ] Documentation fix/improvement
- [ ] New content (scenarios, exercises, labs)
- [ ] Bug fix (broken command, link, etc.)
- [ ] New feature

## Related Issue
Fixes #(issue number) (if applicable)

## Screenshots (if visual changes)
[Add screenshots]

## Checklist
- [ ] Tested all commands/code
- [ ] Links verified
- [ ] Follows style guide
- [ ] Vietnamese language correct
```

---

## 🏆 Recognition

Contributors will be:

- Listed in [Contributors](CONTRIBUTORS.md) file
- Shown on GitHub contributors page
- Credited in course updates

---

## 💬 Communication

- **Questions?** Open a [Discussion](https://github.com/your-org/DevOpsTraining/discussions)
- **Bug report?** Open an [Issue](https://github.com/your-org/DevOpsTraining/issues)
- **Chat?** Join our [Discord](https://discord.gg/devops-training)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 🙏 Thank You

Every contribution, no matter how small, makes a difference. Thank you for helping make DevOps education better for everyone! 🚀

---

<div align="center">

**Made with ❤️ by the community**

</div>
