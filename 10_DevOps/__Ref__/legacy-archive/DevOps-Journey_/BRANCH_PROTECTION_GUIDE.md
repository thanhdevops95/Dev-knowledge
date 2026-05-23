# 🔒 Branch Protection Guide

> **Guide to setting up Branch Protection** on GitLab and GitHub.
>
> *Hướng dẫn thiết lập Branch Protection trên GitLab và GitHub.*

---

## 📋 Overview (Tổng quan)

After setting up Branch Protection Rules, only approved changes can be merged to `main`:

*Sau khi thiết lập Branch Protection Rules, chỉ các thay đổi được duyệt mới được merge vào `main`:*

- ❌ **No one** can push directly to `main` (Không ai có thể push trực tiếp)
- ❌ **No one** can merge without approval (Không ai có thể merge mà không có approval)
- ✅ Only approved **Merge/Pull Requests** can be merged (Chỉ MR/PR được duyệt mới merge được)

---

## 🦊 GitLab (Primary - Chính)

### Step 1: Access Project Settings (Truy cập Settings)

1. Open your GitLab project (Mở project GitLab)
2. Click **Settings** → **Repository** (Click Settings → Repository)
3. Expand **Protected branches** section (Mở rộng phần Protected branches)

Or navigate directly to (Hoặc truy cập trực tiếp):

```
https://gitlab.com/YOUR_USERNAME/YOUR_PROJECT/-/settings/repository
```

### Step 2: Add Protected Branch (Thêm Protected Branch)

1. Click **Add protected branch** (Click thêm protected branch)
2. Select **Branch**: `main`
3. Configure permissions (Cấu hình quyền):

| Setting | Recommended Value |
|---------|-------------------|
| **Allowed to merge** | Maintainers (hoặc Developers + Maintainers) |
| **Allowed to push and merge** | No one |
| **Allowed to force push** | ❌ Off |

1. Click **Protect** (Click Protect)

### Step 3: Configure Merge Request Approvals (Cấu hình MR Approvals)

1. Go to **Settings** → **Merge requests** (Vào Settings → Merge requests)
2. Find **Merge request approvals** section
3. Configure (Cấu hình):

| Setting | Recommended Value |
|---------|-------------------|
| **Approvals required** | 1 (or more) |
| **Require new approval when new commits** | ✅ Enabled |
| **Prevent committers from approving** | ✅ Enabled (optional) |

1. Click **Save changes**

### Result (Kết quả)

- Branch `main` shows 🔒 icon (Branch `main` có biểu tượng 🔒)
- All changes must go through Merge Request (Mọi thay đổi phải qua MR)
- At least 1 approval required (Cần ít nhất 1 approval)

---

## 🐙 GitHub (Alternative - Thay thế)

### Step 1: Access Repository Settings (Truy cập Settings)

1. Open your GitHub repository (Mở repository GitHub)
2. Click **Settings** tab (Click tab Settings)
3. In the left sidebar, click **Branches** (Click Branches)

Or navigate directly to (Hoặc truy cập trực tiếp):

```
https://github.com/YOUR_USERNAME/YOUR_REPO/settings/branches
```

### Step 2: Add Branch Protection Rule (Thêm Rule)

1. Click **Add branch protection rule** or **Add rule**
2. Enter **Branch name pattern**: `main`
3. Configure settings (Cấu hình):

| Option | Description (Mô tả) |
|--------|---------------------|
| ✅ **Require a pull request before merging** | Bắt buộc tạo PR để merge |
| ✅ **Require approvals** | Yêu cầu approvals (set = 1 or more) |
| ✅ **Dismiss stale pull request approvals when new commits are pushed** | Hủy approval nếu có commit mới |
| ✅ **Require status checks to pass before merging** | (Optional - nếu có CI/CD) |
| ✅ **Require conversation resolution before merging** | Bắt buộc resolve comments |
| ✅ **Do not allow bypassing the above settings** | Ngăn cả admin bypass |

1. Click **Create** or **Save changes**

### Result (Kết quả)

- Branch `main` shows 🔒 (Protected) badge
- Direct push is blocked (Push trực tiếp bị chặn):

  ```
  remote: error: GH006: Protected branch update failed
  ```

- Changes must go through Pull Request (Thay đổi phải qua PR)

---

## 🔄 Workflow After Protection (Quy trình sau khi bảo vệ)

```
┌─────────────────────┐     ┌─────────────────────┐
│   Feature branch    │     │   main (Protected)  │
│   (Your changes)    │     │        🔒           │
└─────────────────────┘     └─────────────────────┘
          │                           ↑
          │ 1. Create MR/PR           │ 4. Merge after approval
          └──────────────────────────►│
                                      │
          2. Request review ──────────┤
                                      │
          3. Get approval ────────────┤
```

### For GitLab (Với GitLab)

```bash
# 1. Create feature branch (Tạo feature branch)
git checkout -b feature/my-feature

# 2. Make changes and commit (Thay đổi và commit)
git add .
git commit -m "Add new feature"

# 3. Push branch (Push branch)
git push origin feature/my-feature

# 4. Create Merge Request on GitLab UI (Tạo MR trên GitLab)
# 5. Wait for approval (Chờ approval)
# 6. Merge on GitLab UI (Merge trên GitLab)

# 7. Clean up locally (Dọn dẹp local)
git checkout main
git pull origin main
git branch -d feature/my-feature
```

### For GitHub (Với GitHub)

```bash
# Same workflow, but create Pull Request instead of Merge Request
# (Tương tự, nhưng tạo Pull Request thay vì Merge Request)
```

---

## ❓ FAQ

### Q: Can I bypass if I'm the owner? (Tôi có thể bypass nếu là owner không?)

**GitLab**: Maintainers can push if "Allowed to push" is set to Maintainers.

*Maintainers có thể push nếu "Allowed to push" được set cho Maintainers.*

**GitHub**: You can if you don't enable "Do not allow bypassing".

*Bạn có thể nếu không bật "Do not allow bypassing".*

### Q: Who can approve? (Ai có thể approve?)

**GitLab**: Users with at least Developer role.

*Users có ít nhất role Developer.*

**GitHub**: Collaborators with Write or Admin access.

*Collaborators với quyền Write hoặc Admin.*

### Q: What if CI/CD fails? (Nếu CI/CD fail thì sao?)

If you enable "Require status checks to pass", the merge will be blocked until CI passes.

*Nếu bạn bật "Require status checks to pass", merge sẽ bị chặn cho đến khi CI pass.*

---

## 🔗 Official Documentation (Tài liệu chính thức)

- **GitLab**: [Protected Branches](https://docs.gitlab.com/ee/user/project/protected_branches.html)
- **GitLab**: [Merge Request Approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- **GitHub**: [About Protected Branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)

---

*Last Updated: 2025-12-30*

*Cập nhật lần cuối: 2025-12-30*
