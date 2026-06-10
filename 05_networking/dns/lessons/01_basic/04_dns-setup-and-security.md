# 🎓 DNS Setup & Security — Đăng ký domain, propagation, DNSSEC, DoH/DoT

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.2.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Yêu cầu trước:** [DNS Records](01_dns-records.md), [DNS Resolution](02_dns-resolution.md), [DNS Tools](03_dns-tools.md)

> 🎯 *Bài cuối cluster. Đi từ A-Z: đăng ký domain mới, đổi nameserver về Cloudflare, đợi propagation, bật DNSSEC, hiểu DoH/DoT, defend các attack DNS phổ biến.*

## 🎯 Sau bài này bạn sẽ

- [ ] Đăng ký được **1 domain** từ A-Z (chọn TLD + registrar + checkout)
- [ ] **Đổi nameserver** từ registrar sang DNS provider (Cloudflare)
- [ ] Hiểu **propagation 24-48h** và cách giảm
- [ ] Bật được **DNSSEC** + biết khi nào cần
- [ ] Phân biệt **DoH** vs **DoT** + khi nào dùng
- [ ] Defend 4 attack DNS: spoofing, hijacking, tunneling, amplification
- [ ] Biết **5 best practice** vận hành DNS production

---

## Tình huống — Bạn muốn mua domain đầu tiên

Bạn quyết định ra mắt shop online. Cần `acmeshop.vn`. Bạn Google "mua domain" — thấy:

- **Cloudflare Registrar** — `$10/năm cho .com`, "no markup"
- **Namecheap** — `$8.88/năm .com`, mua kèm SSL được giảm
- **GoDaddy** — `$0.99 năm đầu`, năm 2 = $20
- **Mắt Bão / iNet / TenTen** — `.vn` Việt Nam, ~₫280k-500k/năm
- **Z.com / Matbao** — domain `.vn` + hosting

Bạn ngơ:
- **Mua đâu rẻ + uy tín?**
- Sau khi mua, **làm gì tiếp theo**?
- Tại sao **đợi 24-48h** mới hoạt động?
- **DNSSEC** ai mới cần?
- Setup xong có cần **security gì thêm** không?

→ Bài này dạy bạn **đầy đủ flow từ mua domain → setup → bảo mật** cho domain production.

---

## 1️⃣ Đăng ký domain — Chọn TLD trước tiên

### Bước 1 — Chọn TLD

TLD ảnh hưởng đến **giá (1-150 USD/năm)**, **độ tin cậy** (legal cho `.vn`), và **brand perception** (`.io` tech, `.com` mainstream). 10 TLD phổ biến nhất với cheat sheet "khi nào chọn":

| TLD | Giá/năm (~) | Khi nào chọn |
|---|---|---|
| `.com` | $10-15 USD | Default — phổ thông, mọi nơi |
| `.io` | $40-60 USD | Tech startup (hot) |
| `.dev` | $15-20 USD | Personal portfolio dev |
| `.app` | $20-25 USD | Mobile app, force HTTPS |
| `.ai` | $80-150 USD | AI startup (hot, đắt) |
| `.vn` | ₫280k-500k | Bắt buộc target Việt Nam (legal) |
| `.com.vn` | ₫350k-700k | Company VN — "uy tín" hơn `.vn` đơn |
| `.org` | $10-15 USD | Tổ chức phi lợi nhuận |
| `.net` | $10-15 USD | Cũ — ít dùng cho startup mới |
| `.xyz` | $1-15 USD | Rẻ — phù hợp side project |

> 🧠 *Quy tắc nhanh: dự án dài hạn → `.com`. Startup tech → `.io`/`.dev`/`.ai`. Cho Việt Nam → `.vn`/`.com.vn`. Side project → `.xyz`/`.dev`.*

### Bước 2 — Chọn registrar

Registrar = công ty bán domain. Khác nhau nhiều về **giá renewal**, **UX** (dark pattern hay không), và **dịch vụ kèm** (DNS, SSL, privacy). 5 registrar phổ biến với trade-off rõ ràng:

| Registrar | Pros | Cons | Best for |
|---|---|---|---|
| **Cloudflare Registrar** | Giá gốc (no markup), tích hợp DNS sẵn, bảo mật mạnh, free WHOIS privacy | Không bán mọi TLD, không phone support | **Mọi domain non-VN — recommendation #1** |
| **Namecheap** | Phổ thông, giá tốt, support OK, free WHOIS privacy | Hay upsell | Mua kèm SSL/hosting |
| **GoDaddy** | Lớn nhất, UI quen | **Đắt năm 2**, upsell mạnh, dark pattern | Tránh nếu có lựa chọn khác |
| **PorkBun** | Giá rẻ, tech-friendly, có UI hiện đại | Brand chưa quen | Side project, dev |
| **Mắt Bão / iNet / TenTen** | Bán `.vn` (hosting VN bắt buộc local) | UI cũ, support email chậm | Domain `.vn` legal-required |

→ **Recommendation 2026**: Cloudflare Registrar cho `.com/.io/.dev/...`. Mắt Bão cho `.vn`.

### Bước 3 — Mua

1. Search domain → check available.
2. Add cart → checkout.
3. **Bỏ mọi upsell** (privacy đã miễn phí với Cloudflare/Namecheap; SSL miễn phí qua Let's Encrypt).
4. Verify email từ ICANN trong 15 ngày (nếu không sẽ bị suspend).

### Cạm bẫy mua domain

4 cái bẫy phổ biến khi mua domain — gặp 1 trong số đó là **đắt thêm vài chục USD/năm** hoặc kẹt không transfer được. Đọc trước để tránh:

- ❌ **Giá năm đầu rẻ, năm 2 đắt 5 lần** (GoDaddy hay dùng) → check renewal price.
- ❌ **WHOIS privacy bắt trả thêm** → Cloudflare/Namecheap free. GoDaddy free từ 2022.
- ❌ **Bị "transfer lock" sau khi mua 60 ngày** → quy định ICANN, không tránh được.
- ❌ **Mua `.vn` ở registrar nước ngoài** → không được, phải qua registrar VN.

---

## 2️⃣ Đổi nameserver về DNS provider

Domain mua xong nằm ở **registrar** (Cloudflare/Namecheap). DNS có thể stay ở registrar **HOẶC** chuyển sang DNS provider riêng.

> 💡 **Lý do tách**: DNS provider chuyên (Cloudflare) **nhanh hơn**, **bảo mật hơn**, có **DDoS protection**, có **analytics**, có **proxy** (cái mây cam). Mua domain ở Mắt Bão nhưng dùng DNS ở Cloudflare = best of both worlds.

### Bước 1 — Tạo zone ở Cloudflare

1. [dash.cloudflare.com](https://dash.cloudflare.com) → "Add Site" → nhập `acmeshop.vn`.
2. Chọn plan **Free** (Cloudflare Free đủ 99% nhu cầu).
3. Cloudflare scan zone hiện tại (nếu có) hoặc bắt đầu trống.
4. Cloudflare cho bạn **2 nameserver**, ví dụ:
   - `bob.ns.cloudflare.com`
   - `alice.ns.cloudflare.com`

### Bước 2 — Đổi NS ở registrar

Vào dashboard registrar (Mắt Bão / Namecheap) → tìm "Nameservers" → thay 2 NS mặc định bằng 2 NS Cloudflare.

| Registrar | Đường dẫn |
|---|---|
| Mắt Bão | Quản lý → DNS Management → Nameservers |
| Namecheap | Domain List → Manage → Nameservers → "Custom DNS" |
| Cloudflare | Domain Registration → Manage → Nameservers (nếu đã ở CF, skip bước này) |

### Bước 3 — Thêm record

Vào Cloudflare DNS panel → thêm A, CNAME, MX, TXT theo nhu cầu (xem [bài 01](01_dns-records.md)).

### Bước 4 — Đợi propagation

Cloudflare check NS đã đổi → email báo "site is active". Thường:

- **5 phút - 1 giờ**: 80% resolver cập nhật
- **24 giờ**: 99% cập nhật
- **48 giờ**: gần như 100%

→ Trong thời gian này, site vẫn vào được (nếu A record giống nhau ở 2 nơi). Chỉ "không vào được" khi NS cũ đã tắt mà NS mới chưa propagate.

### Best practice migration

Migrate DNS provider mà không downtime cần **chuẩn bị 7 ngày trước**. Workflow chuẩn — copy zone sang provider mới trước khi switch NS, đảm bảo cả 2 nơi đều trả đúng kết quả:

```
Day -7: Add record y hệt ở Cloudflare (cùng IP) trước khi switch NS
Day -1: Verify Cloudflare zone trả đúng kết quả (dig @bob.ns.cloudflare.com)
Day 0:  Switch NS ở registrar
Day 0+: Monitor propagation qua dnschecker.org
Day +2: Confirm 99%+ propagate → đổi config nếu cần
```

---

## 3️⃣ DNSSEC — Ký số chống fake DNS

### Vấn đề: DNS response có thể bị fake

DNS query qua UDP port 53 **cleartext**. Attacker giữa client và resolver có thể inject response giả → user vào site fake. Gọi là **DNS cache poisoning** / **spoofing**.

```
User → Resolver: acmeshop.vn?
                       ↑
                       [Attacker inject fake response]
Resolver → User: IP = 1.2.3.4 (phishing server)
```

### Giải pháp: DNSSEC

**DNSSEC** = **DNS Security Extensions** — ký số mọi response bằng public-key crypto.

```
.  (root)
 └── KSK signs ZSK   ← Root key (ICANN giữ)
     └── .com KSK signs ZSK
         └── acmeshop.vn KSK signs ZSK
             └── A record signed by ZSK
```

→ Mỗi level ký level dưới. Resolver verify từ root down → đảm bảo response không bị tamper.

### 4 loại record DNSSEC

DNSSEC thêm **4 record mới** để build chain of trust. Mỗi record có vai trò trong "chuỗi chữ ký số" từ root → TLD → zone của bạn. Hiểu 4 cái này là hiểu được DNSSEC hoạt động:

| Record | Vai trò |
|---|---|
| **DNSKEY** | Public key của zone (cả KSK và ZSK) |
| **RRSIG** | Chữ ký số trên mỗi record (A, MX, ...) |
| **DS** | Delegation Signer — hash KSK con, đặt ở zone cha (registrar) |
| **NSEC / NSEC3** | "Authenticated denial" — chứng minh "record này KHÔNG tồn tại" có chữ ký |

### Chain of trust thực tế

```
1. Resolver query "acmeshop.vn A"
2. Auth trả: A record + RRSIG (chữ ký A bằng ZSK)
3. Resolver lấy DNSKEY của acmeshop.vn → verify RRSIG
4. Để tin DNSKEY, resolver verify DS record của acmeshop.vn tại .com TLD
5. Để tin DS, resolver verify chữ ký .com TLD bằng DNSKEY của .com
6. Cuối chuỗi: verify root key — pre-installed cứng trong resolver (root trust anchor)
```

→ Bất kỳ điểm nào chuỗi đứt = resolver coi **bogus**, không trả về client.

### Thống kê adoption 2026

- ~30% domain world có DNSSEC bật.
- ~90% resolver public (Cloudflare, Google) validate DNSSEC.
- `.gov`, `.bank`, `.edu` thường yêu cầu DNSSEC. `.com/.vn` tùy chọn.

### Bật DNSSEC ở Cloudflare

1. Vào zone → DNS → **DNSSEC** → "Enable".
2. Cloudflare cho bạn **DS record** (Delegation Signer):
   ```
   DS  acmeshop.vn.  IN  DS  2371 13 2 ABC123DEF456...
   ```
3. Copy DS record vào **registrar** (Mắt Bão/Namecheap → DNSSEC settings).
4. Đợi 24h → kiểm tra `dig +dnssec acmeshop.vn` thấy `ad` flag = OK.

### Khi nào cần DNSSEC?

| Cần | Không cần |
|---|---|
| Domain bank, fintech, gov | Personal blog |
| Email hosting (cùng với DANE) | Side project |
| Crypto exchange | Marketing landing |
| Healthcare (HIPAA) | Wiki private |

→ DNSSEC làm DNS chậm hơn ~5-10% (do verify chữ ký) và config phức tạp. Hầu hết domain không cần. Bank/crypto **phải**.

### Cạm bẫy DNSSEC

- ❌ **Bật DNSSEC ở Cloudflare nhưng quên thêm DS ở registrar** → site die vì resolver verify fail.
- ❌ **Đổi DNS provider lúc DNSSEC đang on** → phải tắt DNSSEC trước (xóa DS), đợi 48h, rồi mới migrate.
- ❌ **Quên rotate KSK** → key cũ exposed. Cloudflare auto-rotate.

---

## 4️⃣ DoH vs DoT — Mã hóa DNS query

DNS truyền thống **cleartext qua UDP port 53** → ISP/attacker biết bạn query domain nào. Modern fix:

### DoH (DNS over HTTPS)

DNS query gửi qua **HTTPS** (port 443), giống mọi HTTPS request khác.

```
Client → 1.1.1.1:443 (HTTPS) → DNS response
         ↑ ISP chỉ thấy HTTPS đến 1.1.1.1, không biết hỏi domain gì
```

**Provider DoH:**
- Cloudflare: `https://cloudflare-dns.com/dns-query`
- Google: `https://dns.google/dns-query`
- Quad9: `https://dns.quad9.net/dns-query`

**Bật DoH:**
- Chrome: `chrome://settings/security` → "Use secure DNS" → custom → Cloudflare
- Firefox: Preferences → Network Settings → "Enable DNS over HTTPS"
- Windows 11: Settings → Network → DNS → DoH on
- macOS 11+: thông qua MDM profile

### DoT (DNS over TLS)

DNS query qua **TLS** dedicated port **853**.

```
Client → 1.1.1.1:853 (TLS) → DNS response
```

**Khi nào dùng DoT thay vì DoH:**

| Tiêu chí | DoH | DoT |
|---|---|---|
| Hoạt động ở port phổ thông | ✅ 443 (như HTTPS) | ❌ 853 (dễ bị firewall chặn) |
| Khó chặn | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Browser support | ✅ Chrome/FF native | ❌ Cần OS support |
| Android/iOS native | ❌ App level | ✅ "Private DNS" Android 9+ |
| Performance | Slightly slower (HTTPS overhead) | Faster (TLS direct) |

→ **2026 reality**: DoH chính cho browser. DoT chính cho mobile/OS-level.

### Drawback

- ❌ **Corporate firewall** không inspect được DNS → IT compliance issue.
- ❌ **Parental filter** (OpenDNS family) bypass → con cái lách qua DoH.
- ⚠️ Browser DoH có thể **conflict** với corporate DNS — IT phải config policy.

---

## 5️⃣ 4 attack DNS phổ biến

### Attack 1 — DNS Spoofing / Cache Poisoning

**Mục tiêu**: inject response giả vào resolver cache.

**Phương thức**:
- Predict transaction ID (16 bit, brute force được).
- Send response giả faster than auth real (Kaminsky attack 2008).

**Defend**:
- ✅ DNSSEC (verify chữ ký).
- ✅ Random source port (resolver nhập 0x20-bit entropy).
- ✅ DoH/DoT (encrypted = không inject được).

### Attack 2 — DNS Hijacking

**Mục tiêu**: trỏ domain về server attacker.

**Phương thức**:
- Compromise registrar account (phishing email reset password).
- Compromise DNS provider account.
- Compromise authoritative NS infrastructure.

**Defend**:
- ✅ 2FA registrar + DNS provider (mandatory).
- ✅ Registrar lock (`Transfer Prohibited`).
- ✅ DNSSEC + Certificate Transparency (CT) monitoring (xem [crt.sh](https://crt.sh)).

> 📌 **Case lịch sử**: 2017 Brazilian bank — attacker hijacked DNS, redirect all banking traffic to phishing server cho 6 tiếng. Mất triệu đô.

### Attack 3 — DNS Tunneling

**Mục tiêu**: bypass firewall bằng cách giấu data trong DNS query.

**Phương thức**: encode data trong subdomain (`.payload-base64.attacker.com`). Authoritative NS attacker decode.

**Defend**:
- ✅ Monitor DNS traffic anomaly (subdomain dài bất thường).
- ✅ DNS firewall (Cloudflare Gateway, Cisco Umbrella).
- ✅ Block DoH ở perimeter (corporate).

### Attack 4 — DNS Amplification (DDoS)

**Mục tiêu**: dùng DNS resolver làm amplifier để DDoS victim.

**Phương thức**:
- Attacker spoof source IP = victim.
- Query `ANY` type → response 30-50x lớn hơn query.
- Resolver gửi response BIG về victim → bão data.

**Defend**:
- ✅ Resolver: disable open recursion (chỉ phục vụ subnet nội bộ).
- ✅ Rate limit response (RRL — Response Rate Limiting).
- ✅ Victim: dùng anti-DDoS provider (Cloudflare, AWS Shield).

---

## 6️⃣ 5 best practice production

1. **2FA mọi tài khoản** registrar + DNS provider — single account compromise = lose domain.
2. **Registrar Lock** bật — chống transfer trái phép.
3. **Auto-renew bật** — quên expire = mất domain (đã có công ty mất domain triệu đô vì quên gia hạn).
4. **Monitor expiry**: 60/30/7/1 ngày trước expiry → alert.
5. **Monitor certificate transparency** ([crt.sh](https://crt.sh)) — alert khi có cert lạ issue cho domain của bạn.

### Bonus — Backup zone file

```bash
# Cloudflare CLI
flarectl dns export acmeshop.vn > acmeshop.vn.zone

# AWS Route53
aws route53 list-resource-record-sets --hosted-zone-id Z123 > backup.json
```

→ Lưu backup git private repo. Disaster recovery dễ.

---

## 💡 Cạm bẫy thường gặp & Best practice

1. **Quên đổi nameserver thực sự** — Cloudflare báo "active" yêu cầu NS đã propagate. Nếu vẫn chưa, NS check fail. Check bằng `dig acmeshop.vn NS @1.1.1.1`.
2. **DNSSEC bật 1 nơi quên nơi kia** — bật ở Cloudflare nhưng quên thêm DS record ở registrar = site die.
3. **DoH bypass corporate filter** → IT phải biết và config policy. Đừng tự bật DoH trong môi trường công ty không hỏi.
4. **Domain expire** = mất quyền — sau 30-90 ngày redemption period, ai cũng có thể đăng ký lại. Auto-renew là cứu cánh.
5. **WHOIS privacy không che được khi disputes** → nếu kiện cáo, ICANN bắt registrar tiết lộ thông tin. Không phải "anonymous" tuyệt đối.

---

## 🧠 Tự kiểm tra (Self-check)

1. Bạn mua `mydomain.com` ở Namecheap, muốn dùng Cloudflare DNS. Các bước?
2. DNSSEC bật được ở Cloudflare nhưng `dig +dnssec mydomain.com` không thấy flag `ad` — vấn đề ở đâu?
3. Phân biệt DoH và DoT.
4. Tại sao "expired domain" bị mua mất rất nhanh?
5. 4 attack DNS chính là gì? Defense tương ứng?

<details>
<summary>Gợi ý đáp án</summary>

1. (1) Tạo zone ở Cloudflare → nhận 2 NS. (2) Vào Namecheap → Domain List → Manage → Nameservers → Custom DNS → paste 2 NS Cloudflare. (3) Đợi 1-24h propagate. (4) Cloudflare email "site active". (5) Thêm A/CNAME/MX record ở Cloudflare panel.

2. Quên thêm **DS record** ở registrar. DNSSEC chain: registry (.com) phải có DS record chỉ về KSK của bạn. Bật ở Cloudflare là tạo KSK; còn phải copy DS sang registrar.

3. **DoH**: DNS qua HTTPS port 443, giống HTTPS request. Browser native. Khó chặn. **DoT**: DNS qua TLS port 853, dedicated port. OS-level (Android Private DNS). Dễ bị firewall chặn.

4. Domain hot/short/keyword có **squatter list**. Khi expire, drop-catch service auto-register milliseconds sau khi available → bán lại giá cao. Auto-renew tránh được.

5. **Spoofing** → DNSSEC + random source port. **Hijacking** → 2FA + registrar lock. **Tunneling** → monitor anomaly. **Amplification** → disable open recursion + rate limit.
</details>

---

## ⚡ Tra cứu nhanh (Cheatsheet)

### Mua domain checklist

```
[ ] Chọn TLD (.com / .vn / .io / ...)
[ ] Chọn registrar (Cloudflare > Namecheap > Mắt Bão cho .vn)
[ ] Bật WHOIS privacy
[ ] Bật 2FA tài khoản registrar
[ ] Bật Registrar Lock
[ ] Set auto-renew
[ ] Verify email ICANN trong 15 ngày
```

### Setup DNS provider checklist

```
[ ] Tạo zone ở Cloudflare/Route53
[ ] Add records (A, CNAME, MX, TXT)
[ ] Đổi nameserver ở registrar
[ ] Đợi propagation (dnschecker.org)
[ ] Bật DNSSEC (nếu cần)
[ ] Bật 2FA tài khoản DNS provider
[ ] Backup zone file
```

### Security checklist

```
[ ] 2FA registrar + DNS + email recovery
[ ] Registrar lock
[ ] Auto-renew
[ ] Monitor expiry (calendar reminder 60/30/7 ngày)
[ ] Monitor crt.sh cho domain
[ ] DNSSEC nếu fintech/gov/health
[ ] DoH/DoT cho client browse
```

---

## 📚 Từ Điển Thuật Ngữ (Glossary)

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Registrar** | Công ty bán quyền dùng domain (Cloudflare, Namecheap) |
| **Registry** | Cơ quan giữ DB của 1 TLD (Verisign giữ `.com`, VNNIC giữ `.vn`) |
| **DNS provider** | Công ty host DNS zone (Cloudflare, Route53). Có thể trùng/khác registrar |
| **Nameserver (NS)** | Server authoritative trả lời cho zone |
| **Propagation** | Quá trình NS mới phổ biến toàn cầu (24-48h) |
| **DNSSEC** | DNS Security Extensions — ký số chống fake response |
| **KSK / ZSK** | Key Signing Key / Zone Signing Key — 2 key DNSSEC |
| **DS record** | Delegation Signer — chứa hash KSK, đặt ở registrar level |
| **DNSKEY** | Record chứa public key của zone |
| **RRSIG** | Chữ ký số trên record set (A, MX, ...) |
| **NSEC / NSEC3** | "Authenticated denial" — chứng minh record không tồn tại có chữ ký |
| **Trust anchor** | Root key pre-installed trong resolver — bắt đầu chain of trust |
| **DoH** | DNS over HTTPS — mã hóa DNS qua port 443 |
| **DoT** | DNS over TLS — mã hóa DNS qua port 853 |
| **DNS Spoofing** | Attacker inject response giả vào resolver cache |
| **DNS Hijacking** | Attacker chiếm registrar/DNS account → trỏ domain về server fake |
| **DNS Tunneling** | Encode data trong subdomain để bypass firewall |
| **DNS Amplification** | DDoS attack dùng resolver làm amplifier (response > query) |
| **WHOIS privacy** | Ẩn info đăng ký domain khỏi public WHOIS |
| **Registrar Lock** | Cờ chống transfer domain trái phép |

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học
- ⬅️ **Bài trước:** [DNS Tools — `dig`, `nslookup`, `host`, `whois` & cách debug](03_dns-tools.md)
- ↑ **Về cụm:** [dns README](../../README.md)

### 🧩 Các chủ đề có thể bạn quan tâm
- [HTTPS & TLS](../../../http-https/lessons/01_basic/04_https-tls.md) — DNSSEC bổ trợ TLS chứ không thay
- [HTTP headers — Security](../../../http-https/lessons/01_basic/03_http-headers.md) — HSTS bổ sung lớp bảo mật phía web

### 🌐 Tài nguyên tham khảo khác
- 📖 [Cloudflare: DNS security](https://www.cloudflare.com/learning/dns/dns-security/)
- 📖 [DNSSEC Resolver Test — Verisign](https://dnssec-debugger.verisignlabs.com/)
- 📖 [DoH vs DoT comparison — Cloudflare](https://blog.cloudflare.com/announcing-1111/)
- 📖 [Registrar lock explained — ICANN](https://www.icann.org/resources/pages/transfer-policy-2016-06-01-en)
- 📖 [Drop-catching domain industry — Krebs](https://krebsonsecurity.com/2019/12/inside-the-secret-world-of-drop-catching/)
- 📖 [crt.sh — Certificate Transparency search](https://crt.sh)

---

> 🎯 *Cluster DNS basic 5/5 đóng. Bạn giờ có đủ kiến thức: DNS là gì, records, resolution flow, debug tools, setup + security. Bài kế tiếp có thể vào **02_intermediate** (zone delegation nâng cao, anycast DNS, geo-routing) hoặc nhảy sang cluster khác (`tcp-ip-fundamentals`, `load-balancing`).*

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `dns/` lesson 5/5. Cover: đăng ký domain (TLD + registrar + pitfall) + đổi nameserver migration + DNSSEC chain of trust + DoH/DoT modern privacy + 5 attack/defense (cache poisoning, DNS hijack, NXDOMAIN attack, tunneling, zone transfer).
- **v1.1.0** — Thêm **DNSSEC 4 records** (DNSKEY/RRSIG/DS/NSEC) + **chain of trust flow** + adoption stats.
- **v1.2.0 (25/05/2026)** — Bổ sung lead-in trước các bảng ở §1 (TLD table, Registrar table, pitfall mua domain), §2 (migration timeline), §3 (DNSSEC "4 loại record"). Thêm Changelog section.
