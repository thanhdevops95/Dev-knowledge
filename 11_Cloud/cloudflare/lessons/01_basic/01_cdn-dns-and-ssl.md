# 🌐 Cloudflare CDN + DNS + SSL — Foundation của edge

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 24/05/2026\
> **Cập nhật:** 24/05/2026\
> **Level:** Basic (bài 01/5)\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~20 phút\
> **Prerequisites:** Xong [00_what-is-cloudflare-overview](00_what-is-cloudflare-overview.md), hiểu DNS A/CNAME/MX, SSL handshake cơ bản

> 🎯 *Bài này là trụ cột "Network" của Cloudflare — thứ làm Cloudflare nổi tiếng từ 2009. Bạn học: authoritative DNS, 1.1.1.1, sự khác biệt proxied vs DNS-only, 4 SSL mode (Off/Flexible/Full/Full Strict), Universal SSL, Page Rules (legacy) + Rules engine 2024+, Cache Rules syntax mới, Cache analytics. Sau bài: tự setup CDN+SSL cho Acme Shop, hiểu khi nào dùng mode nào, debug cache miss.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **authoritative DNS Cloudflare** vs **1.1.1.1 resolver** — 2 thứ khác nhau
- [ ] Phân biệt **Proxied (cam)** vs **DNS-only (xám)** — khi nào dùng cái nào
- [ ] Hiểu **4 SSL mode**: Off / Flexible / Full / Full Strict — chọn đúng tránh insecure
- [ ] Setup **Universal SSL** + custom hostname + Origin CA cert
- [ ] Viết **Cache Rules** 2024+ syntax (thay Page Rules legacy)
- [ ] Đọc **Cache Analytics** + debug "cache miss" 
- [ ] Setup CDN cho Acme Shop từ A → Z

---

## Tình huống — Acme Shop chậm + AWS CloudFront bill cao

Acme Shop dùng AWS S3 + CloudFront để serve static asset. Tháng 4 bill $1800 chỉ riêng CloudFront. Khách Việt Nam, Indonesia complain ảnh sản phẩm load chậm vào giờ cao điểm. Bạn được giao migrate sang Cloudflare CDN.

Bạn login Cloudflare → bật proxy cho domain → cache hit rate chỉ 12%? Origin AWS S3 vẫn bị hit gần như mọi request. SSL setup default → user bị cảnh báo "Mixed Content". Page Rules cũ ở dashboard cũ hơn... Rồi bạn đọc thấy "Rules engine" mới — phải migrate.

Bài này gỡ rối từng phần.

---

## 1️⃣ Authoritative DNS vs Resolver — Cloudflare có cả 2

🪞 **Ẩn dụ**: *Authoritative DNS là **giấy khai sinh** — Cloudflare lưu "acmeshop.vn = IP 1.2.3.4". Resolver (1.1.1.1) là **người tra cứu** — máy bạn hỏi "domain X ở đâu?" rồi đi hỏi authoritative server. Cloudflare làm cả 2 vai trò nhưng 2 service khác nhau.*

### Authoritative DNS — Cloudflare làm cho Zone của bạn

Khi bạn add zone `acmeshop.vn` vào Cloudflare và đổi nameservers, Cloudflare trở thành **authoritative DNS server** cho domain đó. Mọi DNS query trên thế giới hỏi "acmeshop.vn ở đâu?" cuối cùng sẽ tới nameserver Cloudflare và nhận câu trả lời.

```
User → Resolver (8.8.8.8 / 1.1.1.1) → Root DNS → .vn TLD → 
       → Cloudflare NS (anna.ns.cloudflare.com) → trả IP
```

### Resolver 1.1.1.1 — public DNS resolver

`1.1.1.1` là **public DNS resolver** Cloudflare mở miễn phí — fast, private (no log), DNSSEC. Không liên quan trực tiếp đến authoritative service. User nào setup `1.1.1.1` trên máy → tra DNS qua Cloudflare.

| Service | Vai trò |
|---|---|
| **Authoritative DNS** | Lưu records của domain bạn quản lý |
| **1.1.1.1 Resolver** | Tra cứu records của mọi domain trên Internet |

→ Bài này chỉ tập trung **Authoritative DNS** của zone bạn.

### Records cơ bản

| Type | Mục đích | Ví dụ |
|---|---|---|
| **A** | Trỏ tên → IPv4 | `acmeshop.vn → 203.0.113.42` |
| **AAAA** | Trỏ tên → IPv6 | `acmeshop.vn → 2001:db8::1` |
| **CNAME** | Alias tên → tên khác | `www → acmeshop.vn` |
| **MX** | Mail server | `acmeshop.vn → 10 mx.zoho.com` |
| **TXT** | Text metadata (SPF, DKIM, verify) | `_dmarc → v=DMARC1; p=reject;` |
| **NS** | Nameserver (Cloudflare tự manage) | `anna.ns.cloudflare.com` |
| **SRV** | Service discovery (Matrix, SIP, ...) | (ít dùng) |
| **CAA** | Cert authority authorization | `0 issue "letsencrypt.org"` |

### Tạo DNS record qua Dashboard

`DNS → Records → Add record`:

| Field | Giá trị ví dụ |
|---|---|
| Type | A |
| Name | `@` (= root domain) hoặc `www` |
| IPv4 address | `203.0.113.42` |
| Proxy status | **Proxied (cam)** hoặc **DNS only (xám)** ← phần lớn confusion ở đây |
| TTL | Auto (Cloudflare manage) |

### Tạo qua API/wrangler

```bash
# Qua REST API
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data '{
        "type": "A",
        "name": "www",
        "content": "203.0.113.42",
        "ttl": 1,
        "proxied": true
    }'
```

---

## 2️⃣ Proxied (cam) vs DNS-only (xám) — quyết định lớn nhất

🪞 **Ẩn dụ**: *Proxied (cam) là **"đi qua trạm kiểm soát Cloudflare"** — mọi request user → trạm gần nhất kiểm tra, lọc, cache, rồi mới (đôi khi) forward về origin. DNS-only (xám) là **"đi thẳng đến origin"** — Cloudflare chỉ làm bưu điện trả địa chỉ, không can thiệp traffic.*

### Khác nhau

| Tiêu chí | Proxied (cam 🟠) | DNS-only (xám ⚫) |
|---|---|---|
| **DNS query trả về** | IP của POP Cloudflare | IP origin thật |
| **Traffic đi qua Cloudflare** | ✅ Có | ❌ Không |
| **CDN cache** | ✅ Cache static | ❌ Không cache |
| **WAF / DDoS** | ✅ Áp dụng | ❌ Không bảo vệ |
| **SSL Cloudflare** | ✅ Universal SSL | ❌ Phải tự SSL origin |
| **IP origin bị lộ** | ❌ Ẩn (chỉ Cloudflare biết) | ✅ Lộ |
| **Workers Routes apply** | ✅ Có | ❌ Không |
| **Protocol hỗ trợ** | HTTP/HTTPS chỉ | Mọi protocol (SSH, SMTP, FTP, ...) |
| **Port hỗ trợ** | 80, 443, 2052-2087 (HTTP/HTTPS standard) | Mọi port |

### Khi nào dùng Proxied (cam)

- ✅ Web HTTP/HTTPS (`acmeshop.vn`, `www.acmeshop.vn`, `api.acmeshop.vn`)
- ✅ Subdomain Workers (`workers.dev`)
- ✅ Cần CDN + WAF + DDoS

### Khi nào dùng DNS-only (xám)

- ✅ Mail server (`mail.acmeshop.vn` → SMTP/IMAP)
- ✅ SSH server (`ssh.acmeshop.vn` → port 22)
- ✅ DNS verification record (TXT cho Google Search Console)
- ✅ MX records (luôn xám)
- ✅ Subdomain dùng port non-standard (5432 cho Postgres, ...)

### Lỗi phổ biến — bật proxy cho mail

```
mail.acmeshop.vn → A 203.0.113.42 → Proxied (cam) ← SAI
```

User gửi email → SMTP port 25 → Cloudflare proxy chỉ tunnel HTTP → connection refused. Email bị bounce hàng loạt.

**Fix**: Đổi `mail.acmeshop.vn` thành DNS-only (xám). MX record luôn xám.

### Cách kiểm tra

```bash
# Proxied → trả IP của Cloudflare (104.x.x.x hoặc 172.67.x.x)
dig acmeshop.vn +short
# 104.21.42.13
# 172.67.198.222

# DNS-only → trả IP origin thật
dig mail.acmeshop.vn +short
# 203.0.113.42
```

---

## 3️⃣ SSL/TLS modes — 4 lựa chọn, chọn sai = insecure

🪞 **Ẩn dụ**: *SSL mode quyết định **"đoạn nào trong hành trình request được mã hoá"**. Tưởng tượng request là 1 lá thư đi qua 2 đoạn đường: User → Cloudflare và Cloudflare → Origin. Mỗi mode bảo vệ 1 đoạn khác nhau.*

### Diagram 4 modes

```
User                  Cloudflare                Origin
  |                      |                        |
  |    [Mode]            |     [Mode]             |
  |======================|========================|
  | Off:        HTTP     |        HTTP            |  ← Insecure cả 2 đoạn
  | Flexible:   HTTPS    |        HTTP            |  ← Insecure đoạn 2
  | Full:       HTTPS    |        HTTPS (self-sig OK)
  | Full Strict:HTTPS    |        HTTPS (valid CA)
```

### Chi tiết

| Mode | User ↔ Cloudflare | Cloudflare ↔ Origin | Use case | Mức an toàn |
|---|---|---|---|---|
| **Off** | HTTP | HTTP | Không bao giờ | 🔴 Không bao giờ dùng |
| **Flexible** | HTTPS ✅ | HTTP ❌ | Origin không SSL được (legacy) | 🔴 Insecure — MITM ở đoạn 2 |
| **Full** | HTTPS ✅ | HTTPS (cert any) | Origin self-signed cert | 🟡 OK nếu network trust |
| **Full (Strict)** | HTTPS ✅ | HTTPS (cert valid) | Production | 🟢 **Khuyến nghị** |

### Vì sao Flexible nguy hiểm

User thấy https:// → tưởng an toàn. Nhưng đoạn Cloudflare → Origin vẫn HTTP. Nếu attacker ở giữa Cloudflare và origin (vd ISP của bạn) → đọc/sửa được traffic. Đặc biệt nguy với form login.

→ **Quy tắc 2026**: Mọi production dùng **Full (Strict)**. Origin phải có cert hợp lệ (Let's Encrypt hoặc Cloudflare Origin CA).

### Universal SSL — cert tự động cho mọi zone

Khi add zone, Cloudflare tự cấp **Universal SSL cert** miễn phí cho:
- Apex domain (`acmeshop.vn`)
- First-level subdomain (`*.acmeshop.vn`)

Cert có wildcard, auto-renew, dùng SNI. Hiển thị: SSL/TLS → Edge Certificates.

### Origin CA Certificate — cho phía origin

Nếu origin của bạn (server VPS, AWS EC2) chưa có SSL, dùng **Origin CA** (Cloudflare cấp cert chỉ valid khi traffic đi qua Cloudflare):

```bash
# Trong Dashboard: SSL/TLS → Origin Server → Create Certificate
# Cloudflare tạo cert + private key valid 15 năm
# Install vào nginx/apache origin của bạn
```

Origin CA cert **không** valid với public (vd direct curl) — chỉ valid khi Cloudflare làm proxy. Cách rẻ + dễ nhất để SSL origin.

### Always Use HTTPS

`SSL/TLS → Edge Certificates → Always Use HTTPS = ON`

→ User gõ `http://acmeshop.vn` → Cloudflare redirect 301 → `https://acmeshop.vn`.

### Automatic HTTPS Rewrites

`SSL/TLS → Edge Certificates → Automatic HTTPS Rewrites = ON`

→ Sửa `http://` trong HTML body thành `https://` tự động (tránh "Mixed Content" warning).

### HSTS (HTTP Strict Transport Security)

`SSL/TLS → Edge Certificates → HSTS = ON`

⚠️ **Cẩn thận**: Khi bật, browser **cache rule trong tháng/năm** — không thể rollback sang HTTP nếu lỡ. Chỉ bật khi chắc SSL ổn định lâu dài.

---

## 4️⃣ Page Rules (legacy) vs Rules engine 2024+

Cloudflare có 2 thế hệ cấu hình:

### Page Rules (legacy — sắp deprecate)

```
Page Rules → URL pattern → 1-3 settings
```

Limit: 3 rules free, 20 Pro, 50 Business. Cú pháp wildcard `*`. **Đang phase out**.

### Rules engine (2024+) — khuyến nghị

Cloudflare tách Page Rules thành **4 engines** chuyên biệt:

| Engine | Mục đích | Ví dụ |
|---|---|---|
| **Cache Rules** | Override cache behavior | Cache HTML 1 hour, bypass cache cho `/admin/*` |
| **Configuration Rules** | Bật/tắt feature theo URL | Tắt Email Obfuscation cho `/blog/*` |
| **Redirect Rules** | URL redirect | `/old-path → /new-path` |
| **Origin Rules** | Override origin (Host header, port, ...) | `/api/* → api.acmeshop.vn:8443` |

→ Mỗi engine có 10 rules free, 25 Pro. Cú pháp **expression-based** (giống WAF custom rules):

```
(http.request.uri.path matches "^/api/")
```

### Ví dụ Cache Rule

`Rules → Cache Rules → Create Rule`:

```
Name: Cache HTML pages 5 minutes
If: (http.request.uri.path eq "/" or http.request.uri.path matches "^/products/")
Then:
  - Eligible for cache: Yes
  - Edge TTL: 5 minutes
  - Browser TTL: 1 minute
  - Cache Key: Custom (include query string `?lang=`)
```

### Ví dụ Redirect Rule

```
Name: Redirect old blog
If: (http.request.uri.path matches "^/blog/old/")
Then:
  - Status: 301
  - URL: concat("https://acmeshop.vn/blog/", regex_replace(http.request.uri.path, "^/blog/old/", ""))
  - Preserve query string: Yes
```

### Ví dụ Configuration Rule

```
Name: Disable cache for /admin
If: (http.request.uri.path matches "^/admin/")
Then:
  - Cache Level: Bypass
  - Security Level: High
```

→ Bài này dừng ở Cache Rules; WAF/Rate Limit rules để bài 04.

---

## 5️⃣ Cache behavior — vì sao cache miss

🪞 **Ẩn dụ**: *Cache Cloudflare là **kho hàng tại trạm kiểm soát**. Hàng vào 1 lần, trạm giữ lại; lần sau khách hỏi cùng món → đưa từ kho luôn, không cần ra hậu trường (origin). Cache miss = "không có trong kho, phải đi lấy".*

### Default cache behavior

Cloudflare **mặc định cache** một số extension static:

| Cache mặc định | Không cache mặc định |
|---|---|
| `.js`, `.css`, `.png`, `.jpg`, `.gif`, `.svg`, `.webp` | `.html` (vì có thể dynamic) |
| `.woff`, `.woff2`, `.ttf`, `.otf` | API response (`/api/*`) |
| `.pdf`, `.zip` | Bất kỳ response có `Cache-Control: private` |
| `.mp4`, `.webm` (Stream service) | Bất kỳ response có `Set-Cookie` |

### Cache key

Cloudflare cache theo **cache key** mặc định = `scheme + host + path` (không tính query string).

→ Vấn đề: `acmeshop.vn/product?id=1` và `acmeshop.vn/product?id=2` có **cùng cache key** → trả cùng response. SAI.

**Fix**: Trong Cache Rules → Cache Key → Include Query String `id`.

### Origin Cache-Control header

Origin trả header `Cache-Control: max-age=3600, public` → Cloudflare cache 3600 giây. Override được qua Cache Rules → Edge TTL.

| Header origin | Cloudflare làm gì |
|---|---|
| `Cache-Control: public, max-age=3600` | Cache 1 giờ |
| `Cache-Control: private` | Không cache |
| `Cache-Control: no-cache` | Cache nhưng revalidate mỗi request |
| `Cache-Control: no-store` | Không cache |
| `Set-Cookie: ...` | Không cache (mặc định) |
| Không có Cache-Control | Cache theo extension default |

### Purge cache

Khi deploy code mới, cần purge cache cũ:

```bash
# Purge specific URL
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    --data '{"files":["https://acmeshop.vn/style.css"]}'

# Purge everything (nguy hiểm — cache hit rate về 0 tạm thời)
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    --data '{"purge_everything":true}'

# Purge by tag (Enterprise only)
# Purge by prefix (Enterprise only)
```

Hoặc qua Dashboard: Caching → Configuration → Purge Cache.

### Cache Status header

Response từ Cloudflare luôn có `cf-cache-status`:

| Status | Ý nghĩa |
|---|---|
| `HIT` | Cache hit — trả từ POP |
| `MISS` | Cache miss — đi origin lấy |
| `EXPIRED` | Cache có nhưng hết TTL → revalidate |
| `BYPASS` | Cache rule bypass |
| `DYNAMIC` | Cloudflare quyết định không cache (do Set-Cookie, Cache-Control private, ...) |
| `REVALIDATED` | Origin trả 304 Not Modified → cache OK |

```bash
curl -I https://acmeshop.vn/logo.png
# HTTP/2 200
# cf-cache-status: HIT
# cache-control: public, max-age=14400
# age: 3284
```

---

## 6️⃣ Cache Analytics — debug cache miss

Dashboard → Analytics & Logs → Cache Analytics.

### Metrics quan trọng

| Metric | Ý nghĩa | Target |
|---|---|---|
| **Cache Hit Ratio** | % request cache hit | >80% là tốt, >95% xuất sắc |
| **Bandwidth Saved** | Bandwidth không phải đi origin | Càng cao càng tiết kiệm |
| **Top URLs Cached** | URL cache hit nhiều nhất | Static asset, ảnh, fonts |
| **Top URLs Not Cached** | URL miss/bypass | Check vì sao — nếu static thì sai config |

### Vì sao cache hit rate thấp

| Lý do | Cách kiểm tra | Fix |
|---|---|---|
| Set-Cookie header từ origin | `curl -I` | Loại Cookie không cần thiết khỏi static |
| Cache-Control: private | `curl -I` | Origin trả `public` cho static |
| URL chứa query string khác nhau | Cache Key | Cache Rule include/exclude query |
| `?_t=timestamp` tracking | URL pattern | Strip tracking param qua Transform Rules |
| TTL quá ngắn | Edge TTL setting | Tăng TTL qua Cache Rules |
| Origin trả 5xx | Logs | Fix origin để không hit cache poison |

---

## 7️⃣ Custom Hostnames + SaaS for Multi-tenant

Nếu Acme Shop bán SaaS — khách hàng dùng subdomain riêng (`shop1.acmeshop.com`, `shop2.acmeshop.com`) hoặc custom domain (`mystore.com`):

### SSL for SaaS (Cloudflare for SaaS)

- Free 100 custom hostnames.
- Mỗi customer trỏ CNAME → `acmeshop.com` của bạn.
- Cloudflare tự cấp SSL cert cho mỗi hostname.

```bash
# Add custom hostname qua API
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/custom_hostnames" \
    -H "Authorization: Bearer $CF_API_TOKEN" \
    --data '{
        "hostname": "mystore.com",
        "ssl": {"method": "http", "type": "dv"}
    }'
```

→ Use case: agency, white-label, SaaS multi-tenant. Bài này không deep — note để biết tồn tại.

---

## 🛠️ Hands-on — Setup CDN + SSL cho Acme Shop

### Mục tiêu

Bạn:
1. Add domain `acmeshop.vn` vào Cloudflare (giả lập, có thể test với domain thật của bạn).
2. Setup DNS records.
3. Configure SSL Full Strict + Always HTTPS.
4. Tạo Cache Rule cache HTML 5 phút.
5. Verify cache hit qua curl.

### Bước 1 — Add zone

Dashboard → Add a Site → `acmeshop.vn` → Free plan.

(Nếu chưa có domain → mua $1-10/năm trên Namecheap/Porkbun, hoặc dùng domain bạn có sẵn).

### Bước 2 — Setup records

```
Type   Name   Content              Proxy        TTL
A      @      203.0.113.42         Proxied 🟠   Auto
CNAME  www    acmeshop.vn          Proxied 🟠   Auto
A      api    203.0.113.42         Proxied 🟠   Auto
A      mail   203.0.113.42         DNS only ⚫  Auto
MX     @      10 mx.zoho.com       DNS only ⚫  Auto
TXT    @      v=spf1 ...           DNS only ⚫  Auto
```

### Bước 3 — Đổi nameservers ở registrar

Vào Namecheap/Porkbun → Domain settings → Nameservers → Custom:

```
anna.ns.cloudflare.com
otto.ns.cloudflare.com
```

(Tên cụ thể Cloudflare hiển thị riêng cho zone bạn.)

Wait ~10 phút → Cloudflare email "active".

### Bước 4 — SSL config

`SSL/TLS → Overview`:
- Encryption mode: **Full (Strict)** (đảm bảo origin có cert hợp lệ; nếu chưa, dùng Origin CA bước 4b).

`SSL/TLS → Edge Certificates`:
- Always Use HTTPS: **ON**
- Automatic HTTPS Rewrites: **ON**
- Minimum TLS Version: **TLS 1.2**
- HSTS: tạm OFF (bật khi production stable)

### Bước 4b — (Optional) Origin CA cert

Nếu origin chưa SSL:

```
SSL/TLS → Origin Server → Create Certificate
→ Validity: 15 năm, hostnames: *.acmeshop.vn, acmeshop.vn
→ Download cert + key
→ Cài vào nginx/apache origin
```

### Bước 5 — Cache Rule

`Rules → Cache Rules → Create Rule`:

```
Rule name: Cache HTML 5 min
When incoming requests match:
  (http.request.uri.path eq "/") or
  (http.request.uri.path matches "^/products/")
Then:
  Cache eligibility: Eligible for cache
  Edge TTL: Override origin: 5 minutes
  Browser TTL: Override origin: 1 minute
Save → Deploy
```

### Bước 6 — Test cache

```bash
# Request 1 — MISS
curl -sI https://acmeshop.vn/ | grep -i cf-cache-status
# cf-cache-status: MISS

# Request 2 — HIT
curl -sI https://acmeshop.vn/ | grep -i cf-cache-status
# cf-cache-status: HIT

# Test SSL Full Strict
curl -v https://acmeshop.vn/ 2>&1 | grep "SSL certificate"
# SSL certificate verify ok.
```

### Bước 7 — Cleanup test traffic

Cache Analytics sẽ thấy traffic. Bạn có thể purge:

```
Caching → Configuration → Purge Cache → Purge Everything
```

→ **Kết quả**: domain serve qua Cloudflare CDN, SSL Full Strict, HTML cache 5 phút, cache hit ratio trên 80% sau 1 ngày traffic.

---

## 💡 Pitfalls — Bẫy phổ biến

### ❌ Pitfall: SSL mode Flexible cho production

**Triệu chứng**: User thấy HTTPS lock icon → tưởng an toàn. Form login leak qua HTTP đoạn Cloudflare → Origin.

**Nguyên nhân**: Flexible mode origin vẫn HTTP. Attacker ở giữa đọc/sửa được.

**Cách tránh**: Luôn dùng **Full (Strict)**. Origin cài Origin CA cert nếu không có Let's Encrypt.

### ❌ Pitfall: Bật proxy cho mail subdomain

**Triệu chứng**: Email bounce, SMTP timeout sau khi bật Cloudflare.

**Nguyên nhân**: Proxy chỉ tunnel HTTP/HTTPS. SMTP (port 25/465/587) không qua được.

**Cách tránh**: `mail.*` và MX records → DNS-only (xám) always.

### ❌ Pitfall: Cache miss vì Set-Cookie

**Triệu chứng**: Cache Hit Ratio 5-15%. Mọi static file đều MISS.

**Nguyên nhân**: Origin gửi `Set-Cookie` header (vd session cookie) trên cả request static → Cloudflare bypass cache theo default.

**Cách tránh**:
- Origin: chỉ set cookie trên route cần (vd `/api/login`), không set trên static.
- Hoặc Cache Rule: Cache Key → Ignore cookies.

### ❌ Pitfall: Cache hit cũ sau khi deploy

**Triệu chứng**: Deploy code mới, user vẫn thấy CSS/JS cũ.

**Nguyên nhân**: Cloudflare cache CSS/JS với TTL dài (vài giờ). Không tự invalidate khi deploy.

**Cách tránh**:
- Versioned filename: `style.abc123.css` (Webpack/Vite tự sinh).
- Hoặc: API call purge sau deploy.
- Hoặc: Cache Rule → Cache Key → bypass với specific query.

### ❌ Pitfall: HSTS bật rồi muốn tắt

**Triệu chứng**: Bật HSTS thử nghiệm 1 lần → đổi sang HTTP → browser vẫn force HTTPS → không truy cập được.

**Nguyên nhân**: HSTS cache trong browser theo `max-age` (thường 6 tháng - 1 năm). Tắt HSTS không xoá cache đó.

**Cách tránh**:
- Chỉ bật HSTS khi chắc SSL ổn định lâu dài.
- Test trước với `max-age=300` (5 phút) → đổi `max-age=31536000` (1 năm) sau khi OK.

### ❌ Pitfall: TXT record verification quên DNS-only

**Triệu chứng**: Google Search Console verify TXT fail dù record đúng.

**Nguyên nhân**: Lỗi hiếm — TXT record không bị ảnh hưởng proxy, nhưng vẫn nên để DNS-only cho rõ.

**Cách tránh**: TXT/MX/SRV → mặc định DNS-only.

### ❌ Pitfall: Cache HTML trong khi page có user-specific content

**Triệu chứng**: User A login → user B vào cùng URL → thấy thông tin A.

**Nguyên nhân**: Cache Rule cache HTML cho tất cả users → user-specific data bị share.

**Cách tránh**:
- Chỉ cache HTML public (homepage, blog, product listing).
- Page user-specific: Bypass cache HOẶC tách thành "shell + AJAX" (shell cache, data AJAX no-cache).

### ❌ Pitfall: Wildcard cache rule quá rộng

**Triệu chứng**: `*` match cả `/admin/*` → admin panel bị cache → user khác thấy nhau.

**Nguyên nhân**: Pattern matching quá rộng.

**Cách tránh**: 
- Cache rule luôn specific path (`^/products/`, `^/blog/`).
- Configuration Rule: `^/admin/` → Cache Level: Bypass.

---

## 🧠 Self-check

**Q1.** Phân biệt authoritative DNS và resolver DNS. Cloudflare làm cái nào cho zone của bạn?

<details>
<summary>💡 Đáp án</summary>

- **Authoritative**: server "biết câu trả lời" cho 1 domain (vì lưu records). Cloudflare làm authoritative cho zone bạn add.
- **Resolver**: server "tra cứu" cho user (8.8.8.8, 1.1.1.1). Cloudflare có resolver công cộng tên 1.1.1.1 nhưng đó là service khác.
</details>

**Q2.** Khi nào subdomain phải DNS-only (xám)?

<details>
<summary>💡 Đáp án</summary>

- Mail server (SMTP/IMAP — port 25/465/587/143/993)
- SSH server (port 22)
- Database direct (Postgres 5432, MySQL 3306)
- MX records (luôn xám)
- DNS verification TXT records
- Bất kỳ protocol không phải HTTP/HTTPS
</details>

**Q3.** SSL mode Flexible nguy hiểm thế nào?

<details>
<summary>💡 Đáp án</summary>

User ↔ Cloudflare HTTPS (an toàn). Cloudflare ↔ Origin HTTP (insecure). Attacker giữa Cloudflare và origin (vd ISP) đọc/sửa được password, cookie, ... User không biết vì browser vẫn thấy https://.
</details>

**Q4.** `cf-cache-status: DYNAMIC` nghĩa là gì?

<details>
<summary>💡 Đáp án</summary>

Cloudflare quyết định không cache response này. Thường do origin gửi `Set-Cookie`, `Cache-Control: private`, hoặc extension không trong default cache list. Khác với BYPASS (do rule bạn set).
</details>

**Q5.** Khi deploy CSS mới, cache cũ vẫn serve. Cách fix nào tốt nhất?

<details>
<summary>💡 Đáp án</summary>

**Tốt nhất**: Versioned filename — `style.abc123.css`. Mỗi build hash mới → URL mới → cache key mới → tự nhiên invalidate. Không cần purge.

**Tạm**: Purge specific URL qua API sau deploy. Đừng `purge_everything` vì làm cache hit rate cả site về 0.
</details>

---

## ⚡ Cheatsheet

| Mục đích | Cách làm |
|---|---|
| Check DNS proxy status | `dig domain.com +short` (104.x = proxied) |
| Check cache hit | `curl -sI URL \| grep cf-cache-status` |
| Purge URL | `curl -X POST .../purge_cache --data '{"files":["URL"]}'` |
| Purge all | `--data '{"purge_everything":true}'` |
| SSL mode tốt | Full (Strict) |
| Free Universal SSL | Auto, apex + 1-level subdomain |
| Wildcard SSL | Cần Advanced Certificate Manager (paid) hoặc Advanced DCV |
| Force HTTPS | SSL/TLS → Edge Certificates → Always Use HTTPS |
| Bypass cache for path | Cache Rule với "Cache eligibility: Bypass" |
| Cache HTML | Cache Rule → Edge TTL override |

---

## 📚 Glossary

| EN | VN / Giải thích |
|---|---|
| **Authoritative DNS** | Server giữ records gốc của 1 domain |
| **Resolver / Recursive DNS** | Server tra cứu DNS giúp client |
| **Proxied** | Traffic đi qua Cloudflare (cam) |
| **DNS-only** | DNS trả về IP origin, không proxy (xám) |
| **Universal SSL** | Cert tự động miễn phí cho zone |
| **Origin CA** | Cert Cloudflare cấp cho origin server |
| **Full (Strict)** | SSL mode khuyến nghị — cả 2 chân đều HTTPS valid |
| **HSTS** | Header buộc browser luôn dùng HTTPS |
| **Page Rules** | Cấu hình URL pattern (legacy) |
| **Rules engine** | Hệ thống mới (Cache/Config/Redirect/Origin Rules) |
| **Cache Key** | Chuỗi định danh 1 cached object |
| **Edge TTL** | Thời gian cache ở POP |
| **Browser TTL** | Thời gian cache ở browser user |
| **Purge** | Xoá cache thủ công |
| **cf-cache-status** | Header cho biết trạng thái cache |
| **HIT / MISS / DYNAMIC / BYPASS** | Trạng thái cache cụ thể |
| **Custom Hostname** | Subdomain/domain khách map qua CNAME (Cloudflare for SaaS) |

---

## 🔗 Liên kết & Tài nguyên

### Trong cluster
- ↶ Trước: [00_what-is-cloudflare-overview](00_what-is-cloudflare-overview.md)
- → Tiếp: [02_workers-and-pages](02_workers-and-pages.md) — Workers + Pages edge compute
- ↑ Cluster: [Cloudflare README](../../README.md)

### Cross-reference
- ☁️ [AWS S3 + IAM](../../../aws/lessons/01_basic/02_s3-deep-and-iam.md) — so sánh CloudFront vs Cloudflare CDN
- ☁️ [GCP Cloud Storage + IAM](../../../gcp/lessons/01_basic/02_cloud-storage-and-iam.md)

### Tài nguyên ngoài (2026)
- 📖 [Cloudflare DNS docs](https://developers.cloudflare.com/dns/)
- 📖 [SSL/TLS modes docs](https://developers.cloudflare.com/ssl/origin-configuration/ssl-modes/)
- 📖 [Cache Rules docs](https://developers.cloudflare.com/cache/how-to/cache-rules/)
- 📖 [Page Rules → Rules engine migration](https://developers.cloudflare.com/rules/page-rules/migration/)
- 📖 [Origin CA Certificates](https://developers.cloudflare.com/ssl/origin-configuration/origin-ca/)
- 📖 [Cloudflare for SaaS](https://developers.cloudflare.com/cloudflare-for-platforms/cloudflare-for-saas/)
- 📖 [Cache Analytics](https://developers.cloudflare.com/analytics/account-and-zone-analytics/zone-analytics/)

---

## 📌 Changelog

- **v1.0.0 (24/05/2026)** — Bản đầu tiên. Bài 01 cluster Cloudflare basic. DNS authoritative + 1.1.1.1 + proxied vs DNS-only + 4 SSL modes + Universal SSL + Origin CA + Page Rules → Rules engine migration + Cache Rules 2024 syntax + cf-cache-status + cache analytics + hands-on Acme Shop setup full + 8 pitfalls. Pattern theo AWS/GCP lesson 01.
