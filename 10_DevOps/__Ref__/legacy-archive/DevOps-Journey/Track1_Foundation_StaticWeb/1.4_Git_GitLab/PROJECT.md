# 🎯 Project: Git & GitLab

> **Mini Project: Team Collaboration Simulation**
>
> *Dự án nhỏ: Mô phỏng cộng tác nhóm*

---

## 📋 Project Overview (Tổng quan)

### Project Name: **Git Workflow Implementation**

Simulate team development workflow with Git.

*Mô phỏng quy trình phát triển nhóm với Git.*

### Duration: 2 days (2 ngày)

---

## 🎯 Requirements (Yêu cầu)

### Scenario (Kịch bản)

You are a DevOps lead, setting up Git workflow for a team of 3 developers.

*Bạn là DevOps lead, setup Git workflow cho team 3 người.*

### Tasks (Các nhiệm vụ)

#### 1. Repository Setup (Thiết lập Repository)

- Create repository with proper structure (Tạo repo với cấu trúc phù hợp)
- Setup branch protection rules (Thiết lập protection rules)
- Create CONTRIBUTING.md
- Setup Merge Request template (GitLab) or PR template (GitHub)

#### 2. Implement Git Flow

```
main ────────────────────────────────
  │
  └── develop ───────────────────────
        │
        ├── feature/user-auth ──────
        │
        ├── feature/api-endpoints ──
        │
        └── release/1.0.0 ──────────
```

#### 3. Collaboration Features (Tính năng cộng tác)

- Create and review Merge Requests (GitLab) or Pull Requests (GitHub)
- Handle merge conflicts (Xử lý xung đột)
- Use conventional commits (Sử dụng conventional commits)
- Create releases with tags (Tạo releases với tags)

#### 4. Automation (Tự động hóa)

- Setup commit hooks (Thiết lập commit hooks)
- Create GitLab CI pipeline (Primary) or GitHub Actions workflow (Tạo pipeline CI)
- Automate changelog generation (Tự động tạo changelog)

---

## 📁 Project Structure (Cấu trúc dự án)

### For GitLab (Primary - Chính)

```
team-project/
├── .gitlab-ci.yml           # GitLab CI pipeline
├── src/
├── tests/
├── docs/
│   └── git-workflow.md
├── .gitignore
├── .gitattributes
├── CONTRIBUTING.md
├── CHANGELOG.md
└── README.md
```

### For GitHub (Alternative - Thay thế)

```
team-project/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── ISSUE_TEMPLATE/
├── src/
├── tests/
├── docs/
│   └── git-workflow.md
├── .gitignore
├── .gitattributes
├── CONTRIBUTING.md
├── CHANGELOG.md
└── README.md
```

---

## ✅ Deliverables (Sản phẩm bàn giao)

- [ ] Repository with complete setup (Repo với setup hoàn chỉnh)
- [ ] Branch protection configured (Đã cấu hình branch protection)
- [ ] 3+ merged MRs/PRs (3+ MR/PR đã merge)
- [ ] Release v1.0.0 with tag (Release v1.0.0 với tag)
- [ ] CI pipeline/workflow running (Pipeline/workflow đang chạy)
- [ ] Documentation complete (Tài liệu hoàn chỉnh)

---

**Good luck! 🚀**

*Chúc may mắn!*
