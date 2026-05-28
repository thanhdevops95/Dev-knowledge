# 🌐 DNS — Hệ thống phân giải tên miền

> `[BEGINNER]` ⭐ `[MUST-KNOW]` — Tại sao gõ google.com lại vào đúng trang Google?

---

## Tại sao cần DNS?

Máy tính giao tiếp bằng **IP address** (142.250.190.78), con người nhớ bằng **tên miền** (google.com).

**DNS** (Domain Name System) = "danh bạ điện thoại" của internet — dịch tên miền → IP.

---

## 1. Quá trình phân giải DNS

```
Bạn gõ: google.com
         │
         ▼
┌─────────────────┐
│ Browser Cache   │ → Đã truy cập gần đây? → Có → Dùng IP đã lưu
└────────┬────────┘
         │ Không có
         ▼
┌─────────────────┐
│   OS Cache      │ → /etc/hosts hoặc OS DNS cache?
└────────┬────────┘
         │ Không có
         ▼
┌─────────────────┐
│ Recursive       │ → DNS resolver của ISP / Google (8.8.8.8)
│ Resolver        │   Đã cache? → Có → Trả IP
└────────┬────────┘
         │ Không có → Hỏi lần lượt:
         ▼
┌─────────────────┐
│ Root Server (.) │ → "google.com? Tôi không biết, hỏi .com server"
│ (13 cluster)    │   Trả: TLD server cho .com
└────────┬────────┘
         ▼
┌─────────────────┐
│ TLD Server      │ → ".com? Tôi biết nameserver của google.com"
│ (.com, .org...) │   Trả: ns1.google.com
└────────┬────────┘
         ▼
┌─────────────────┐
│ Authoritative   │ → "google.com = 142.250.190.78"
│ DNS Server      │   Trả IP cuối cùng!
└─────────────────┘
         │
         ▼
    Trả IP cho browser → Kết nối HTTP
```

> Toàn bộ quá trình này thường mất **< 50ms**. Kết quả được cache → lần sau nhanh hơn.

---

## 2. DNS Record Types

| Type | Mục đích | Ví dụ |
|---|---|---|
| **A** | Domain → IPv4 | `google.com → 142.250.190.78` |
| **AAAA** | Domain → IPv6 | `google.com → 2607:f8b0:4004::` |
| **CNAME** | Alias → Domain khác | `www.example.com → example.com` |
| **MX** | Mail server | `example.com → mail.google.com` (priority 10) |
| **TXT** | Text tùy ý | SPF, DKIM, domain verification |
| **NS** | Nameserver | `example.com → ns1.cloudflare.com` |
| **SOA** | Start of Authority | Zone info, serial, refresh |
| **SRV** | Service location | `_sip._tcp.example.com → sip.example.com:5060` |
| **PTR** | Reverse DNS (IP → Domain) | `78.190.250.142 → google.com` |

```bash
# Tra cứu DNS records
nslookup google.com
dig google.com A
dig google.com MX
dig google.com ANY

# Trace quá trình phân giải
dig +trace google.com
```

---

## 3. DNS Caching & TTL

```
DNS Record: google.com  A  142.250.190.78  TTL: 300

TTL (Time To Live) = 300 giây = 5 phút
→ Cache giữ record 5 phút, sau đó query lại

TTL ngắn (60s):  Thay đổi DNS nhanh (failover)
TTL dài (86400): Ít query, giảm latency (trang ổn định)
```

---

## 4. CNAME vs A Record

```
A Record:     example.com → 93.184.216.34     (IP cụ thể)
CNAME Record: www.example.com → example.com   (alias)

Khi nào dùng CNAME?
• www → root domain
• CDN: assets.example.com → d1234.cloudfront.net
• Load Balancer: api.example.com → lb-abc.aws.com

⚠️ CNAME KHÔNG dùng cho root domain (example.com)!
   Root domain phải dùng A hoặc ALIAS record
```

---

## 5. DNS trong thực tế

### Cấu hình domain cho web app

```
# Cloudflare / Route53 / GoDaddy DNS settings:

# Root domain → Load Balancer
example.com       A      → 203.0.113.50

# www redirect
www.example.com   CNAME  → example.com

# API subdomain
api.example.com   A      → 203.0.113.51

# Email (Google Workspace)
example.com       MX     → aspmx.l.google.com (priority 1)
example.com       MX     → alt1.aspmx.l.google.com (priority 5)

# Email authentication
example.com       TXT    → "v=spf1 include:_spf.google.com ~all"

# Domain verification
example.com       TXT    → "google-site-verification=abc123..."
```

### DNS-based Load Balancing

```
example.com  A  → 93.184.216.34   (Server US)
example.com  A  → 203.0.113.50    (Server EU)
example.com  A  → 198.51.100.10   (Server Asia)

DNS trả về IP gần user nhất (GeoDNS / Anycast)
```

---

## 6. Bảo mật DNS

```
Rủi ro:
• DNS Spoofing/Poisoning: Attacker trả IP giả → redirect user đến trang giả
• DNS Hijacking: Chiếm quyền DNS settings
• DDoS on DNS: Tấn công DNS server → website không resolve được

Giải pháp:
• DNSSEC: Chữ ký số verify DNS response là authentic
• DoH (DNS over HTTPS): Mã hóa DNS queries
• DoT (DNS over TLS): Mã hóa DNS qua TLS
```

---

## Các lỗi thường gặp

```
❌ Sai: Đổi DNS xong expect thấy ngay
✅ Đúng: DNS propagation mất 5 phút → 48 giờ (tùy TTL cũ)

❌ Sai: CNAME cho root domain
✅ Đúng: Root domain dùng A record hoặc ALIAS (Cloudflare)

❌ Sai: Quên set MX record → không nhận email
✅ Đúng: Luôn check MX record khi setup email cho domain
```

---

## Bài tập thực hành

- [ ] Dùng `dig` hoặc `nslookup` tra DNS records của 5 website
- [ ] Setup domain cho 1 project (Vercel/Netlify + custom domain)
- [ ] Cấu hình MX record cho Google Workspace
- [ ] Dùng `dig +trace` xem toàn bộ quá trình phân giải

---

## Tài nguyên thêm

- [How DNS Works (Comic)](https://howdns.works/) — Giải thích bằng truyện tranh
- [DNS Lookup Tool](https://mxtoolbox.com/) — Kiểm tra DNS records online
- [Cloudflare Learning Center — DNS](https://www.cloudflare.com/learning/dns/what-is-dns/) — Giải thích rõ
