# 🌊 DigitalOcean — Tổng quan + Team/Project + doctl CLI

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.1\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 10/06/2026\
> **Level:** Basic (bài 00/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Đã xong [Cloud Fundamentals](../../../cloud-fundamentals/) ✅, hiểu Region/AZ/IaaS-PaaS-SaaS

> 🎯 *Bài đầu cluster DigitalOcean. Bạn đã quen AWS/GCP "siêu thị 250 services"; giờ học **DigitalOcean** — vendor cloud developer-first, ít service hơn nhưng giá predictable, UI thân thiện, công ty nhỏ-vừa và startup dùng cực nhiều. Bài này dạy: DO là gì, niche, Team/Project hierarchy, doctl CLI, pricing flat, hands-on Droplet đầu tiên.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **DO khác AWS/GCP** ở điểm nào, vì sao chọn DO
- [ ] Biết **các services tier 1** của DO (nhóm Compute/Storage/Database/Network/Ops) và analog với AWS
- [ ] Tạo **DO account** an toàn (2FA, billing alert, Team setup)
- [ ] Hiểu **Team → Project → Resource** hierarchy
- [ ] Cài đặt **doctl CLI** + auth + context
- [ ] Hiểu **Tier Pricing** flat / predictable của DO
- [ ] Deploy 1 **Droplet đầu tiên** (smallest tier)

---

## Tình huống — Sếp giao xây "side project" budget thấp

Sáng thứ Hai, sếp gửi message:

> *"Mình muốn build 1 internal tool nhỏ cho team — FastAPI backend + Postgres + UI. Budget $50/tháng tối đa. AWS phức tạp quá, mỗi lần bill ra mình toát mồ hôi. Tìm cloud nào dễ tính, giá rõ ràng, deploy nhanh giúp mình."*

Bạn nghĩ ngay tới **DigitalOcean**:
- Pricing flat — $6 Droplet là $6, không có "data transfer fee surprises".
- UI thân thiện, deploy Droplet trong 30 giây.
- Marketplace có sẵn "1-Click Apps" (Postgres, Node, Docker).
- Doc rõ ràng, community tutorials chất lượng cao (DO tutorials nổi tiếng từ 2014).

Vấn đề: bạn chưa biết DO khác AWS chỗ nào, "Project" trong DO khác "Project" GCP ra sao, doctl gõ thế nào. Bài này lấp đầy.

---

## 1️⃣ DigitalOcean là gì, khác AWS/GCP thế nào

🪞 **Ẩn dụ**: *AWS như **siêu thị Walmart 200 mặt hàng** — có tất cả nhưng dễ lạc; GCP như **cửa hàng kỹ sư Google** — tinh, ít món, nặng về data/AI; DigitalOcean như **tiệm tạp hóa của developer** — chỉ có món bạn dùng hàng ngày, giá niêm yết rõ, chủ tiệm vui vẻ, không "hidden fee".*

### Định nghĩa

**DigitalOcean** (DO) = nhà cung cấp cloud Mỹ ra đời 2011, IPO 2021, niche **developer-first** + **small/medium business**. Hiện ~5% market share global (sau AWS/Azure/GCP/Alibaba) nhưng top-3 trong segment **startup + SMB + indie hacker**.

### Điểm mạnh DO 2026

| Điểm mạnh | Vì sao | Ví dụ |
|---|---|---|
| **Pricing predictable** | Tier flat — $6/$12/$24 Droplet, không "bill bomb" cuối tháng | $6 Basic Droplet 1vCPU/1GB/25GB SSD/1TB transfer |
| **UX đơn giản** | UI thân thiện, ít option rối, deploy 30 giây | Tạo Droplet 3 click |
| **Developer experience** | Doc + tutorial chất lượng, community lớn | DigitalOcean Community (5M+ articles) |
| **App Platform PaaS** | Build từ Git auto, alternative Heroku | Push code → deploy live URL |
| **Managed services** | Postgres/MySQL/Redis/Mongo/Kafka one-click | Production-ready trong 5 phút |
| **Bandwidth generous** | Bandwidth tính theo tier (1TB cho Basic), không tính per-GB | Tiết kiệm 5-10x so AWS egress |
| **Marketplace 1-Click** | Pre-built images cho 100+ app | Deploy WordPress/n8n/Plausible 1 click |

### Điểm yếu / Trade-off

| Yếu | Hệ quả |
|---|---|
| Ít service hơn nhiều (~30 vs 250+ AWS) | Niche workload phức tạp thiếu lựa chọn (vd: không có queue managed như SQS; có Functions serverless nhưng hệ sinh thái event-source/trigger kém phong phú hơn Lambda) |
| Region ít (~15 vs AWS 30+) | Latency vùng xa (Việt Nam ping SGP1 OK, US workload mới mượt) |
| Enterprise features yếu | SLA, compliance (HIPAA, FedRAMP) hạn chế hơn AWS/Azure |
| Không có niche specialized (TPU, Quantum, Satellite) | Workload đặc thù không có |
| Auto-scale cơ bản | ASG-like nhưng không advanced như AWS |

### Khi nào chọn DO

| Use case | Chọn DO nếu |
|---|---|
| Side project / MVP / startup early | Budget thấp, deploy nhanh, predictable bill |
| Internal tool công ty SMB | Team < 50 người, không cần enterprise SLA |
| Indie hacker / freelancer | Cần host đơn giản, giá rõ |
| App Platform PaaS (alternative Heroku) | Push Git → deploy live |
| K8s học tập | DOKS rẻ (control plane free, chỉ trả tiền worker node) |
| Bandwidth-heavy app | Bandwidth allotment thoải mái |
| Workload cần migrate từ Heroku/Render | Tương đồng UX |

### Khi nào KHÔNG chọn DO

- Enterprise scale > 1000 employees → AWS/Azure/GCP
- Workload cần ML/AI advanced (TPU, custom silicon) → GCP/AWS
- Compliance HIPAA/FedRAMP/PCI strict → AWS (DO có HIPAA nhưng option hạn chế)
- Cần global presence > 20 regions → AWS/GCP
- Cần niche service (FinTech rails, Satellite, IoT Core) → AWS

---

## 2️⃣ DO Services tier 1 (must-know)

DO có ~30 services. **Tier 1** (cần biết ngay) = nhóm services chiếm 95% workload, liệt kê đầy đủ theo 5 mảng bên dưới (Compute / Storage / Database / Network / Identity & Ops).

### Compute (tính toán)

| Service | Mô tả | Analog AWS | Khi dùng |
|---|---|---|---|
| **Droplet** | VM truyền thống | EC2 | App backend, VM tùy biến, lift-and-shift |
| **App Platform** | PaaS auto-build từ Git | Elastic Beanstalk / Heroku | Web app modern, không muốn quản OS |
| **Functions** | Serverless function | Lambda | Event-driven, ngắn (< 15 phút) |
| **Kubernetes (DOKS)** | Managed K8s | EKS | Microservices, K8s team |

### Storage (lưu trữ)

| Service | Mô tả | Analog AWS |
|---|---|---|
| **Spaces** | Object storage S3-compatible | S3 |
| **Volumes** | Block storage attach to Droplet | EBS |
| **Snapshots** | Point-in-time backup Droplet/Volume | EBS Snapshot |
| **Container Registry** | Private Docker registry | ECR |

### Database

| Service | Mô tả | Analog AWS |
|---|---|---|
| **Managed Postgres** | Postgres managed + standby + backup | RDS Postgres |
| **Managed MySQL** | MySQL managed | RDS MySQL |
| **Managed Redis** | Redis managed | ElastiCache |
| **Managed MongoDB** | MongoDB managed | DocumentDB |
| **Managed Kafka** | Kafka managed (2024+) | MSK |

### Network

| Service | Mô tả | Analog AWS |
|---|---|---|
| **VPC** | Virtual private network per region | VPC |
| **Load Balancer** | L4/L7 LB managed | ELB |
| **Reserved IP** (Floating IP) | Static IP có thể remap | Elastic IP |
| **Firewall** | Cloud firewall (security group) | Security Group |
| **DNS** | Managed DNS | Route 53 |

### Identity & Ops

| Service | Mô tả | Analog AWS |
|---|---|---|
| **Team** | Container quản lý multi-user, billing | AWS Organization |
| **Project** | Group resources logic | (no direct analog) |
| **Personal Access Token (PAT)** | API key | IAM access key |
| **Monitoring** (built-in) | Free metric + alert | CloudWatch (free tier) |

→ **Học bài 01-04** cluster basic: Droplet+Volume, Spaces+CDN, Managed DB, App Platform+Functions.

---

## 3️⃣ Resource hierarchy — Team → Project → Resource

DO **đơn giản hơn AWS/GCP** ở chỗ chỉ có **2 cấp**: Team và Project.

```
Team: "Acme Engineering"           ← gắn billing + multi-user
├── Project: "acmeshop-prod"
│   ├── Droplet "web-1"
│   ├── Volume "data-1"
│   ├── Managed DB "postgres-prod"
│   └── Spaces "acmeshop-uploads"
├── Project: "acmeshop-staging"
│   └── Droplet "web-staging"
└── Project: "internal-tools"
    └── App Platform "dashboard"
```

### Các level

| Level | Mô tả | Tương đương AWS / GCP |
|---|---|---|
| **Team** | Top-level — gắn billing + invite member | AWS Organization / GCP Org |
| **Project** | Group resources logic (theo app/env) | AWS tag-based grouping / GCP Project (gần nhất) |
| **Resource** | Droplet, Volume, DB, ... cụ thể | (same) |

### Vì sao DO đơn giản hơn

- DO **không có "Account"** isolation như AWS — mọi resource trong cùng Team chia chung billing.
- **Project chỉ là logical grouping** — không isolate billing/permission như AWS Account hay GCP Project.
- Permission control theo **Team Role** (Owner / Member / Biller / Resource Viewer), không granular như IAM.

> ⚠️ **Hệ quả**: DO **không phù hợp** cho enterprise cần strict isolation giữa env (prod/staging) ở mức billing/IAM. Workaround: tạo **multiple Teams** (1 Team prod, 1 Team staging) — invite cùng user, billing tách.

### Vì sao "Project" vẫn quan trọng

Dù không isolate, Project vẫn dùng để:
- Group resource trên UI cho dễ nhìn.
- Bật/tắt notification per project.
- Tag resource cho cost report.
- Apply default firewall/tag.

→ **Thực hành**: tạo 1 Project cho mỗi `<app>-<env>` (e.g., `acmeshop-prod`, `acmeshop-staging`).

---

## 4️⃣ Tạo DO account + secure baseline

### Bước 1 — Tạo account

1. Truy cập [digitalocean.com](https://www.digitalocean.com) → "Sign up".
2. Đăng ký bằng email/Google/GitHub.
3. Verify email + add credit card hoặc PayPal.
4. Nhận **free credit** khi đăng ký mới (mức tiền + thời hạn thay đổi theo chương trình/khu vực — xem trang signup để biết ưu đãi hiện hành).

### Bước 2 — Bật 2FA

**Bắt buộc** trước khi làm gì khác:
1. Settings → Security → Two-Factor Authentication.
2. Dùng **Authenticator app** (Google Authenticator, Authy, 1Password) — **không** dùng SMS.
3. Lưu backup codes offline (KeePass / 1Password vault).

### Bước 3 — Tạo Team (nếu nhiều người dùng)

1. Settings → Teams → Create New Team.
2. Tên Team: `Acme Engineering`.
3. Invite member với role:
   - **Owner**: full control (deploy + billing + invite).
   - **Member**: deploy resource, không invite/billing.
   - **Biller**: chỉ xem billing.
   - **Resource Viewer**: read-only.

### Bước 4 — Setup billing alert

```
Billing → Billing alerts → Create alert
- Set threshold: $20 / $50 / $100 / $200
- Email khi đạt mốc
```

**Quan trọng**: DO **không tự tắt** Droplet khi quá budget — chỉ gửi email. Phải có **kill switch script** (cron + doctl) nếu muốn hard cap.

### Bước 5 — Setup Personal Access Token (PAT) cho doctl

1. API → Personal Access Tokens → Generate New Token.
2. Tên: `doctl-local-dev`.
3. Scope: **Full Access** (cho dev) hoặc **Custom** (read-only cho monitoring).
4. Expiration: 90 ngày (rotate định kỳ).
5. Copy token (chỉ show 1 lần) → lưu vào password manager.

### Bước 6 — Không share PAT trong code/Git

- **NEVER** commit PAT vào Git public/private.
- Lưu trong `~/.config/doctl/config.yaml` (doctl tự manage) hoặc env var `DIGITALOCEAN_ACCESS_TOKEN`.
- Dùng **`gitleaks`** hook check trước commit.

---

## 5️⃣ doctl CLI — Cài đặt + auth + context

### Cài đặt

```bash
# macOS
brew install doctl

# Linux (snap)
sudo snap install doctl

# Linux (binary) — thay version bằng bản mới nhất tại github.com/digitalocean/doctl/releases
cd ~ && wget https://github.com/digitalocean/doctl/releases/download/v1.160.1/doctl-1.160.1-linux-amd64.tar.gz
tar xf doctl-*.tar.gz
sudo mv doctl /usr/local/bin

# Windows (scoop)
scoop install doctl

# Verify
doctl version
```

### Auth — Init context

```bash
# Init với PAT (interactive)
doctl auth init

# Paste PAT khi prompt
# > Validating token... ✓
```

Context lưu tại `~/.config/doctl/config.yaml`. Có thể init nhiều context cho nhiều Team.

### Context — Multi-account setup

```bash
# Init context "work"
doctl auth init --context work
# Paste work PAT

# Init context "sandbox"
doctl auth init --context sandbox
# Paste sandbox PAT

# List contexts
doctl auth list

# Switch context
doctl auth switch --context sandbox

# Default context (no --context flag)
doctl auth switch --context default
```

### Common commands

```bash
# List Droplets
doctl compute droplet list

# List regions
doctl compute region list

# List sizes (Droplet types)
doctl compute size list

# List SSH keys
doctl compute ssh-key list

# List Projects
doctl projects list

# Account info
doctl account get

# Get account balance
doctl balance get
```

### doctl trong CI/CD

```bash
# Set token via env var (không cần auth init)
export DIGITALOCEAN_ACCESS_TOKEN="dop_v1_xxxxx"
doctl compute droplet list

# GitHub Actions: dùng official action
# - uses: digitalocean/action-doctl@v2
#   with:
#     token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
```

---

## 6️⃣ Tier Pricing — DO bảng giá flat

DO nổi tiếng vì **pricing predictable**. Cùng 1 Droplet size = cùng 1 giá ở mọi region (trừ vài region đặc biệt).

### Droplet Basic (shared CPU) — phổ biến nhất

| Tier | vCPU | RAM | SSD | Transfer | Giá/tháng |
|---|---|---|---|---|---|
| **s-1vcpu-512mb-10gb** | 1 | 512 MB | 10 GB | 500 GB | $4 |
| **s-1vcpu-1gb** | 1 | 1 GB | 25 GB | 1 TB | $6 |
| **s-1vcpu-2gb** | 1 | 2 GB | 50 GB | 2 TB | $12 |
| **s-2vcpu-2gb** | 2 | 2 GB | 60 GB | 3 TB | $18 |
| **s-2vcpu-4gb** | 2 | 4 GB | 80 GB | 4 TB | $24 |
| **s-4vcpu-8gb** | 4 | 8 GB | 160 GB | 5 TB | $48 |

### Premium Intel / AMD (dedicated CPU portion)

Giá cao hơn ~20% so Basic shared, nhưng latency CPU ổn định hơn (không bị "noisy neighbor"). Suffix `-intel` hoặc `-amd`.

### Managed Database

| Tier | RAM | vCPU | Storage | Giá/tháng |
|---|---|---|---|---|
| **Basic** (single node, dev) | 1 GB | 1 | 10 GB | $15 |
| **Basic** (single node) | 2 GB | 1 | 25 GB | $30 |
| **Pro** (HA standby) | 4 GB | 2 | 50 GB | $120 |

### Spaces (Object Storage)

- **$5/tháng** flat: 250 GB storage + 1 TB outbound transfer.
- Vượt: $0.02/GB storage, $0.01/GB transfer.

### Load Balancer

- **$12/tháng** small (10k concurrent connections).
- $24 medium, $48 large.

### So với AWS — Ví dụ "$10 Droplet" tương đương

| Item | DO | AWS EC2 ước lượng |
|---|---|---|
| 1 vCPU, 2GB RAM, 50GB SSD | $12/tháng flat | t3.small (~$15) + EBS 50GB (~$4) = $19 |
| Bandwidth 2 TB/tháng | Free (in tier) | EC2: $180 outbound transfer (US, $0.09/GB) |
| Backup automated | +20% ($2.40) | EBS snapshot ($0.05/GB-month) |
| **Tổng (real workload)** | **~$15** | **~$200** |

→ **Đây là lý do** DO thắng AWS cho indie/SMB: bandwidth là killer.

> ⚠️ DO cũng tính bandwidth overage **nhưng** rất rộng ($0.01/GB so AWS $0.09).

---

## 🛠️ Hands-on — Tạo Droplet đầu tiên

### Mục tiêu

Tạo 1 Droplet $6 basic, SSH vào, chạy 1 lệnh, rồi destroy. Toàn bộ < 5 phút.

### Bước 1 — Add SSH key

```bash
# Generate key pair (nếu chưa có)
ssh-keygen -t ed25519 -C "thien.le@acmeshop.vn" -f ~/.ssh/do_ed25519

# Upload public key lên DO
doctl compute ssh-key import do-main \
    --public-key-file ~/.ssh/do_ed25519.pub

# Get fingerprint key
doctl compute ssh-key list
# Sample output:
# ID         Name      FingerPrint
# 12345678   do-main   aa:bb:cc:dd:...
```

### Bước 2 — Tạo Droplet

```bash
# Get region + size + image list (optional, để biết slug)
doctl compute region list --format Slug,Name
doctl compute size list --format Slug,Memory,VCPUs,Disk,PriceMonthly | head -20
doctl compute image list-distribution --format Slug,Distribution,Name | grep ubuntu-24

# Tạo Droplet
doctl compute droplet create acmeshop-test \
    --region sgp1 \
    --size s-1vcpu-1gb \
    --image ubuntu-24-04-x64 \
    --ssh-keys aa:bb:cc:dd:... \
    --wait

# Kết quả mong đợi:
# ID         Name             Public IPv4       Memory   VCPUs   Disk   Region
# 123456789  acmeshop-test    138.197.xxx.xxx   1024     1       25     sgp1
```

### Bước 3 — SSH vào

```bash
# Get IP từ output (hoặc list lại)
doctl compute droplet list --format Name,PublicIPv4

# SSH bằng private key
ssh -i ~/.ssh/do_ed25519 root@138.197.xxx.xxx

# Trong Droplet
echo "Hello from DigitalOcean!" > /tmp/hello.txt
cat /tmp/hello.txt
uname -a
exit
```

### Bước 4 — Add vào Project

```bash
# List projects
doctl projects list

# Get project ID
PROJ_ID=$(doctl projects list --format ID,Name --no-header | grep "acmeshop-prod" | awk '{print $1}')

# Move Droplet vào project
doctl projects resources assign "$PROJ_ID" \
    --resource=do:droplet:123456789
```

### Bước 5 — Destroy (tránh charge)

```bash
# Destroy Droplet
doctl compute droplet delete acmeshop-test --force

# Verify
doctl compute droplet list
```

→ **Kết quả**: bạn đã deploy + SSH + cleanup Droplet trong < 5 phút. Bill: ~$0.01 (charge theo giờ).

---

## 💡 Cạm bẫy thường gặp & Best practice

### 1. Để PAT leak

**Bẫy**: Commit PAT vào Git public → bot crypto miner exploit trong 1-2 giờ → bill $500-5000.

**Fix**:
- **Không commit** PAT bao giờ.
- Dùng `gitleaks` pre-commit hook.
- Rotate PAT mỗi 90 ngày.
- Scope PAT minimal (read-only nếu chỉ cần đọc).

### 2. Quên destroy Droplet sau khi test

**Bẫy**: Tạo Droplet $48 để load test → quên xóa → cuối tháng $48 bill.

**Fix**:
- Tag rõ resource sandbox: `--tag-name=sandbox,env=dev`.
- Cron daily list: `doctl compute droplet list --tag-name sandbox`.
- Script auto-destroy sau N giờ (xem recipes).

### 3. Bandwidth overage bị bất ngờ

**Bẫy**: App có CDN-heavy → vượt 1TB free Basic Droplet → bị tính $0.01/GB → $100+ surprise bill.

**Fix**:
- Monitor bandwidth: `doctl monitoring metrics droplet bandwidth-inbound|outbound ...`.
- Dùng Spaces + CDN cho static asset thay vì serve trực tiếp từ Droplet.
- Cloudflare đứng trước (free) để giảm bandwidth Droplet.

### 4. Reserved IP để dở chừng

**Bẫy**: Tạo Reserved IP, gắn vào Droplet, sau xóa Droplet nhưng Reserved IP **không tự release** → bị charge $4/tháng dù không dùng.

**Fix**:
- Sau khi xóa Droplet → check `doctl compute reserved-ip list` → delete nếu không cần.
- Note: Reserved IP **gắn vào Droplet thì FREE**, **không gắn ai** thì $4/tháng.

### 5. Snapshot tích lũy

**Bẫy**: Auto-backup Droplet bật → snapshot tích lũy → 50 snapshot × 25GB = bill nặng.

**Fix**:
- Lifecycle: giữ tối đa 4 weekly snapshots, prune cũ.
- `doctl compute snapshot list` → review định kỳ.

### 6. Region nhầm cho user VN

**Bẫy**: Tạo Droplet ở `nyc1` (US East) cho user VN → ping 250ms.

**Fix**:
- VN/SEA user → `sgp1` (Singapore).
- EU user → `fra1` (Frankfurt) hoặc `ams3` (Amsterdam).
- US user → `nyc1`/`nyc3`/`sfo3`.

### 7. Dùng root SSH thay vì user thường

**Bẫy**: Droplet mặc định login `root` → brute-force SSH dễ trúng.

**Fix**:
- Sau setup: tạo user thường (`adduser deploy`), add sudo, disable root SSH (`PermitRootLogin no` trong `/etc/ssh/sshd_config`).
- Cloud-init script tự setup user khi tạo Droplet (xem bài 01).

### 8. Project chỉ là cosmetic — nhầm tưởng isolate

**Bẫy**: Tưởng Project trong DO isolate billing/permission như GCP Project → vẫn share billing chung Team.

**Fix**:
- Cần isolate billing thật → tạo **multiple Teams**, mỗi Team 1 billing account riêng.
- Cần isolate IAM → DO Team role chỉ có 4 level, không granular như AWS IAM.

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** DO và AWS khác nhau ở điểm cốt lõi nào?

<details>
<summary>💡 Đáp án</summary>

- **Số lượng service**: DO ~30 vs AWS 250+. DO tập trung core "developer toolkit".
- **Pricing**: DO flat tier, predictable. AWS pay-per-use, dễ "bill bomb" do bandwidth/transfer.
- **Audience**: DO = startup/SMB/indie. AWS = enterprise + everything.
- **UX**: DO UI đơn giản, ít option. AWS UI phức tạp, nhiều dropdown.

</details>

**Q2.** Team, Project, Resource trong DO khác Org/Folder/Project của GCP thế nào?

<details>
<summary>💡 Đáp án</summary>

- DO chỉ có 2 cấp logical: Team (billing + members) → Project (grouping cosmetic).
- GCP có 3 cấp: Org → Folder → Project (Project isolate billing + IAM thật).
- Hệ quả: DO Project KHÔNG isolate billing/IAM — workaround là tạo nhiều Team.

</details>

**Q3.** Tại sao bandwidth là điểm khác biệt lớn giữa DO và AWS?

<details>
<summary>💡 Đáp án</summary>

- DO tính bandwidth theo tier Droplet (Basic $6 → 1TB free, $48 → 5TB free). Vượt tier mới tính $0.01/GB.
- AWS tính per-GB egress ngay từ byte đầu ($0.09/GB out, varies by region).
- Workload bandwidth-heavy (video, file delivery) trên AWS = 5-10x chi phí so DO.

</details>

**Q4.** PAT bị leak nguy hiểm thế nào, cách phòng?

<details>
<summary>💡 Đáp án</summary>

- Bot scan GitHub liên tục, leak PAT exploit trong 1-2 giờ → spin Droplet GPU crypto miner → $500-5000/giờ.
- Phòng: không commit PAT, dùng env var, `gitleaks` hook, rotate 90 ngày, scope minimal (read-only nếu đủ).

</details>

**Q5.** Region nào DO phù hợp cho user Việt Nam?

<details>
<summary>💡 Đáp án</summary>

`sgp1` (Singapore) — ping VN ~30-50ms. Không có region VN nên SGP là tốt nhất. Tránh `nyc1`/`fra1` cho user VN (250ms+).

</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Mục đích | Lệnh |
|---|---|
| Auth init | `doctl auth init` |
| List Droplets | `doctl compute droplet list` |
| Tạo Droplet | `doctl compute droplet create NAME --region sgp1 --size s-1vcpu-1gb --image ubuntu-24-04-x64 --ssh-keys FP` |
| SSH | `ssh -i ~/.ssh/key root@IP` |
| Destroy Droplet | `doctl compute droplet delete NAME --force` |
| List regions | `doctl compute region list` |
| List sizes | `doctl compute size list` |
| List images | `doctl compute image list-distribution` |
| List projects | `doctl projects list` |
| Account info | `doctl account get` |
| Balance | `doctl balance get` |
| Switch context | `doctl auth switch --context NAME` |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **DigitalOcean (DO)** | (giữ nguyên) | Vendor cloud developer-first, ra đời 2011 |
| **Droplet** | (giữ nguyên) | VM của DO (analog EC2) |
| **Team** | Nhóm | Container quản lý multi-user + billing |
| **Project** | Dự án | Logical grouping resource (cosmetic, không isolate billing) |
| **doctl** | (giữ nguyên) | CLI chính của DO |
| **PAT** | Personal Access Token | API key của user |
| **Spaces** | (giữ nguyên) | Object storage S3-compatible |
| **Volumes** | Khối lưu trữ | Block storage attach Droplet (analog EBS) |
| **DOKS** | (giữ nguyên) | DigitalOcean Kubernetes Service |
| **App Platform** | (giữ nguyên) | PaaS auto-build từ Git |
| **Reserved IP** | IP cố định | Static IP có thể remap (cũ gọi Floating IP) |
| **Tier pricing** | Giá theo bậc | Pricing flat theo size, không pay-per-use chi tiết |
| **1-Click App** | Ứng dụng 1 cú click | Pre-built Droplet image cho 100+ app |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Cloud Fundamentals — Nền tảng điện toán đám mây](../../../cloud-fundamentals/)
- ➡️ **Bài tiếp theo:** [Droplet + Block Storage Volumes — Compute cơ bản DO](01_droplets-and-volumes.md)
- ↑ **Về cụm:** [DigitalOcean](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ [AWS basic](../../../aws/) — so sánh service analog
- ☁️ [GCP basic](../../../gcp/) — vendor #3, focus data/AI
- 🏗️ [IaC Terraform](../../../../10_devops/iac/) — Terraform DO provider
- 🧭 [Cloud Engineer roadmap](../../../../00_roadmaps/career/cloud-engineer_career-roadmap.md)

### 🌐 Tài nguyên tham khảo khác

- 📖 [DO docs](https://docs.digitalocean.com/)
- 📖 [doctl reference](https://docs.digitalocean.com/reference/doctl/)
- 📖 [DO Community tutorials](https://www.digitalocean.com/community/tutorials) — 5M+ articles, chất lượng cao
- 📖 [DO Marketplace](https://marketplace.digitalocean.com/) — 100+ 1-Click apps
- 📖 [DO Pricing](https://www.digitalocean.com/pricing)
- 📖 [DO Status page](https://status.digitalocean.com/)
- 📖 [DO Bandwidth Calculator](https://www.digitalocean.com/community/tools/bandwidth-calculator)
- 📖 [Comparison: DO vs AWS vs GCP](https://www.digitalocean.com/blog/digitalocean-vs-aws)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu. Bài 00 cluster DigitalOcean basic. Overview DO + niche developer/SMB + so sánh AWS/GCP + 12 services tier 1 + Team→Project hierarchy + doctl setup + Tier Pricing flat + hands-on Droplet + 8 pitfalls. Pattern theo AWS/GCP lesson 00.
- **v1.1.0 (01/06/2026)** — Đổi field metadata "Prerequisites" → "Yêu cầu trước"; chuẩn hoá Glossary header sang 3 cột "Thuật ngữ | Tiếng Việt | Giải thích"; chuẩn hoá nav (⬅️/➡️/↑ + link text = tiêu đề thực, 3 sub Định hướng/Chủ đề liên quan/Tài nguyên). Sửa mâu thuẫn nội bộ: DOKS control plane free (bỏ "$12"), DO có Functions serverless (gỡ ý "không có Lambda equivalent"). Làm mềm free credit signup (bỏ số cứng $200/60 ngày); cập nhật doctl v1.104.0 → v1.160.1 + ghi chú dùng bản mới nhất.
- **v1.1.1 (10/06/2026)** — Sửa mâu thuẫn số đếm services tier 1: bảng §2 liệt kê ~22 mục (4 Compute + 4 Storage + 5 Database + 5 Network + 4 Identity & Ops) nhưng văn bản ghi "10-12 services" / "~12 services". Bỏ con số cứng, đổi sang "các services tier 1 theo 5 nhóm" ở mục tiêu và lời dẫn §2.
