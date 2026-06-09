# ☁️ Cloudflare — Tổng quan, account hierarchy, wrangler CLI

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 01/06/2026\
> **Level:** Basic (bài 00/5)\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** Đã xong [Cloud Fundamentals](../../../cloud-fundamentals/) ✅, hiểu CDN/DNS cơ bản, đã từng dùng `curl`

> 🎯 *Bài đầu tiên của Cloudflare cluster. Bạn đã quen AWS/GCP — vendor "data-center-centric". Cloudflare là một paradigm khác: **edge-first**, mọi thứ chạy ở 320+ POPs phủ khắp thế giới trước cả khi chạm origin. Bài này dạy: Cloudflare là gì, 3 trụ cột (Network/Security/Developer Platform), Account+Zone hierarchy, wrangler CLI, Free Tier "ngông nghênh" so với AWS/GCP, và deploy first Worker trong 5 phút.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **Cloudflare khác AWS/GCP** ở điểm nào (edge-first vs region-first)
- [ ] Biết **3 trụ cột** Cloudflare và services tier 1 trong mỗi trụ
- [ ] Tạo **Cloudflare account** an toàn (MFA, API token scoping)
- [ ] Hiểu **Account → Zone → Resource** hierarchy + multi-tenant model
- [ ] Cài đặt **wrangler CLI** + auth + multi-account
- [ ] Biết **Free Tier 2026** Cloudflare cho gì (rất rộng so với competitors)
- [ ] Deploy **first Worker** "Hello World" lên edge global trong 5 phút

---

## Tình huống — Bạn được giao migrate Acme Shop từ AWS sang Cloudflare

Sáng thứ Hai, sếp gọi vào meeting:

> Sếp: *"Tháng vừa rồi AWS bill bên mình $4200, riêng CloudFront + Data Transfer Out đã chiếm $2800. Khách Acme Shop ở Việt Nam, Indonesia, Philippines mà CDN lại tính per-GB egress đắt kinh khủng. Bên dev khuyên thử Cloudflare — họ bảo egress R2 = $0, Workers thay được Lambda, cả WAF lẫn DDoS free. Bạn nhận task migrate. Tuần này làm POC trước."*

Bạn login Cloudflare dashboard lần đầu → bị lạ:
- Không có "region selector" như AWS — sao service không cần chọn region?
- "Zone" là gì? Khác "Project" của GCP thế nào?
- API token vs Global API key — dùng cái nào?
- wrangler CLI deploy Workers — Workers chạy ở đâu nếu không có region?
- DNS chuyển qua Cloudflare có khác gì so với Route 53?
- Free Tier nói "unmetered DDoS protection" — thật không?

→ Bài này lấp đầy: Cloudflare paradigm + setup baseline + wrangler working + first Worker live.

---

## 1️⃣ Cloudflare là gì — vì sao "edge-first" thay đổi paradigm

🪞 **Ẩn dụ**: *AWS/GCP như **chuỗi siêu thị lớn ở vài thành phố** — bạn muốn mua hàng phải đi tới siêu thị (region). Cloudflare như **mạng 7-Eleven phủ khắp mọi phường** — chỗ nào cũng có cửa hàng gần, lấy hàng trong 30 giây. Bạn không "deploy tới region nào" — bạn deploy 1 lần, Cloudflare tự đồng bộ tới 320+ cửa hàng khắp thế giới.*

### Định nghĩa

**Cloudflare** = công ty hạ tầng internet thành lập 2009, ban đầu là DDoS protection + CDN. Hiện sở hữu **mạng edge lớn nhất thế giới**: **320+ POPs** (Points of Presence) ở **120+ quốc gia**, trong vòng 50ms latency của 95% dân số online toàn cầu.

Khác AWS/GCP, Cloudflare **không phân loại theo region**. Mọi service deploy 1 lần → tự đẩy ra toàn bộ POP. Request từ user vào POP gần nhất xử lý ngay tại đó — chỉ chạm origin (AWS S3, server bạn, ...) khi thực sự cần.

### So sánh paradigm

| Tiêu chí | AWS/GCP/Azure (region-first) | Cloudflare (edge-first) |
|---|---|---|
| **Unit deploy** | Region (`us-east-1`, `asia-southeast1`) | Toàn cầu — 1 lần là khắp 320+ POP |
| **Latency model** | User → nearest region (50-200ms) | User → nearest POP (5-30ms) |
| **Compute** | VM/container/Lambda trong region | Workers (V8 isolate) tại mỗi POP |
| **Storage** | Đặt resource ở 1-2 region | R2 multi-region; KV/D1 replicated khắp edge |
| **Pricing model** | Per-resource + heavy egress fee | Flat per-request + **zero egress** cho R2 |
| **DDoS / WAF** | Tính phí riêng | **Free unmetered DDoS** Layer 3/4 |
| **CDN** | CloudFront/Cloud CDN — add-on | **Built-in** — bật proxy DNS là xong |

### Khi nào chọn Cloudflare

| Use case | Chọn Cloudflare nếu |
|---|---|
| Global audience high-traffic | Cần CDN cực gần user + DDoS free |
| Static site / SPA | Pages free + custom domain + SSL + CDN built-in |
| Cost-sensitive egress | R2 zero egress vs S3 $0.09/GB |
| Edge compute latency-critical | Workers cold start ~0ms (V8 isolate) vs Lambda 100-500ms |
| Zero Trust / VPN replacement | Access + Tunnel rẻ + dễ hơn AWS Verified Access |
| API gateway / rate limit | Workers + Rate Limiting + WAF tích hợp sẵn |
| Multi-cloud strategy | Cloudflare làm "front door" trước AWS/GCP origin |

### Khi KHÔNG chọn Cloudflare làm primary cloud

| Use case | Vì sao tránh |
|---|---|
| Heavy compute (ML training, video transcode) | Workers giới hạn 30s CPU, không có GPU |
| Long-running stateful workload | Workers stateless; cần Durable Objects/D1, vẫn giới hạn |
| Managed Postgres/MySQL phức tạp | Cloudflare không có managed SQL truyền thống (D1 = SQLite) |
| Niche enterprise service (SAP, Oracle, AD) | Cloudflare không có |
| Compliance yêu cầu region cụ thể (data residency cứng) | Workers chạy khắp POP, cần config Data Localization Suite (paid) |

→ Pattern phổ biến 2026: **Cloudflare làm edge layer + AWS/GCP làm origin** cho workload heavy.

---

## 2️⃣ Ba trụ cột Cloudflare — services tier 1

Cloudflare 2026 chia thành **3 mảng sản phẩm chính**:

### Trụ 1 — Network (foundation, miễn phí rộng)

| Service | Mô tả | Free Tier |
|---|---|---|
| **DNS** | Authoritative DNS + 1.1.1.1 resolver | Unlimited records, free |
| **CDN** | Reverse proxy + cache static asset | Unlimited bandwidth, free |
| **SSL/TLS** | Universal SSL cert tự động | Free, auto-renew |
| **Load Balancing** | L4/L7 global LB | Paid (từ $5/tháng) |
| **Argo Smart Routing** | Route qua backbone tối ưu | Paid (~$5/tháng) |
| **Spectrum** | Reverse proxy TCP/UDP (non-HTTP) | Paid |

→ Bài 01 đi sâu DNS + CDN + SSL.

### Trụ 2 — Security

| Service | Mô tả | Free Tier |
|---|---|---|
| **DDoS Protection** | L3/L4/L7 protection | **Unmetered free** |
| **WAF** | Web Application Firewall + managed rules | Free 1 custom rule; Pro/$25 = managed rules |
| **Rate Limiting** | Throttle theo IP/header | Free 10k req/tháng; Pro |
| **Bot Management** | Phân biệt human/bot/automated | Pro+ |
| **Zero Trust** (Access + Gateway + Tunnel) | VPN replacement, SSO, network filter | Free up to 50 users |
| **Turnstile** | CAPTCHA alternative không phiền user | Free unlimited |
| **mTLS** | Client certificate auth | Free 50 certs |

→ Bài 04 đi sâu WAF + Zero Trust + Bot.

### Trụ 3 — Developer Platform (Workers + storage)

| Service | Mô tả | Free Tier |
|---|---|---|
| **Workers** | Edge compute (V8 isolate, JS/TS/WASM) | 100k req/ngày, 10ms CPU/req |
| **Workers KV** | Eventual consistent key-value | 100k read/ngày, 1k write/ngày, 1 GB |
| **Durable Objects** | Strongly consistent stateful object | Paid ($5/tháng bundle) |
| **R2** | S3-compatible object storage | 10 GB storage, 1M Class A, 10M Class B op/tháng — **zero egress fee** |
| **D1** | SQLite edge-replicated | 500 MB/DB (5 GB tổng account), 5M row read/ngày |
| **Queues** | Message queue | Paid (Workers Paid plan $5) |
| **Hyperdrive** | Connection pool tới Postgres origin | Free with Workers Paid |
| **Pages** | Static site + dynamic functions | 500 builds/tháng, unlimited bandwidth |
| **Vectorize** | Vector DB cho AI/RAG | Beta — free tier rộng |
| **AI Gateway / Workers AI** | LLM proxy + serverless model | Free đa số model nhỏ |

→ Bài 02 sâu Workers + Pages. Bài 03 sâu R2 + D1 + Queues.

### Bonus — Email + Streams + Calls

| Service | Mô tả |
|---|---|
| **Email Routing** | Forward `you@yourdomain.com` → Gmail, free |
| **Email Workers** | Process inbound email bằng Worker |
| **Stream** | Video hosting + adaptive bitrate (paid per minute) |
| **Cloudflare Calls** | WebRTC infrastructure (beta) |

---

## 3️⃣ Hierarchy — Account → Zone → Resource

Cloudflare hierarchy **đơn giản hơn AWS/GCP** rất nhiều:

```text
Account (gắn email + billing)
├── Zone "acmeshop.vn"        ← (1 zone = 1 domain)
│   ├── DNS records (A, CNAME, MX, ...)
│   ├── Page Rules / Rules engine
│   ├── SSL certificates
│   ├── WAF rules
│   └── Cache settings
├── Zone "acme-staging.dev"
└── Workers (account-scoped, không gắn zone)
    ├── worker "acmeshop-api"
    ├── worker "acmeshop-image-resize"
    └── R2 bucket "acmeshop-uploads"
```

### Các khái niệm

| Khái niệm | Mô tả | Tương đương AWS/GCP |
|---|---|---|
| **Account** | Top-level — gắn email, billing, plan | AWS Account / GCP Org |
| **Zone** | 1 domain được Cloudflare manage DNS | (không tương đương trực tiếp; gần Route 53 Hosted Zone) |
| **Workers / R2 / D1** | Account-scoped, không thuộc zone | Lambda/S3/RDS nhưng global |
| **API Token** | Credential phạm vi giới hạn | IAM Role |
| **Members** | User trong account với role | IAM Users |

### Vì sao "Zone-centric" cho DNS/CDN/WAF

Tại sao Cloudflare bắt domain phải là "Zone"? Vì để Cloudflare làm CDN/proxy, bạn phải **trỏ nameservers của domain về Cloudflare**. Lúc đó Cloudflare "sở hữu" DNS của domain → bật `proxied = true` → mọi request đến domain đi qua POP Cloudflare trước → cache + WAF + DDoS protect → forward về origin nếu cần.

```text
User → DNS query "acmeshop.vn" → Cloudflare DNS trả về IP của POP gần
User → HTTP request tới POP → Cloudflare cache/WAF/Worker xử lý
       → (nếu cần) forward tới origin AWS S3 / VPS bạn
```

→ Nameservers Cloudflare = "cửa khẩu hải quan" của domain. Bạn không có Zone = không có CDN/WAF, chỉ dùng Workers/R2 stand-alone.

### Multiple zones cùng account

| Tình huống | Setup |
|---|---|
| 1 cá nhân + 3 domain riêng | 1 Account + 3 Zone |
| Công ty + nhiều brand | 1 Account + N Zone |
| Agency quản lý cho khách | Có **Tenant API** (Enterprise) hoặc tạo nhiều account |

---

## 4️⃣ Tạo Cloudflare account + secure baseline

### Bước 1 — Tạo account

1. Vào [dash.cloudflare.com/sign-up](https://dash.cloudflare.com/sign-up).
2. Email + password mạnh. Không cần credit card cho Free plan.
3. Verify email.

### Bước 2 — Bật 2FA

**Bắt buộc trước khi add domain**:
1. Profile → Authentication → Two-Factor Authentication → Enable.
2. Dùng **Authenticator app** (1Password, Authy, Google Authenticator) — không SMS.
3. **Lưu 10 backup codes** offline (password manager).

### Bước 3 — Add domain (Zone) đầu tiên

1. Dashboard → Add a Site → nhập `yourdomain.com`.
2. Chọn **Free plan** ($0/tháng).
3. Cloudflare scan DNS records hiện tại → review + add thiếu.
4. Cloudflare cung cấp **2 nameservers** dạng `xxx.ns.cloudflare.com`.
5. Vào registrar (Namecheap/GoDaddy/Porkbun) đổi nameservers.
6. Đợi 5 phút - 24 giờ propagate. Cloudflare email khi active.

### Bước 4 — Tạo API token (KHÔNG dùng Global API Key)

**Global API Key** = quyền full account, leak là toang. **API Token** = scoped, an toàn hơn.

1. Profile → API Tokens → Create Token.
2. Template: "Edit Cloudflare Workers" (hoặc custom).
3. Permissions chỉ vừa đủ (Principle of Least Privilege):
   - Account: Workers Scripts:Edit, Workers KV Storage:Edit
   - Zone: Cache Purge:Purge (nếu cần)
4. Account Resources: chọn account cụ thể, không "All accounts".
5. IP Address Filtering (optional): chỉ IP công ty.
6. TTL: set 6 tháng - 1 năm.
7. Copy token → lưu password manager. **Token chỉ hiện 1 lần.**

### Bước 5 — Setup billing alert (Pro+)

Free plan không có spending — không cần alert. Nếu nâng Pro/Business: Billing → Subscription → Notifications.

### Bước 6 — Audit Logs

Free plan có **Audit Log 30 ngày** cho mọi action quan trọng. Pro+ giữ lâu hơn:

```text
Account Home → Manage Account → Audit Log
```

Có thể filter theo user, action, date. Export CSV.

---

## 5️⃣ wrangler CLI — Cài đặt + auth + first command

🪞 **Ẩn dụ**: *`wrangler` là "chiếc xe tải" của Cloudflare — chở code Worker, asset Pages, dữ liệu R2/KV/D1 từ máy bạn lên edge global. Một CLI duy nhất cho cả Developer Platform.*

### Cài đặt

```bash
# Khuyến nghị: npm global
npm install -g wrangler

# Hoặc dùng npx (không cần install)
npx wrangler --version

# Verify
wrangler --version
# Kết quả: ⛅️ wrangler 3.x.x
```

> Yêu cầu Node.js 18+ (2026 khuyến nghị Node 20 LTS).

### Auth — Interactive (dev local)

```bash
# Mở browser → login Cloudflare → cấp quyền
wrangler login

# Verify
wrangler whoami
# Kết quả:
# 👋 You are logged in with an OAuth Token, associated with the email "thien.le@acmeshop.vn".
# ┌────────────────────────────┬────────────────────────────────────┐
# │ Account Name               │ Account ID                         │
# ├────────────────────────────┼────────────────────────────────────┤
# │ Acme Shop                  │ a1b2c3d4e5f6...                    │
# └────────────────────────────┴────────────────────────────────────┘
```

### Auth — API Token (CI/CD)

```bash
# Set env variable
export CLOUDFLARE_API_TOKEN="your-token-here"
export CLOUDFLARE_ACCOUNT_ID="a1b2c3d4e5f6..."

# wrangler tự động dùng
wrangler whoami
```

Hoặc tạo file `.env` (không commit):

```bash
CLOUDFLARE_API_TOKEN=xxx
CLOUDFLARE_ACCOUNT_ID=xxx
```

→ Trong GitHub Actions: dùng `secrets.CLOUDFLARE_API_TOKEN`.

### Common commands

```bash
# List Workers trong account
wrangler deployments list

# Tail logs realtime của Worker
wrangler tail my-worker-name

# Init project mới
wrangler init my-first-worker

# Deploy
wrangler deploy

# Dev local (Workers chạy local qua Miniflare)
wrangler dev

# R2 commands
wrangler r2 bucket list
wrangler r2 object put my-bucket/file.txt --file=./file.txt

# KV commands
wrangler kv:namespace create MY_KV
wrangler kv:key put --binding=MY_KV "key1" "value1"

# D1 commands
wrangler d1 create my-db
wrangler d1 execute my-db --command="SELECT 1"
```

---

## 6️⃣ Free Tier 2026 — Cloudflare rộng đến mức nào

So sánh side-by-side với AWS/GCP:

| Resource | Cloudflare Free | AWS Free 12-month | GCP Always Free |
|---|---|---|---|
| **CDN bandwidth** | **Unlimited** | 1 TB CloudFront | (không có) |
| **DDoS protection** | **Unmetered L3-L7** | Shield Standard (basic) | Cloud Armor basic |
| **Edge compute** | 100k req/ngày Workers | 1M Lambda req/tháng | 2M Functions/tháng |
| **Object storage** | 10 GB R2 + **$0 egress** | 5 GB S3 + 100 GB egress | 5 GB GCS + 1 GB egress/tháng |
| **DB** | D1 500 MB/DB (5 GB tổng) + 5M reads/ngày | 750h RDS db.t3.micro | 1 GB Firestore |
| **DNS** | Unlimited records | Route 53: 50 records | Cloud DNS: 25 zones |
| **SSL** | Free unlimited Universal SSL | ACM free | Let's Encrypt manual |
| **WAF custom rules** | 5 rules free | AWS WAF $1/rule + $0.60/M | Cloud Armor $5/policy |
| **Pages (static + functions)** | Unlimited bandwidth, 500 builds/tháng | Amplify: 1000 build-min, 5 GB | Firebase Hosting: 10 GB |

→ Với startup / personal project, **Cloudflare Free đủ chạy production** không trả $0. Khác AWS/GCP free 12 tháng rồi hết.

---

## 7️⃣ Account-level vs Zone-level permission

Khi tạo API token hoặc invite member:

| Permission scope | Áp dụng cho |
|---|---|
| **Account-level** | Workers, R2, D1, Pages, Account settings, Billing |
| **Zone-level** | DNS, SSL, WAF, Cache, Page Rules, Rate Limiting |

Ví dụ token deploy Workers:

```text
Account: Acme Shop
  ├── Workers Scripts: Edit
  ├── Workers KV: Edit
  └── R2 Storage: Edit
Zone: (không cần — Workers không gắn zone)
```

Token cho frontend dev update DNS:

```text
Account: (không cần)
Zone: acmeshop.vn
  └── DNS: Edit
```

→ Tách quyền theo team. Token leak chỉ mất phạm vi đó.

---

## 🛠️ Hands-on — Deploy first Worker "Hello edge" trong 5 phút

### Mục tiêu

Bạn deploy 1 Worker đơn giản trả về JSON, accessible từ URL `https://acmeshop-hello.<your-subdomain>.workers.dev`. Worker chạy ở 320+ POPs ngay khi deploy.

### Bước 1 — Init project

```bash
mkdir acmeshop-hello && cd acmeshop-hello
npm create cloudflare@latest -- acmeshop-hello \
    --type=hello-world \
    --lang=ts \
    --git=true \
    --deploy=false
```

Lệnh này tạo:

```text
acmeshop-hello/
├── src/
│   └── index.ts          # Worker code
├── test/
├── wrangler.toml         # Config
├── package.json
└── tsconfig.json
```

### Bước 2 — Xem code Worker

```typescript
// src/index.ts
export default {
    async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
        const url = new URL(request.url);
        const colo = request.cf?.colo ?? "unknown";

        return Response.json({
            message: "Hello from edge!",
            path: url.pathname,
            colo,
            country: request.cf?.country,
            timestamp: new Date().toISOString(),
        });
    },
} satisfies ExportedHandler<Env>;
```

→ `request.cf.colo` = mã POP xử lý request (e.g., `SIN` = Singapore, `HAN` = Hà Nội, `LAX` = Los Angeles).

### Bước 3 — Dev local

```bash
wrangler dev
# ⛅️ wrangler 3.x.x
# Ready on http://localhost:8787
```

Mở browser → `http://localhost:8787` → thấy JSON.

### Bước 4 — Deploy lên edge

```bash
wrangler deploy
# Total Upload: 1.32 KiB / gzip: 0.55 KiB
# Uploaded acmeshop-hello (0.96 sec)
# Published acmeshop-hello (1.07 sec)
#   https://acmeshop-hello.<your-subdomain>.workers.dev
# Current Deployment ID: a1b2c3d4-...
```

### Bước 5 — Test global latency

```bash
# Từ máy bạn
curl https://acmeshop-hello.<your-subdomain>.workers.dev
# {
#   "message": "Hello from edge!",
#   "path": "/",
#   "colo": "SIN",
#   "country": "VN",
#   "timestamp": "2026-05-24T03:14:00.000Z"
# }

# Test từ region khác (VPN hoặc curl từ remote server)
curl -H "CF-Connecting-IP: 8.8.8.8" https://acmeshop-hello.<your-subdomain>.workers.dev
# colo có thể khác (e.g., "IAD")
```

### Bước 6 — Tail logs realtime

```bash
wrangler tail acmeshop-hello
# Listening for logs... open the worker URL to see them
```

Mở URL nhiều lần → thấy log streaming.

### Bước 7 — Cleanup (optional)

```bash
# Xóa Worker
wrangler delete acmeshop-hello

# Hoặc giữ — Free tier không tốn gì
```

→ **Kết quả**: 1 Worker live ở 320+ POPs, latency ~5-30ms từ user gần POP, hoàn toàn free.

---

## 💡 Cạm bẫy thường gặp & Best practice

### ❌ Cạm bẫy: Dùng Global API Key cho mọi script

**Triệu chứng**: Script CI/CD dùng `CLOUDFLARE_API_KEY` (Global) → 1 ngày bị compromise → toàn bộ zone+DNS+Workers bị wipe.

**Nguyên nhân**: Global API Key = quyền cao nhất, không scope. Một file `.env` rò rỉ = mất account.

**Cách tránh**:
- **Luôn dùng API Token** với permission scoped.
- 1 token / 1 use case (deploy / DNS / R2).
- Set TTL token + rotate định kỳ.
- `gitleaks` hook trước khi commit.

### ❌ Cạm bẫy: Quên đổi nameservers → Zone "Pending"

**Triệu chứng**: Add zone xong, chờ mãi không active. CDN/WAF không hoạt động.

**Nguyên nhân**: Chưa đổi nameservers ở registrar (Namecheap/GoDaddy). Cloudflare chỉ active khi DNS query thật sự đi qua nameserver Cloudflare.

**Cách tránh**:
- Sau add zone → vào registrar đổi NS ngay.
- Kiểm tra: `dig NS yourdomain.com +short` phải trả `xxx.ns.cloudflare.com`.
- Đợi 5 phút - 24h (TTL DNS).

### ❌ Cạm bẫy: Bật proxy (cam) cho subdomain không hỗ trợ HTTP

**Triệu chứng**: Bật proxy (icon cam) cho subdomain `mail.acmeshop.vn` → email server không nhận được kết nối SMTP.

**Nguyên nhân**: Proxy Cloudflare chỉ tunnel HTTP/HTTPS (port 80, 443, ...). Mail/SSH/FTP cần **DNS-only** (icon xám).

**Cách tránh**:
- DNS record cho mail/SSH/database → **DNS-only** (xám).
- Chỉ web (HTTP/HTTPS) → **Proxied** (cam).
- Bài 01 chi tiết.

### ❌ Cạm bẫy: Nhầm Workers free tier 100k/ngày là 100k/tháng

**Triệu chứng**: Worker chạy production, ngày 2 đã hết quota → return error 1015 (rate limited).

**Nguyên nhân**: Free tier = **100k requests/ngày** (không phải /tháng). Reset mỗi 0h UTC.

**Cách tránh**:
- Monitor request rate ở Dashboard → Workers → Analytics.
- Khi gần ngưỡng → upgrade Workers Paid ($5/tháng, 10M req included).

### ❌ Cạm bẫy: Commit `wrangler.toml` chứa account_id + zone_id public

**Triệu chứng**: Repo public trên GitHub có `wrangler.toml` lộ `account_id`. Không phải secret nhưng giúp attacker target.

**Nguyên nhân**: account_id/zone_id không phải secret nhưng là PII của infrastructure.

**Cách tránh**:
- Repo private → OK commit.
- Repo public → để placeholder, set qua env hoặc secrets.

### ❌ Cạm bẫy: Region bias khi test latency

**Triệu chứng**: Test từ máy ở Việt Nam → 8ms tới Worker. Tự tin "global fast". Khách Brazil complain 200ms.

**Nguyên nhân**: Bạn ở gần POP Singapore (HAN/SIN). User ở Brazil đi POP GRU (São Paulo) — POP có nhưng connection từ user → POP có thể chậm nếu ISP local kém.

**Cách tránh**:
- Test bằng **Catchpoint / BrowserStack / WebPageTest** từ nhiều region.
- Dùng `request.cf.colo` log để biết user đi POP nào.
- Monitor real-user latency qua Cloudflare Analytics → Web Analytics.

### ❌ Cạm bẫy: Nhầm "Zone" với "Project"

**Triệu chứng**: Bạn muốn tách 3 môi trường (prod/staging/dev) trên cùng 1 domain — không biết tạo Zone hay tạo Worker khác name.

**Nguyên nhân**: Zone = domain. Workers/R2/D1 là account-scoped, không thuộc zone.

**Cách tránh**:
- 3 môi trường = 3 subdomain (prod: `acmeshop.vn`, staging: `staging.acmeshop.vn`, dev: `dev.acmeshop.vn`) trên cùng 1 zone.
- Hoặc 3 worker name: `acmeshop-api-prod`, `acmeshop-api-staging`, `acmeshop-api-dev`.
- Hoặc dùng wrangler **environments** (`[env.staging]`) trong `wrangler.toml`.

### ❌ Cạm bẫy: Không bật "Always Use HTTPS"

**Triệu chứng**: User gõ `http://acmeshop.vn` → Cloudflare forward HTTP về origin → form login leak password qua HTTP.

**Nguyên nhân**: Mặc định Cloudflare cho phép cả HTTP và HTTPS. Phải bật "Always Use HTTPS" để redirect 301.

**Cách tránh**:
- SSL/TLS → Edge Certificates → **Always Use HTTPS** = ON.
- SSL/TLS → **HSTS** (cẩn thận — bật rồi khó tắt).

---

## 🧠 Tự kiểm tra (Self-check)

**Q1.** Cloudflare khác AWS/GCP ở 3 điểm chính nào?

<details>
<summary>💡 Đáp án</summary>

1. **Edge-first vs region-first**: Cloudflare deploy 1 lần là toàn cầu 320+ POP. AWS/GCP phải chọn region.
2. **Pricing model**: Cloudflare zero egress (R2), unlimited bandwidth CDN. AWS/GCP tính per-GB egress đắt.
3. **Built-in security**: DDoS unmetered free + WAF + SSL tự động. AWS/GCP phải mua riêng (Shield Advanced, WAF, ACM).
</details>

**Q2.** Khi nào dùng "Proxied" (cam) vs "DNS-only" (xám) cho 1 DNS record?

<details>
<summary>💡 Đáp án</summary>

- **Proxied (cam)**: HTTP/HTTPS traffic — cần CDN, WAF, DDoS, cache.
- **DNS-only (xám)**: Non-HTTP (mail, SSH, FTP, custom port) hoặc record validation (TXT/MX) không cần proxy.
</details>

**Q3.** API Token vs Global API Key — khác gì? Khi nào dùng cái nào?

<details>
<summary>💡 Đáp án</summary>

- **Global API Key**: 1 token full quyền account. Cũ, không nên dùng cho automation.
- **API Token**: Scoped permission (chỉ Workers, chỉ Zone X, ...), có TTL, có IP filter.
- **Best practice 2026**: Luôn dùng API Token. Mỗi use case 1 token riêng.
</details>

**Q4.** Workers free tier giới hạn gì?

<details>
<summary>💡 Đáp án</summary>

- 100k requests/ngày (reset 0h UTC).
- 10ms CPU time / request.
- Workers KV: 100k reads/ngày, 1k writes/ngày.
- Vượt → error 1015 hoặc upgrade Workers Paid $5/tháng = 10M req included.
</details>

**Q5.** Vì sao R2 có "zero egress fee" mà S3 thì không?

<details>
<summary>💡 Đáp án</summary>

Cloudflare là 1 trong những thành viên sáng lập **Bandwidth Alliance** + sở hữu backbone network riêng. Họ không "phải trả tiền peering" như AWS. Đồng thời Cloudflare định vị R2 là chiến lược để cạnh tranh S3 — chấp nhận lỗ egress để hút khách.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

| Mục đích | Lệnh |
|---|---|
| Cài wrangler | `npm install -g wrangler` |
| Login | `wrangler login` |
| Whoami | `wrangler whoami` |
| Init Worker mới | `npm create cloudflare@latest -- my-worker` |
| Dev local | `wrangler dev` |
| Deploy | `wrangler deploy` |
| Tail logs | `wrangler tail <name>` |
| List Workers | `wrangler deployments list` |
| Delete Worker | `wrangler delete <name>` |
| List R2 buckets | `wrangler r2 bucket list` |
| Create KV namespace | `wrangler kv:namespace create <NAME>` |
| List zones (REST API) | `curl -H "Authorization: Bearer $TOKEN" https://api.cloudflare.com/client/v4/zones` |
| Check DNS NS | `dig NS yourdomain.com +short` |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Tiếng Việt | Giải thích |
|---|---|---|
| **POP** | Điểm hiện diện | Point of Presence — 1 data center edge Cloudflare (320+ cái) |
| **Zone** | Vùng (domain) | 1 domain được Cloudflare manage DNS |
| **Account** | Tài khoản | Top-level container, gắn email + billing |
| **Worker** | Hàm chạy ở edge | Function code chạy ở edge (V8 isolate) |
| **wrangler** | CLI Cloudflare | CLI chính để deploy Workers + Pages + R2 + D1 |
| **R2** | Object storage | Object storage S3-compatible, zero egress |
| **D1** | CSDL SQLite edge | SQLite database edge-replicated |
| **KV** | Key-value store | Workers KV — eventual consistent key-value store |
| **Durable Objects** | Object có trạng thái | Stateful object với strong consistency |
| **Pages** | Hosting static + Functions | Static site hosting + Functions (Workers tích hợp) |
| **Universal SSL** | Chứng chỉ SSL miễn phí | Cert miễn phí auto-renew của Cloudflare |
| **Proxied (cam)** | Đi qua proxy | DNS record đi qua proxy Cloudflare (HTTP/HTTPS) |
| **DNS-only (xám)** | Chỉ phân giải DNS | DNS record trả IP origin trực tiếp, không qua proxy |
| **Free Tier** | Gói miễn phí | Plan miễn phí — rộng hơn AWS/GCP rất nhiều |
| **API Token** | Credential scoped | Credential phạm vi giới hạn (recommended) |
| **Global API Key** | Khoá API toàn quyền | Credential full quyền (legacy, tránh) |
| **colo** | Mã POP | Mã POP xử lý request (SIN, HAN, LAX, ...) |
| **Bandwidth Alliance** | Liên minh băng thông | Liên minh giảm egress fee giữa cloud providers |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [Cloud Fundamentals — Nền tảng điện toán đám mây](../../../cloud-fundamentals/) — kiến thức nền tiên quyết
- ➡️ **Bài tiếp theo:** [Cloudflare CDN + DNS + SSL — Foundation của edge](01_cdn-dns-and-ssl.md) — DNS, proxied vs DNS-only, SSL modes
- ↑ **Về cụm:** [Cloudflare](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ **So sánh paradigm:** [AWS](../../../aws/) — vendor region-first lớn nhất
- ☁️ **So sánh paradigm:** [GCP](../../../gcp/) — vendor region-first
- 🌐 **Edge serverless:** [Serverless](../../../serverless/) — Workers thuộc nhóm này
- 🧭 **Tấm bản đồ sự nghiệp:** [Cloud Engineer Career Roadmap](../../../../00_roadmaps/career/cloud-engineer_career-roadmap.md)

### 🌐 Tài nguyên tham khảo khác

- [Cloudflare docs](https://developers.cloudflare.com/) — tài liệu gốc đầy đủ nhất.
- [wrangler CLI reference](https://developers.cloudflare.com/workers/wrangler/) — tra cứu lệnh wrangler.
- [Cloudflare Free Plan](https://www.cloudflare.com/plans/free/) — chi tiết gói miễn phí.
- [Network Map (320+ POPs)](https://www.cloudflare.com/network/) — bản đồ mạng edge toàn cầu.
- [Workers Examples gallery](https://developers.cloudflare.com/workers/examples/) — kho ví dụ Worker.
- [Cloudflare Radar](https://radar.cloudflare.com/) — xu hướng internet toàn cầu realtime.
- [The Cloudflare Blog](https://blog.cloudflare.com/) — bài kỹ thuật chuyên sâu.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 00 cluster Cloudflare basic. Overview Cloudflare edge-first paradigm + 3 trụ cột (Network/Security/Developer Platform) + Account→Zone hierarchy + wrangler CLI setup + Free Tier 2026 vs AWS/GCP + hands-on first Worker live tại 320+ POPs + 8 pitfalls. Pattern theo AWS/GCP lesson 00.
- **v1.1.0 (01/06/2026)** — Sửa lỗi QA: gắn ngôn ngữ cho các code fence bare (cây thư mục/flow/scope token/path dùng `text`, file `.env` dùng `bash`); chuẩn hoá phần "Liên kết & Tài nguyên" theo gold standard (marker ⬅️/➡️/↑, link-text = tiêu đề thực, 3 sub-heading canonical: Định hướng lộ trình học / Các chủ đề có thể bạn quan tâm / Tài nguyên tham khảo khác).
