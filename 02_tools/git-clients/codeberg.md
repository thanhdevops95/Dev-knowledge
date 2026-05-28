# 🛠️ Codeberg — Non-profit, ethical, free git hosting

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Loại:** Tool individual — focused vào Codeberg\
> **Đọc trước:** [00_what-is-git-hosting.md](./00_what-is-git-hosting.md)

> 🎯 *Codeberg = git hosting **non-profit**, dựa trên **Forgejo** (hardfork Gitea). KHÔNG tracking, KHÔNG AI train code bạn, KHÔNG vendor lock-in big-tech. Phù hợp OSS project + dev care ethical.*

---

## Tình huống — Maria không muốn code lên Microsoft

Maria là OSS dev viết tool cho cộng đồng Linux. Cô không muốn:
- Code public bị **Microsoft train Copilot** (GitHub Terms of Service cho phép)
- **Tracking pixel** từ Big Tech
- Phải verify SMS / phone với Microsoft
- Project OSS phụ thuộc vào platform của 1 corporation

Maria search "GitHub alternatives ethical" → tìm thấy **Codeberg**. Free, non-profit, OSS, dựa trên Forgejo. Cài thử → quá nhẹ, không có popup AI, không tracking. Maria yêu.

→ Bài này dạy bạn dùng Codeberg cho OSS project + privacy/ethical reasons.

---

## 1️⃣ Vậy Codeberg là gì?

**Codeberg** = git hosting **không lợi nhuận** (e.V. = registered non-profit Đức, Berlin). Thành lập 2019. Engine: **Forgejo** (hardfork Gitea OSS, được Codeberg sponsor).

**Số liệu 2026**:
- ~150,000 user (rất nhỏ so với GitHub 150M)
- ~250,000 repo
- Funding: donations + grants (NPO không quảng cáo, không VC)
- Đặc biệt phổ biến: dev Châu Âu, Linux/FOSS community

🪞 **Ẩn dụ**: Codeberg giống **Wikipedia của git hosting** — non-profit, do cộng đồng vận hành, không quảng cáo, không "free vì có data của bạn". Bạn pay bằng **donation** thay vì **data + attention**.

### Codeberg vs Forgejo vs Gitea — phân biệt

| | **Codeberg** | **Forgejo** | **Gitea** |
|---|---|---|---|
| Là gì | **Instance** chạy ở codeberg.org | **Software** chạy ở Codeberg + self-host được | **Software** Gitea (parent fork) |
| Tổ chức | Codeberg e.V. (NPO Đức) | Forgejo organization (community OSS) | Lonn Holdings (Hong Kong, for-profit 2022+) |
| Bạn dùng | Cloud hosting | Self-host (nếu muốn run Codeberg-like instance) | Self-host (nếu muốn parent Gitea) |
| Vì sao 3 cái? | 2022 Gitea bị mua bởi for-profit → community lo lắng → hardfork ra Forgejo. Codeberg dùng Forgejo. |

→ End user **chỉ cần biết Codeberg** = instance bạn dùng. Forgejo + Gitea là engine bên dưới.

---

## 2️⃣ Tại sao Codeberg? — Strengths

| Tiêu chí | GitHub | **Codeberg** |
|---|---|---|
| **Free unlimited** | ✅ | ✅ |
| **AI training opt-out** | Cần manual setting | ⭐ Default **không train** |
| **Tracking / ads** | Có ads cho Pro/Team | ⭐ **KHÔNG ads, KHÔNG tracking** |
| **Owned by** | Microsoft (for-profit) | NPO e.V. Đức |
| **Funding** | VC + revenue | Donations |
| **Open source platform** | ❌ (GitHub closed) | ✅ (Forgejo OSS) |
| **CI/CD** | Actions ⭐⭐⭐ | Forgejo Actions (compatible GHA syntax!) |
| **Migration GitHub → Codeberg** | N/A | ⭐ Built-in importer 1-click |
| **Thị phần** | 70% | <1% |
| **Cộng đồng VN** | ⭐⭐⭐ | (chưa có) |

### Pick Codeberg khi:

- ✅ **OSS project** không muốn corporate lock-in
- ✅ **Privacy concern** — không muốn data bị scrape/train AI
- ✅ **EU based** — GDPR-friendly (server Đức)
- ✅ **Donate-friendly** — ủng hộ NPO non-profit
- ✅ **Ethical tech** — chọn alternative cho Big Tech

### KHÔNG pick Codeberg khi:

- ❌ Career portfolio — recruiter VN scroll GitHub, không biết Codeberg
- ❌ AI-heavy workflow — không có Copilot
- ❌ Project commercial scale lớn — Codeberg không scale như Big Tech
- ❌ Cần Marketplace actions phong phú — Forgejo actions chưa rich như GitHub

---

## 3️⃣ Bước 1: Tạo account

1. Vào [codeberg.org](https://codeberg.org) → **Register**
2. Username (4-40 chars, alphanumeric + `_-`)
3. Email + password
4. **CAPTCHA** (có thể là math hoặc reCAPTCHA alternative)
5. Verify email

> 💡 **Approval workflow** (cuối 2023+): account mới có thể cần waiting period vài giờ để admin approve — chống spam/abuse. Đây là trade-off của NPO không có budget anti-spam như GitHub.

### Bật 2FA

1. **Settings** (avatar top-right) → **Security**
2. **Two-Factor Authentication** → Enable TOTP
3. Scan QR với authenticator app
4. Backup codes — lưu

### SSH key

1. Settings → **SSH / GPG Keys** → **Add Key**
2. Paste public key (`cat ~/.ssh/id_ed25519.pub`)
3. Test: `ssh -T git@codeberg.org`

### Access Token

1. Settings → **Applications** → **Generate New Token**
2. Token Name + scopes
3. Generate → copy

---

## 4️⃣ Tạo repository + push

### Web UI

1. **+** (top-right) → **New Repository**
2. Owner + Repo Name + Description
3. Visibility: Public / Private
4. Init README, .gitignore, License
5. **Create Repository**

### Push project local

```bash
cd ~/projects/myapp
git remote add origin git@codeberg.org:<user>/myapp.git
git branch -M main
git push -u origin main
```

### Repo UI (Forgejo-based)

```
┌─────────────────────────────────────────────────────────┐
│  Code │ Issues │ Pull Requests │ Releases │ Wiki │ ...  │
└─────────────────────────────────────────────────────────┘
```

Tương tự GitHub về layout, ít features hơn. Quen GitHub → dùng Codeberg dễ.

---

## 5️⃣ Pull Request workflow

Forgejo gọi là **Pull Request (PR)**, không **Merge Request** như GitLab.

### Flow giống GitHub

```bash
git checkout -b feature/add-search
# ... code + commit
git push -u origin feature/add-search
```

Trên web:
1. Banner "Compare & Pull Request" hiện
2. Click → điền title + description
3. Reviewers + Labels + Milestone
4. Create Pull Request

### Review + merge

- Diff view
- Inline comment
- **Approve** button
- Merge: Create merge commit / Squash / Rebase

---

## 6️⃣ Forgejo Actions — CI/CD compatible GitHub Actions

**Magic**: Forgejo Actions tương thích GitHub Actions yaml syntax — bạn có thể copy `.github/workflows/*.yml` từ GitHub repo qua **gần như nguyên xi**.

### `.forgejo/workflows/test.yml`

```yaml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: docker
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test
```

→ 99% giống GitHub Actions yaml. Chỉ khác:
- Path: `.forgejo/workflows/` thay `.github/workflows/`
- Runner: `docker` thay `ubuntu-latest`
- Một số action GitHub-specific không có (như `actions/cache@v3` cần Forgejo equivalent)

### Free runners

- Codeberg cung cấp shared runners free, nhưng **quota giới hạn** (community-funded)
- Heavy CI → self-host runner trên VPS bạn

---

## 7️⃣ Migrate từ GitHub sang Codeberg

Codeberg có **built-in importer**:

1. **+** → **New Migration**
2. Service: **GitHub**
3. **Clone Address**: URL repo GitHub
4. Authentication: username + PAT (cần PAT scope `repo:read`)
5. Options:
   - ✅ Issues
   - ✅ Pull requests
   - ✅ Releases
   - ✅ Wiki
   - ✅ Labels + Milestones
6. **Migrate Repository**

→ Sau vài phút, repo + history + issues + PR đầy đủ ở Codeberg.

> 💡 Limit: 50 issues/PR cho free account (chống spam). Repo siêu lớn cần multiple batches.

### Sau migrate

- Update `origin` remote local:
  ```bash
  git remote set-url origin git@codeberg.org:<user>/myapp.git
  ```
- Update CI yaml: `.github/workflows/` → `.forgejo/workflows/`
- Update README badges (CI badge URL khác)

---

## 💡 Pitfall thường gặp

### ❌ Pitfall: Account approval pending

- New account đôi khi pending approval admin (chống abuse). Có thể đợi vài giờ đến vài ngày.
- **Cách tránh**: tạo account sớm, dùng email reputation tốt (không tạm)

### ❌ Pitfall: Quota CI runner shared hết

- Shared runner Codeberg free, nhưng community-funded → có quota
- Heavy push → CI queue dài
- **Cách fix**: self-host runner trên VPS bạn (free, unlimited)

### ❌ Pitfall: Recruiter không biết Codeberg

- Career portfolio mà chỉ Codeberg → recruiter VN không biết, hỏi GitHub đâu
- **Cách tránh**: dual-host — Codeberg cho OSS, GitHub mirror cho visibility
  ```bash
  git remote add github git@github.com:<user>/myapp.git
  git push github main    # mirror sang GitHub
  ```

### ❌ Pitfall: Mong đợi feature parity với GitHub

- Codeberg/Forgejo nhỏ hơn — ít integration, ít app marketplace
- **Cách tránh**: chọn Codeberg với expectation "git hosting đơn giản + ethical", không thay GitHub fully

### ✅ Best practice: Donate khi dùng nhiều

- Codeberg là NPO, sống nhờ donation
- Nếu repo bạn dùng nhiều bandwidth/storage → consider donate
- [codeberg.org/Codeberg-e.V./Welcome](https://codeberg.org/Codeberg-e.V./Welcome) — info

---

## 🧠 Self-check

**Q1.** Tại sao có 3 thứ: Codeberg, Forgejo, Gitea?

<details>
<summary>💡 Đáp án</summary>

**Lịch sử**:
- **Gitea** (2016) = OSS lightweight git hosting (fork của Gogs)
- **2022**: Gitea bị mua bởi Lonn Holdings (Hong Kong, for-profit) — community lo lắng future
- **Cuối 2022**: community hardfork ra **Forgejo** (governance OSS thuần)
- **Codeberg** (instance từ 2019) chuyển sang dùng Forgejo engine 2022

**Phân biệt**:
- **Codeberg** = **instance cloud** (codeberg.org) bạn dùng — như github.com
- **Forgejo** = **software** chạy ở Codeberg (và bạn có thể self-host)
- **Gitea** = parent fork — vẫn tồn tại nhưng community lo về for-profit drift

→ Beginner chỉ cần biết "Codeberg" — instance để sign up + dùng. Forgejo + Gitea là engine.

</details>

**Q2.** Codeberg vs GitHub — khi nào pick Codeberg?

<details>
<summary>💡 Đáp án</summary>

**Pick Codeberg khi**:
- OSS project không muốn Big Tech control
- Privacy concern — không muốn code train AI
- EU-based, GDPR friendly
- Donate-friendly, ủng hộ ethical tech
- Tự host được (Forgejo OSS)

**KHÔNG pick khi**:
- Cần career portfolio (recruiter VN biết GitHub thôi)
- AI heavy (không Copilot)
- Marketplace integration phong phú
- Team commercial scale

→ Solution thực tế: **dual-host** — Codeberg primary + GitHub mirror cho visibility.

</details>

**Q3.** Forgejo Actions vs GitHub Actions khác nhau ra sao?

<details>
<summary>💡 Đáp án</summary>

**Tương thích ~99%** ở mức yaml syntax. Có thể copy `.github/workflows/*.yml` từ GitHub qua **gần như nguyên xi**.

**Khác biệt**:
- Path: `.forgejo/workflows/` thay `.github/workflows/`
- Runner identifier: `docker` thay `ubuntu-latest`
- Some GitHub-specific actions (vd `actions/cache`) cần Forgejo equivalent
- Marketplace nhỏ hơn — ít plugin community

→ Migration GitHub → Codeberg: yaml copy + thay path + thay runner name. Usually < 1 hour cho project trung bình.

</details>

---

## ⚡ Cheatsheet

| Action | Cách |
|---|---|
| Sign up | codeberg.org/user/sign_up |
| 2FA | Settings → Security → Enable TOTP |
| SSH key | Settings → SSH/GPG Keys → Add Key |
| Access Token | Settings → Applications → Generate Token |
| Tạo repo | `+` → New Repository |
| Migrate từ GitHub | `+` → New Migration → service GitHub |
| Setup CI | Tạo `.forgejo/workflows/*.yml` |
| Self-host runner | [forgejo.org/docs/latest/admin/actions/](https://forgejo.org/docs/latest/admin/actions/) |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Codeberg | (giữ EN) | Instance cloud non-profit (codeberg.org) |
| Forgejo | (giữ EN) | Software OSS chạy Codeberg, hardfork Gitea |
| Gitea | (giữ EN) | Parent fork của Forgejo |
| NPO / e.V. | Tổ chức phi lợi nhuận / Eingetragener Verein | Codeberg e.V. (Đức) |
| Hardfork | (giữ EN) | Fork với governance độc lập, không quay lại merge với parent |
| Forgejo Actions | (giữ EN) | CI/CD tương thích GitHub Actions syntax |
| Migration | Di trú | Import repo từ platform khác |
| Approval workflow | Quy trình duyệt | New account chờ admin approve |

---

## 🔗 Liên kết & Tài nguyên

### Trong kho

- 🛠️ [00_what-is-git-hosting.md](./00_what-is-git-hosting.md) — So sánh git hosting
- 🛠️ [github.md](./github.md) — GitHub user guide
- 🛠️ [gitea.md](./gitea.md) — Gitea self-host (parent của Forgejo)

### Tài nguyên ngoài

- [Codeberg.org](https://codeberg.org/) — sign up
- [Codeberg Documentation](https://docs.codeberg.org/) — chính thức
- [Forgejo Documentation](https://forgejo.org/docs/) — engine docs
- [Forgejo Actions Guide](https://forgejo.org/docs/latest/user/actions/)
- [Codeberg-e.V.](https://codeberg.org/Codeberg-e.V./Welcome) — about NPO, donate
- [Awesome Codeberg](https://codeberg.org/momar/awesome-codeberg) — community projects
- [Migration FAQ](https://docs.codeberg.org/getting-started/migrating-repos-from-github/)

---

## 📌 Changelog

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Tool individual #5 trong git-clients/. Cover: tình huống Maria dev OSS không thích Microsoft → §1 Codeberg là gì + phân biệt Codeberg/Forgejo/Gitea → §2 vs GitHub (5 pick + 4 không pick) → §3 Account + 2FA + SSH → §4 Repo + push → §5 PR workflow → §6 Forgejo Actions compatible GitHub Actions → §7 Migrate từ GitHub built-in importer. 5 pitfall + 3 self-check.
