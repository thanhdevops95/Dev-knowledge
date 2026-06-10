# 🎓 DNS Records — A, CNAME, MX, TXT, NS và bạn bè

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [DNS là gì](00_what-is-dns.md)

> 🎯 *Sau bài này bạn config được zone file cho domain mình mua: trỏ root domain về IP, dùng CNAME cho subdomain, thêm MX cho email, TXT cho SPF/DKIM/verification, NS cho subdomain phân quyền.*

## 🎯 Sau bài này bạn sẽ

- [ ] Hiểu **7 loại record phổ biến**: A, AAAA, CNAME, MX, TXT, NS, SOA
- [ ] Phân biệt **A vs CNAME** (lỗi #1 của beginner)
- [ ] Config được MX để **nhận email** trên domain riêng
- [ ] Đọc được TXT record SPF/DKIM/DMARC + verification (Google/GitHub)
- [ ] Hiểu **wildcard `*` record** + use case
- [ ] Biết khi nào dùng **ALIAS/ANAME** (Cloudflare/Route53 custom record)
- [ ] Đọc được 1 zone file thật

---

## Tình huống — bạn mua domain xong, panel toàn ký hiệu lạ

Bạn mua domain `acmeshop.vn` ở **Cloudflare** (₫280k/năm). Vào tab DNS settings — Bạn thấy:

```
Type     Name      Content              TTL    Proxy
─────────────────────────────────────────────────────
A        @         203.0.113.10         Auto   Proxied
A        www       203.0.113.10         Auto   Proxied
CNAME    blog      acmeshop.medium.com  Auto   Off
MX       @         mail.gmail.com       3600   Off
TXT      @         "v=spf1 include:_spf.google.com ~all"
TXT      _dmarc    "v=DMARC1; p=reject; rua=mailto:..."
```

Bạn ngơ:
- `A` và `CNAME` khác nhau ra sao? Sao `www` dùng `A`, `blog` dùng `CNAME`?
- **`@`** là gì? Sao 4 record có `@`?
- `MX` để làm gì? Liên quan email?
- TXT bắt đầu bằng `"v=spf1"` đọc như nào?
- `Proxied` là gì (cái mây cam của Cloudflare)?

→ Đây là **DNS records** — từng dòng config trong zone file dạy resolver cách trả lời từng loại câu hỏi. Bài này dạy bạn **7 loại record cốt lõi** + **5 use case thực tế**.

---

## 1️⃣ DNS record là gì?

**DNS record** = 1 entry trong **zone file** của domain, dạng:

```
<name>   <TTL>   <class>   <type>   <data>
```

Ví dụ:
```
acmeshop.vn.   3600   IN   A   203.0.113.10
```

Đọc: *"`acmeshop.vn` (TTL 3600s, internet class) thuộc loại A (IPv4), value là `203.0.113.10`."*

| Trường | Ý nghĩa |
|---|---|
| `name` | Domain/subdomain — `@` = root, `www` = subdomain `www.acmeshop.vn` |
| `TTL` | Cache time tính bằng giây |
| `class` | Hầu như luôn là `IN` (Internet) |
| `type` | Loại record (A, CNAME, MX...) |
| `data` | Giá trị (IP, domain khác, text...) |

> 🧠 **Ẩn dụ — Zone file như mục lục thư viện:**
> - Mỗi sách (domain/subdomain) có **nhiều entry** ở nhiều mục.
> - Bạn tra "Nguyễn Văn A" có thể thấy: ở kệ A203 (record A), email tới `mail@` (record MX), tài khoản Google verify (TXT).
> - 1 domain có thể có **rất nhiều record** cho từng nhu cầu.

### `@` là gì?

`@` = **root domain** (apex domain). Khi tên là `@`, áp cho chính `acmeshop.vn` (không có subdomain).

| Tên trong panel | FQDN đầy đủ |
|---|---|
| `@` | `acmeshop.vn.` |
| `www` | `www.acmeshop.vn.` |
| `api` | `api.acmeshop.vn.` |
| `mail` | `mail.acmeshop.vn.` |
| `*` | bất kỳ `<x>.acmeshop.vn.` (wildcard) |

---

## 2️⃣ 7 loại record phổ biến

DNS có ~30 loại record, nhưng **7 cái dưới đây chiếm 95%** mọi zone file thực tế. Học chúng kèm use case là đủ để config DNS cho production. Bảng tổng hợp:

| Type | Tên đầy đủ | Trả về | Use case |
|---|---|---|---|
| **A** | Address | IPv4 | Trỏ domain về server |
| **AAAA** | (Quad-A) | IPv6 | IPv6 — bắt buộc cho dual-stack |
| **CNAME** | Canonical Name | Domain khác | Alias subdomain về domain ngoài |
| **MX** | Mail Exchange | Mail server domain | Nhận email |
| **TXT** | Text | Text tùy ý | SPF, DKIM, DMARC, verification |
| **NS** | Name Server | Authoritative NS | Phân quyền DNS cho subdomain |
| **SOA** | Start Of Authority | Metadata zone | Bắt buộc, 1 zone 1 SOA |

Các loại nâng cao (sẽ gặp sau): `SRV`, `PTR`, `CAA`, `DS`, `DNSKEY`, `TLSA`.

---

## 3️⃣ A & AAAA — Trỏ domain về IP

**A record** = mapping `domain → IPv4`.\
**AAAA record** = mapping `domain → IPv6`.

```
@      A      203.0.113.10            ; acmeshop.vn → IPv4
@      AAAA   2001:db8::42            ; acmeshop.vn → IPv6
www    A      203.0.113.10            ; www.acmeshop.vn → cùng IP
api    A      198.51.100.55           ; api.acmeshop.vn → server khác
```

### Khi nào dùng A vs AAAA?

→ **Cả 2** — modern server nên có **dual-stack** (IPv4 + IPv6). Trỏ cả `A` và `AAAA`, client tự chọn protocol nào hỗ trợ.

### Nhiều A record cho 1 domain = round-robin

Đặt **nhiều A record** cho cùng 1 tên là cách load balancing DNS đơn giản nhất — DNS resolver trả danh sách IP xoay vòng, client tự chọn 1 cái. Free, không cần LB hardware, nhưng có hạn chế:

```
@      A      203.0.113.10
@      A      203.0.113.11
@      A      203.0.113.12
```

→ Resolver trả **danh sách 3 IP theo thứ tự xoay vòng** → load balancing đơn giản (free, không cần LB hardware). Hạn chế: không health check (1 IP chết vẫn được serve cho user).

---

## 4️⃣ CNAME — Alias từ subdomain sang domain khác

**CNAME record** = "subdomain này **là alias** của domain khác — resolver tự hỏi tiếp".

```
www       CNAME   acmeshop.vn.            ; www → acmeshop.vn (A record)
shop      CNAME   acmeshop.myshopify.com. ; shop → Shopify
blog      CNAME   acmeshop.medium.com.    ; blog → Medium custom domain
docs      CNAME   acmeshop.github.io.     ; docs → GitHub Pages
```

→ Resolver query `blog.acmeshop.vn` → thấy CNAME → tự đi query `acmeshop.medium.com` → trả về IP cuối cùng.

### Quy tắc QUAN TRỌNG của CNAME

CNAME có **3 ràng buộc đặc biệt** từ RFC mà nếu không biết sẽ tạo nhiều lỗi DNS khó debug. Đây là kiến thức **phải nắm** trước khi config CNAME cho production:

| Rule | Lý do |
|---|---|
| ❌ **Không CNAME ở apex (`@`)** | Spec RFC cấm — apex phải có `SOA` + `NS`, CNAME loại trừ mọi record khác |
| ❌ **Không trộn CNAME với record khác cùng tên** | `blog CNAME ...` không được kèm `blog A ...` |
| ✅ **Trỏ về 1 domain duy nhất** | Không có "multi-CNAME" |

### Lỗi #1 của beginner — CNAME apex

Khi deploy lên Netlify/Vercel/GitHub Pages, beginner hay set CNAME cho root domain (`acmeshop.vn` thay vì `www.acmeshop.vn`) — sai theo RFC. Dưới đây là ví dụ lỗi điển hình + 3 cách fix:

```
@   CNAME   acmeshop.netlify.app.   ; ❌ SAI — apex không được CNAME
```

**Cách fix** (3 lựa chọn):

1. **Dùng A** — query IP của Netlify rồi paste vào A record. Hạn chế: IP đổi → bạn phải update tay.
2. **Dùng ALIAS / ANAME / "CNAME flattening"** — record giả lập do DNS provider làm (Cloudflare, Route53). Cloudflare flatten tự động khi bạn set CNAME apex (proxy on).
3. **Redirect** — đặt apex A trỏ vào `203.0.113.10` (chạy nginx redirect 301 → `www.acmeshop.vn`).

---

## 5️⃣ MX — Nhận email trên domain riêng

**MX record** = chỉ server nào nhận email cho `@acmeshop.vn`. Có **priority** (số nhỏ = ưu tiên cao).

```
@   MX   10   aspmx.l.google.com.
@   MX   20   alt1.aspmx.l.google.com.
@   MX   30   alt2.aspmx.l.google.com.
```

→ Gửi mail tới `nguyenvana@acmeshop.vn`:
1. Mail server gửi (Gmail của user khác) query MX của `acmeshop.vn`.
2. Nhận về 3 MX. Thử priority `10` trước (Google primary).
3. Nếu down → fallback priority `20`, `30`.

### Phổ biến (2026)

4 provider email lớn nhất 2026 đều có MX record format khác nhau — copy đúng cấu hình từ docs của provider, sai 1 ký tự là email không nhận được:

| Provider | MX record |
|---|---|
| **Google Workspace** | `1 smtp.google.com` (single MX, mới 2023) |
| **Microsoft 365** | `0 acmeshop-vn.mail.protection.outlook.com` |
| **Zoho Mail** | `10 mx.zoho.com`, `20 mx2.zoho.com` |
| **Self-host (Postfix)** | `10 mail.acmeshop.vn` (kèm A record `mail`) |

### Cạm bẫy MX

- ❌ **MX trỏ vào IP** → sai. MX phải trỏ vào **domain**, không phải IP.
- ❌ **MX trỏ vào CNAME** → spec không cho. Phải trỏ domain có A record thật.
- ❌ **Quên SPF + DKIM** → email bị Gmail/Outlook mark spam ngay (xem §6).

---

## 6️⃣ TXT — Text tùy ý (SPF/DKIM/DMARC/verification)

**TXT record** = chuỗi text bất kỳ. Original dùng cho ghi chú. Giờ là **chỗ chứa metadata bảo mật + verification**.

### Use case 1 — SPF (Sender Policy Framework)

Chỉ rõ **server nào được phép gửi email** dưới danh `@acmeshop.vn` — chống spoofing.

```
@   TXT   "v=spf1 include:_spf.google.com include:mailgun.org ~all"
```

Đọc:
- `v=spf1` — version 1
- `include:_spf.google.com` — Google Workspace OK gửi
- `include:mailgun.org` — Mailgun (transactional) OK gửi
- `~all` — server khác = soft fail (mark spam)

### Use case 2 — DKIM (DomainKeys Identified Mail)

Public key cho receiver verify email **thực sự gửi từ bạn**, không bị tamper.

```
default._domainkey   TXT   "v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3..."
```

→ Provider (Google/Mailgun) sẽ cho bạn copy chuỗi này.

### Use case 3 — DMARC (Domain-based Message Authentication)

Chính sách khi SPF/DKIM fail.

```
_dmarc   TXT   "v=DMARC1; p=reject; rua=mailto:postmaster@acmeshop.vn"
```

- `p=reject` — fail = bouce thẳng (cứng)
- `p=quarantine` — fail = vào spam (mềm)
- `p=none` — chỉ report, không bounce (test mode)

### Use case 4 — Verification (Google/GitHub/Microsoft)

```
@   TXT   "google-site-verification=abc123xyz..."
```

→ Bạn add record này để **chứng minh domain là của bạn** khi setup Google Workspace / Search Console / GitHub Pages.

### Cạm bẫy TXT

- ❌ **Quote sai** — dấu `"..."` phải bao toàn bộ chuỗi.
- ❌ **2 SPF record cho cùng name** → spec cấm. Phải gộp vào **1 record** với nhiều `include:`.
- ❌ **TXT vượt 255 ký tự** → DNS giới hạn 1 chuỗi 255 ký tự. Public key DKIM dài hơn → phải chia nhiều chuỗi: `"abc..." "def..."`.

---

## 7️⃣ NS — Phân quyền DNS cho subdomain

**NS record** = chỉ "authoritative server cho `<name>` là server này".

Mỗi domain có ít nhất 2 NS ở apex:

```
@   NS   ns1.cloudflare.com.
@   NS   ns2.cloudflare.com.
```

→ Khi đăng ký domain ở Namecheap, bạn nhập 2 NS này → Namecheap (registrar) báo cho `.vn` registry → query về `acmeshop.vn` từ giờ Cloudflare trả lời.

### Sub-delegation — phân quyền subdomain cho server khác

```
dev   NS   ns1.dev-host.com.
dev   NS   ns2.dev-host.com.
```

→ Mọi query `*.dev.acmeshop.vn` được forward về `ns1.dev-host.com`. Hữu ích khi:
- Team dev/staging có DNS riêng
- Đại lý/khách hàng quản lý subdomain họ tự config

---

## 8️⃣ SOA — Metadata zone (auto, ít khi đụng)

**SOA** = **Start Of Authority** — metadata zone, mỗi zone 1 SOA duy nhất, do DNS provider tự tạo.

```
@   SOA   ns1.cloudflare.com. dns.cloudflare.com. (
            2024051401 ; serial (YYYYMMDDxx)
            10800      ; refresh
            3600       ; retry
            604800     ; expire
            86400 )    ; minimum TTL (negative cache)
```

| Trường | Ý nghĩa |
|---|---|
| Master NS | Authoritative server primary |
| Admin email | `dns.cloudflare.com` = `dns@cloudflare.com` (`@` thay = `.`) |
| Serial | Version zone — tăng khi config đổi (secondary NS dùng để biết cần sync) |
| Refresh/Retry/Expire | Cho secondary NS sync |
| Minimum TTL | Negative cache TTL (response NXDOMAIN cache bao lâu) |

→ Beginner **không cần** chỉnh SOA. Cloudflare/Route53 auto-manage.

---

## 9️⃣ Wildcard record `*`

```
*   A   203.0.113.10
```

→ **Mọi subdomain chưa có record riêng** sẽ trả `203.0.113.10`. Hữu ích cho:

- **SaaS multi-tenant** — `customer1.app.com`, `customer2.app.com`... cùng IP, app phân biệt qua `Host` header.
- **Catch-all dev** — `*.dev.acmeshop.vn` về staging.

### Cạm bẫy wildcard

- ❌ Subdomain đã có record cụ thể → wildcard không apply (specific thắng wildcard).
- ❌ Wildcard không có cấp dưới — `*.acmeshop.vn` không match `a.b.acmeshop.vn`.
- ⚠️ SSL cert wildcard (`*.acmeshop.vn`) phải request riêng (Let's Encrypt qua DNS-01 challenge).

---

## 🔟 ALIAS / ANAME / CNAME flattening — "CNAME ở apex"

Vì spec cấm CNAME ở apex, nhưng nhu cầu trỏ `acmeshop.vn` về Netlify/Vercel/Heroku (chỉ cho domain, không cho IP) **rất thực tế**.

→ DNS provider lớn (Cloudflare, Route53, DigitalOcean) làm **ALIAS / ANAME / CNAME flattening**:

1. User config `@ CNAME acmeshop.netlify.app.` (panel cho phép)
2. DNS provider **tự resolve** `acmeshop.netlify.app` → IP
3. Trả IP đó trong A response
4. Refresh định kỳ (TTL Netlify thay đổi → provider update)

→ Tên gọi khác nhau:
- **Cloudflare**: CNAME flattening (auto khi proxy on)
- **Route53**: ALIAS record (chỉ cho AWS resource)
- **DigitalOcean / NS1 / DNSimple**: ALIAS hoặc ANAME

→ **Không phải standard DNS record** — chỉ là feature của provider.

---

## 1️⃣1️⃣ Zone file đầy đủ cho `acmeshop.vn`

```
; Apex + www
@      A      203.0.113.10
@      AAAA   2001:db8::10
www    A      203.0.113.10
www    AAAA   2001:db8::10

; Email — Google Workspace
@      MX     1   smtp.google.com.
@      TXT    "v=spf1 include:_spf.google.com ~all"
google._domainkey   TXT   "v=DKIM1; k=rsa; p=MIGfMA0GCS..."
_dmarc TXT    "v=DMARC1; p=quarantine; rua=mailto:postmaster@acmeshop.vn"

; Subdomain — SaaS / static
api    A      198.51.100.55
shop   CNAME  acmeshop.myshopify.com.
blog   CNAME  acmeshop.medium.com.
docs   CNAME  acmeshop.github.io.

; Wildcard cho dev
*.dev  A      192.0.2.20

; Verification (đã verify, giữ lại để Google không bỏ trust)
@      TXT    "google-site-verification=abc123xyz..."

; NS (auto từ Cloudflare)
@      NS     ns1.cloudflare.com.
@      NS     ns2.cloudflare.com.
```

→ Bạn giờ có: web (`@`, `www`), email (`MX`), Shopify (`shop`), Medium blog (`blog`), GitHub Pages docs (`docs`), staging wildcard (`*.dev`).

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **CNAME apex** → Không được. Dùng A record hoặc ALIAS/flattening của provider.
2. **2 SPF records** → Spec cấm. Phải gộp `include:` vào 1 record.
3. **MX trỏ vào IP** → Sai. MX phải là domain có A record.
4. **Quên dấu `.` cuối FQDN trong zone file** → `acmeshop.medium.com` (không dấu) ≠ `acmeshop.medium.com.` (FQDN). Cloudflare panel tự thêm, nhưng raw zone file cần đúng.
5. **Đổi NS khi đang chạy production** → NS đổi = đi lại từ root → mất 24-48h. Đảm bảo **2 NS cũ + 2 NS mới đều có cùng record** trước khi switch, không thì site die nửa người.

---

## 🧠 Tự kiểm tra (Self-check)

1. Bạn mua domain `mysite.io`, muốn:
   a. `mysite.io` trỏ về `198.51.100.10`
   b. `www.mysite.io` trỏ về cùng nơi
   c. `docs.mysite.io` trỏ tới `mysite.github.io`
   d. Email `@mysite.io` về Google Workspace
   → Viết zone file.

2. Sao không CNAME được apex? Cách work-around?
3. TXT SPF `v=spf1 -all` nghĩa là gì? Khác `~all`?
4. Domain có 3 A record cùng `@`, kết quả khi user query?
5. ALIAS record là gì? Khác CNAME ra sao?

<details>
<summary>Gợi ý đáp án</summary>

1. ```
   @      A      198.51.100.10
   www    A      198.51.100.10           (hoặc CNAME @)
   docs   CNAME  mysite.github.io.
   @      MX  1  smtp.google.com.
   @      TXT    "v=spf1 include:_spf.google.com ~all"
   ```

2. CNAME loại trừ mọi record khác cùng name, nhưng apex bắt buộc có SOA + NS → conflict. Work-around: dùng A record (paste IP), hoặc dùng ALIAS / CNAME flattening của provider lớn.

3. `-all` = hard fail (server khác = chắc chắn fail, reject). `~all` = soft fail (mark suspicious nhưng vẫn deliver, an toàn hơn khi mới setup).

4. Resolver trả **cả 3 IP**, client (browser) chọn ngẫu nhiên → DNS round-robin load balancing đơn giản. Hạn chế: không health check.

5. ALIAS = feature riêng của DNS provider (Cloudflare, Route53), giả lập "CNAME ở apex" bằng cách provider tự resolve IP và serve A response. Standard DNS không có ALIAS — chỉ là quality-of-life feature.
</details>

---

## ⚡ Cheatsheet

| Mục đích | Record loại | Ví dụ |
|---|---|---|
| Trỏ domain về server | A | `@ A 203.0.113.10` |
| Hỗ trợ IPv6 | AAAA | `@ AAAA 2001:db8::10` |
| Alias subdomain → domain ngoài | CNAME | `blog CNAME mysite.medium.com.` |
| Nhận email | MX | `@ MX 10 smtp.google.com.` |
| Chống spoof email | TXT (SPF) | `@ TXT "v=spf1 include:_spf.google.com ~all"` |
| Verify ownership | TXT | `@ TXT "google-site-verification=..."` |
| Phân quyền subdomain | NS | `dev NS ns1.other.com.` |
| Bắt mọi subdomain | wildcard A | `* A 203.0.113.10` |

### Đối chiếu record vs use case

| Bạn muốn | Dùng record |
|---|---|
| Trỏ `mydomain.com` về VPS | A (apex) |
| Trỏ `www.mydomain.com` → cùng VPS | A hoặc CNAME → @ |
| Trỏ `app.mydomain.com` → Heroku | CNAME |
| Trỏ `mydomain.com` → Netlify (apex) | ALIAS/CNAME flattening |
| Nhận mail `you@mydomain.com` | MX + TXT (SPF/DKIM/DMARC) |
| Verify Google Workspace | TXT |
| Subdomain riêng cho team A | NS |

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Apex / root domain** | Phần ngắn nhất bạn đăng ký (`acmeshop.vn`, không có subdomain) |
| **FQDN** | Fully Qualified Domain Name — full domain có dấu `.` cuối |
| **A / AAAA** | Address record — trỏ domain → IPv4/IPv6 |
| **CNAME** | Canonical Name — alias subdomain → domain khác |
| **MX** | Mail eXchange — mail server nhận email cho domain |
| **TXT** | Text record — chứa SPF/DKIM/DMARC/verification |
| **NS** | Name Server — authoritative server cho zone (hoặc sub-zone) |
| **SOA** | Start Of Authority — metadata zone, 1 zone 1 SOA |
| **SPF** | Sender Policy Framework — chỉ server nào được gửi email |
| **DKIM** | DomainKeys Identified Mail — chữ ký số chống tamper |
| **DMARC** | Domain-based Message Authentication — chính sách khi SPF/DKIM fail |
| **ALIAS / ANAME** | "CNAME apex" giả lập do provider làm |
| **Wildcard** | `*` match mọi subdomain chưa có record riêng |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [DNS là gì? — Danh bạ điện thoại của Internet](00_what-is-dns.md)
- ➡️ **Bài tiếp theo:** [DNS Resolution — Hành trình từ `google.com` đến IP](02_dns-resolution.md)
- ↑ **Về cụm:** [dns README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [HTTP headers](../../../http-https/lessons/01_basic/03_http-headers.md) — `Host` header phối hợp wildcard DNS cho SaaS multi-tenant

### 🌐 Tài nguyên tham khảo khác
- 📖 [Cloudflare DNS records explained](https://www.cloudflare.com/learning/dns/dns-records/)
- 📖 [SPF/DKIM/DMARC complete guide — dmarcian](https://dmarcian.com/dmarc-vs-spf-vs-dkim/)
- 📖 [Google Workspace MX setup](https://support.google.com/a/answer/140034)
- 📖 [Mailgun: How to set up DKIM](https://documentation.mailgun.com/en/latest/quickstart-sending.html)

---

> 🎯 *Sau bài này bạn config được zone file cho domain mình mua: trỏ web, nhận email, alias subdomain, verify Google. Bài kế tiếp đi sâu vào **flow query thực sự đi qua những server nào** — root → TLD → authoritative — kèm cache + TTL chi tiết.*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `dns/` lesson 2/5. Cover: zone file structure + 7 record types (A/AAAA/CNAME/MX/TXT/NS/SOA) + CNAME 3 rules + apex fix + MX với SPF/DKIM/DMARC anti-spam + TXT verification + NS delegation + SOA metadata + record nâng cao (SRV, PTR, CAA, DS, DNSKEY).
- **v1.1.0 (25/05/2026)** — Bổ sung lead-in trước các bảng/ví dụ ở §2 (7 record types), §3 (A multi-record round-robin), §4 (CNAME 3 rules + lỗi CNAME apex), §5 (MX provider table). Thêm Changelog section.
