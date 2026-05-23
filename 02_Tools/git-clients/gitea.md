# 🛠️ Gitea — Self-host git lightweight

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 23/05/2026\
> **Loại:** Tool individual — focused vào Gitea self-host\
> **Đọc trước:** [00_what-is-git-hosting.md](./00_what-is-git-hosting.md), (optional) [codeberg.md](./codeberg.md) — parent fork context

> 🎯 *Gitea = git hosting OSS **siêu nhẹ**, **single binary**, RAM < 100MB, **self-host** trên VPS rẻ / homelab. "GitHub-lite trong nhà bạn". Phù hợp solo dev / small team muốn full control.*

---

## Tình huống — Anh học K8s muốn lab GitOps tại nhà

Anh là DevOps junior, đang học K8s + GitOps (ArgoCD watch git repo → tự deploy). Anh setup homelab Raspberry Pi 5 chạy K8s. Cần git server để ArgoCD watch.

3 lựa chọn:
- **GitHub** — works, nhưng Pi cần internet ổn để pull. Bandwidth ISP giới hạn.
- **GitLab CE self-host** — 8 GB RAM minimum, Pi không kham nổi
- **Gitea** — single binary 50 MB, RAM < 100 MB, chạy mượt trên Pi 4. ⭐

Anh cài Gitea 5 phút. Push code → ArgoCD watch → K8s deploy. Toàn bộ lab tại nhà, không phụ thuộc cloud bên ngoài.

→ Đây là use case **chính** của Gitea: **self-host lightweight cho cá nhân/homelab**.

---

## 1️⃣ Vậy Gitea là gì?

**Gitea** (phát âm "git-TEA") = git hosting **OSS lightweight**, fork của **Gogs** (2016). **Single binary** (Go) — copy 1 file 50MB lên server → chạy.

**Số liệu 2026**:
- ~10,000+ instance self-host trên thế giới
- Memory footprint: ~50-100 MB RAM
- Single binary ~50 MB
- License: MIT (open source)
- Owner: Lonn Holdings (Hong Kong, for-profit từ 2022) — controversial

### Lịch sử + 3-way split

| Năm | Sự kiện |
|---|---|
| 2014 | **Gogs** ra đời (Go Git Service) — single binary git hosting |
| 2016 | Community fork → **Gitea** (governance OSS hơn Gogs) |
| 2022 | Gitea bị mua bởi Lonn Holdings (Hong Kong, for-profit) |
| 2022 | Community lo lắng → hardfork → **Forgejo** |
| Nay | Gitea, Forgejo, Codeberg tồn tại song song |

→ **Hiện trạng 2026**:
- **Gitea** vẫn OSS + maintain bởi Lonn — many users vẫn dùng (legacy install)
- **Forgejo** = community-governed alternative
- **Codeberg** = instance cloud chạy Forgejo

### Pick Gitea hay Forgejo cho self-host?

| | **Gitea** | **Forgejo** |
|---|---|---|
| License | MIT | GPL-3.0 |
| Governance | Lonn Holdings (for-profit) | Forgejo organization (OSS) |
| Compatibility | Mature, ổn định | Hardfork 2022, đang catch up |
| Migration | (parent) | Có tool migrate từ Gitea → Forgejo |
| Community vibe | Mixed (governance concern) | OSS-loyal |

→ **Khuyến nghị 2026**:
- Đã có Gitea instance → giữ (chưa lý do strong để migrate)
- **Setup mới** → cân nhắc **Forgejo** (governance OSS hơn, future-proof)

> 💡 Bài này dùng "Gitea" làm chính nhưng **mọi setup + UI gần như identical cho Forgejo**. Chỉ khác URL download.

---

## 2️⃣ Gitea vs GitLab CE — Self-host showdown

| Tiêu chí | **Gitea** | **GitLab CE** |
|---|---|---|
| **RAM tối thiểu** | 100 MB ⭐ | 8 GB |
| **Disk** | 200 MB | 50+ GB |
| **Single binary?** | ✅ Có | ❌ (PostgreSQL + Redis + Sidekiq + Nginx + ...) |
| **Setup time** | 5 phút | 1-2 giờ |
| **Features** | Cơ bản (issue, PR, wiki, basic CI) | Đầy đủ (Actions, Registry, Monitor, Security scan, ...) |
| **Maintain** | Low (1 binary update) | High (database backup, multi-service) |
| **VPS cost** | $5/mo (1 GB RAM) đủ | $20+/mo (8 GB+ RAM) |
| **Phù hợp** | Solo / small team / homelab | Enterprise / 50+ users |

### Pick Gitea khi:

- ✅ Solo dev / nhỏ (< 10 user)
- ✅ VPS rẻ ($5/mo) hoặc homelab (Raspberry Pi)
- ✅ Cần git hosting đơn giản, không cần Container Registry / SAST / etc.
- ✅ Không muốn maintain database/Redis/Nginx tách
- ✅ Network restricted (cấm cloud public)

### Pick GitLab CE khi:

- ✅ Team 20+ user
- ✅ Cần CI/CD mạnh + Container Registry + monitoring
- ✅ Compliance requirement
- ✅ Có DevOps team maintain

---

## 3️⃣ Cài Gitea — 4 cách

### Option A — Docker (Khuyến nghị beginner)

```bash
# 1. Tạo folder data persist
mkdir -p ~/gitea/data

# 2. Chạy container
docker run -d \
  --name=gitea \
  --restart=always \
  -p 3000:3000 \
  -p 222:22 \
  -v ~/gitea/data:/data \
  -e USER_UID=1000 \
  -e USER_GID=1000 \
  gitea/gitea:latest

# 3. Verify
docker ps | grep gitea
```

→ Mở browser → `http://localhost:3000` → cài đặt qua wizard (§4).

### Option B — Docker Compose (Production)

```yaml
# docker-compose.yml
version: '3'

services:
  gitea:
    image: gitea/gitea:latest
    container_name: gitea
    restart: always
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - GITEA__database__DB_TYPE=postgres
      - GITEA__database__HOST=db:5432
      - GITEA__database__NAME=gitea
      - GITEA__database__USER=gitea
      - GITEA__database__PASSWD=<strong-password>
    networks:
      - gitea
    volumes:
      - ./gitea-data:/data
    ports:
      - "3000:3000"
      - "222:22"
    depends_on:
      - db

  db:
    image: postgres:16
    restart: always
    environment:
      - POSTGRES_USER=gitea
      - POSTGRES_PASSWORD=<strong-password>
      - POSTGRES_DB=gitea
    networks:
      - gitea
    volumes:
      - ./postgres-data:/var/lib/postgresql/data

networks:
  gitea:
```

```bash
docker compose up -d
```

> 💡 Default Gitea dùng SQLite — đủ cho personal. Production dùng Postgres như compose trên.

### Option C — Binary trực tiếp (Linux)

```bash
# 1. Download binary mới nhất
wget -O gitea https://dl.gitea.com/gitea/1.21.0/gitea-1.21.0-linux-amd64
chmod +x gitea

# 2. Run
./gitea web

# Default: http://localhost:3000
```

→ Có thể setup systemd service để chạy mãi:

```ini
# /etc/systemd/system/gitea.service
[Unit]
Description=Gitea
After=network.target

[Service]
Type=simple
User=git
WorkingDirectory=/home/git
ExecStart=/home/git/gitea web
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable gitea
sudo systemctl start gitea
```

### Option D — APT (Ubuntu/Debian community PPA)

```bash
# (Community PPA, không official)
curl -fsSL https://raw.githubusercontent.com/morphis/morphis-debian/master/install.sh | sudo bash
sudo apt install gitea
```

> ⚠️ Community PPA — verify maintainer trước khi cài.

---

## 4️⃣ First-run setup wizard

Lần đầu mở `http://localhost:3000`:

### Database

| Field | Value |
|---|---|
| **Database Type** | SQLite (personal) / PostgreSQL (production) / MySQL |
| **Database Host** | localhost / `db` (docker-compose) |
| **Database Name** | `gitea` |
| **Username + Password** | (from compose env) |

### General Settings

| Field | Value |
|---|---|
| **Site Title** | "My Gitea" |
| **Repository Root Path** | `/data/git/repositories` (default OK) |
| **Server Domain** | `localhost` hoặc `git.example.com` |
| **Gitea Base URL** | `http://localhost:3000` hoặc `https://git.example.com` |

### Email (optional, recommend)

| Field | Value |
|---|---|
| **SMTP Host** | smtp.gmail.com:587 hoặc Mailgun/Postmark/... |
| **SMTP From** | `noreply@example.com` |
| **SMTP User + Password** | (Gmail App Password hoặc API key) |

→ Setup email cho password reset + notification.

### Admin Account

**BẮT BUỘC tạo admin** ở bước này:
- Username: vd `admin`
- Password: strong
- Email: real

→ **Install Gitea** → done. Login với admin account.

---

## 5️⃣ User workflow

UI Gitea tương tự GitHub minimalist:

```
┌─────────────────────────────────────────┐
│ Dashboard │ Issues │ PRs │ Explore │ +  │
└─────────────────────────────────────────┘
```

### Tạo repo

1. `+` → **New Repository**
2. Owner + Repo Name
3. Visibility: Public / Private
4. Init README, .gitignore, License
5. Create

### Push từ local

```bash
cd ~/projects/myapp
git remote add origin git@gitea.local:<user>/myapp.git    # SSH port 222 nếu Docker
# Hoặc HTTPS:
git remote add origin http://localhost:3000/<user>/myapp.git

git push -u origin main
```

> ⚠️ Nếu Docker port 222 cho SSH, format URL khác:
> ```
> git remote add origin ssh://git@localhost:222/<user>/myapp.git
> ```

### SSH key setup

1. Profile (avatar top-right) → **Settings** → **SSH / GPG Keys**
2. Add public key
3. Test: `ssh -T git@localhost -p 222`

### PR workflow

Giống GitHub PR — không Smart Commits như Bitbucket, không Approval rules mạnh như GitLab. **Basic but works**.

---

## 6️⃣ Gitea Actions — CI/CD compatible

Gitea 1.19+ có **Actions** built-in, tương thích GitHub Actions yaml.

### `.gitea/workflows/test.yml`

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "Hello from Gitea Actions"
```

→ Cần **runner self-host**:

```bash
# Cài act_runner
wget -O act_runner https://gitea.com/gitea/act_runner/releases/download/v0.2.6/act_runner-0.2.6-linux-amd64
chmod +x act_runner

# Register với Gitea instance
./act_runner register --no-interactive --instance http://localhost:3000 --token <runner-token>

# Run
./act_runner daemon
```

Token lấy từ Site Administration → Actions → Runners.

→ Sau khi runner ready, push code → Actions tab show pipeline.

---

## 7️⃣ Backup + Maintain

### Backup SQLite (personal)

```bash
# Stop Gitea
sudo systemctl stop gitea     # hoặc docker stop gitea

# Copy data folder
tar czf gitea-backup-$(date +%Y%m%d).tar.gz ~/gitea/data

# Restart
sudo systemctl start gitea
```

### Backup PostgreSQL (production)

```bash
# Dump DB
docker exec gitea-db-1 pg_dump -U gitea gitea > gitea-db-$(date +%Y%m%d).sql

# Backup file storage
tar czf gitea-files-$(date +%Y%m%d).tar.gz ~/gitea/gitea-data
```

### Update Gitea version

```bash
# Docker
docker pull gitea/gitea:latest
docker compose down
docker compose up -d

# Binary
sudo systemctl stop gitea
wget -O gitea https://dl.gitea.com/gitea/<new-version>/gitea-<version>-linux-amd64
chmod +x gitea
sudo systemctl start gitea
```

> 💡 **Major version upgrade** (vd 1.20 → 1.21): đọc changelog, có thể có migration step.

---

## 💡 Pitfall thường gặp

### ❌ Pitfall: SSH port conflict với system SSH

```bash
docker run -p 22:22 gitea/gitea     # ❌ Conflict với host SSH
```

- **Hậu quả**: container không start hoặc host SSH bị block
- **Cách tránh**: dùng port khác (vd `222`), URL clone: `ssh://git@host:222/...`

### ❌ Pitfall: Không setup HTTPS — credentials leak

- HTTP plain → password git push qua mạng plain text → mạng public capture được
- **Cách fix**: setup HTTPS với:
  - Nginx reverse proxy + Let's Encrypt cert
  - Hoặc Caddy auto-HTTPS
  - Hoặc Cloudflare Tunnel

### ❌ Pitfall: Quên backup → mất data

- Self-host = bạn chịu trách nhiệm 100%. Disk fail = mất repo nếu không backup.
- **Cách tránh**:
  - Cron job backup hàng ngày → S3/Backblaze/external disk
  - Test restore định kỳ (3 tháng/lần)
  - Setup git remote mirror sang GitHub backup

### ❌ Pitfall: Không update version → security vuln

- Self-host = bạn maintain. Gitea có CVE → bạn phải update
- **Cách tránh**:
  - Subscribe security mailing list của Gitea
  - Update ít nhất major version mỗi 6 tháng
  - Docker tag `:latest` để auto-update khi rebuild

### ✅ Best practice: Mirror sang GitHub làm backup

```bash
# Trên repo Gitea, Settings → Repository Settings → Mirror
# Push mirror tới GitHub repo khác
# → Mọi push lên Gitea tự sync sang GitHub
```

→ Disk Gitea cháy → vẫn còn GitHub mirror.

---

## 🧠 Self-check

**Q1.** Gitea vs Forgejo vs Codeberg — phân biệt?

<details>
<summary>💡 Đáp án</summary>

- **Gitea** = software OSS, parent fork (Gogs → Gitea 2016)
- **Forgejo** = hardfork của Gitea 2022 (community lo for-profit drift), governance OSS hơn
- **Codeberg** = **instance cloud** chạy Forgejo engine (codeberg.org)

**Bạn dùng?**
- Self-host → cài **Gitea** hoặc **Forgejo** (recommend Forgejo cho governance OSS hơn)
- Cloud, không tự host → dùng **Codeberg** account

→ End user chỉ cần 1 trong 3. Forgejo + Gitea là software, Codeberg là instance.

</details>

**Q2.** Khi nào pick Gitea thay GitLab CE cho self-host?

<details>
<summary>💡 Đáp án</summary>

**Gitea (~100 MB RAM)** vs **GitLab CE (8+ GB RAM)** — chênh lệch 80x.

**Pick Gitea**:
- Solo dev / homelab / Raspberry Pi
- VPS rẻ ($5/mo, 1 GB RAM)
- Cần git hosting đơn giản — không cần Container Registry, SAST, monitor
- Không muốn maintain DB + Redis + Sidekiq

**Pick GitLab CE**:
- Team 20+ user
- Cần CI/CD mạnh + advanced features
- Có server hardware tốt (16 GB+ RAM)
- Có DevOps team maintain

→ Solo dev: Gitea 99% case. Enterprise: GitLab CE.

</details>

**Q3.** Mirror Gitea repo sang GitHub để làm gì?

<details>
<summary>💡 Đáp án</summary>

**3 lý do**:

1. **Backup external** — disk Gitea cháy, vẫn còn code trên GitHub
2. **Visibility** — recruiter / community thấy GitHub, không biết Gitea instance của bạn
3. **Public portfolio** — Gitea self-host private, GitHub public mirror

**Cách setup**: Gitea repo settings → Mirror → Push mirror → cấu hình GitHub repo + PAT.

→ Mọi `git push` lên Gitea tự sync sang GitHub. 1 source of truth + 1 backup/visibility.

</details>

---

## ⚡ Cheatsheet

### Cài Docker (1 lệnh)

```bash
docker run -d --name gitea \
  -p 3000:3000 -p 222:22 \
  -v ./gitea-data:/data \
  gitea/gitea:latest
```

### URLs

| URL | Đi đến |
|---|---|
| `<gitea-url>:3000` | Web UI |
| `<gitea-url>:3000/-/admin` | Site Administration (admin only) |
| `<gitea-url>:3000/<user>/<repo>` | Repo |
| `<gitea-url>:3000/<user>/<repo>/issues` | Issues |
| `<gitea-url>:3000/<user>/<repo>/pulls` | PRs |

### Backup

```bash
# SQLite + data
tar czf gitea-backup.tar.gz ./gitea-data

# Postgres
docker exec gitea-db pg_dump -U gitea gitea > backup.sql
```

### Common admin actions

| Action | Đường đi |
|---|---|
| Tạo user mới | Site Admin → Users → New User |
| Promote user thành admin | Site Admin → Users → edit → Administrator |
| Quota disk | Site Admin → Repositories → quotas |
| Setup OAuth (Google/GitHub login) | Site Admin → Authentication → New Source |

---

## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Gitea | (giữ EN) | Self-host git OSS, fork của Gogs |
| Gogs | (giữ EN) | Parent của Gitea (2014, ít maintain) |
| Forgejo | (giữ EN) | Hardfork Gitea 2022, governance OSS |
| Single binary | (giữ EN) | 1 file executable, không cần dependency |
| Self-host | Tự host | Cài + maintain trên server của bạn |
| Site Administration | (giữ EN) | UI quản admin Gitea (chỉ admin) |
| `act_runner` | (giữ EN) | Runner cho Gitea Actions |
| Repository mirror | Bản sao | Sync repo Gitea sang platform khác (vd GitHub) |
| OAuth | (giữ EN) | Login qua Google/GitHub thay password |

---

## 🔗 Liên kết & Tài nguyên

### Trong kho

- 🛠️ [00_what-is-git-hosting.md](./00_what-is-git-hosting.md) — So sánh git hosting
- 🛠️ [codeberg.md](./codeberg.md) — Forgejo cloud instance (engine bà con)
- 🛠️ [gitlab.md](./gitlab.md) — Alternative self-host nặng hơn
- 🐳 [Docker basics](../../10_DevOps/docker/lessons/01_basic/) — cần biết Docker để self-host

### Tài nguyên ngoài

- [gitea.com](https://gitea.com/) — chính thức (lưu ý: gitea.io đã thành gitea.com sau Lonn acquisition)
- [Gitea Docs](https://docs.gitea.com/) — chính thức
- [Forgejo Docs](https://forgejo.org/docs/) — alternative
- [act_runner GitHub](https://gitea.com/gitea/act_runner) — CI runner
- [Awesome Gitea](https://gitea.com/gitea/awesome-gitea) — community resources
- [Gitea Docker Hub](https://hub.docker.com/r/gitea/gitea) — official image
- [Migration Gitea → Forgejo](https://forgejo.org/docs/latest/admin/upgrade-from-gitea/)

---

## 📌 Changelog

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Tool individual #6 trong git-clients/ — **đóng cluster**. Cover: tình huống homelab K8s lab → §1 Gitea + 3-way split (Gogs/Gitea/Forgejo) → §2 vs GitLab CE (RAM 100MB vs 8GB) → §3 Cài 4 cách (Docker/Compose/Binary/APT) → §4 First-run wizard → §5 User workflow → §6 Gitea Actions + runner setup → §7 Backup + maintain + update. 5 pitfall + 3 self-check.
