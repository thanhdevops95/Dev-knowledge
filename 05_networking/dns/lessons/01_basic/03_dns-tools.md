# 🎓 DNS Tools — `dig`, `nslookup`, `host`, `whois` & cách debug

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 23/05/2026\
> **Cập nhật:** 25/05/2026\
> **Level:** Basic\
> **Tags:** [MUST-KNOW]\
> **Thời lượng đọc:** ~15 phút\
> **Prerequisites:** [DNS Records](01_dns-records.md), [DNS Resolution](02_dns-resolution.md)

> 🎯 *Học 4 lệnh CLI để query/debug DNS thật. Sau bài này bạn debug được "vì sao DNS sai" trong 2 phút thay vì 2 giờ.*

## 🎯 Sau bài này bạn sẽ

- [ ] Dùng được **`dig`** — Swiss army knife của DNS
- [ ] Dùng được **`nslookup`** — phổ thông trên Windows
- [ ] Dùng được **`host`** — gọn nhất, cho script
- [ ] Dùng được **`whois`** — info domain owner + registrar
- [ ] Đọc được output `dig` chi tiết (5 section)
- [ ] Biết **5 case debug DNS** phổ biến + cách query
- [ ] So sánh tool nào tốt cho task nào

---

## Tình huống — Bạn debug "DNS lỗi" mà không biết lỗi ở đâu

Bạn deploy site mới `shop.acmeshop.vn`. User báo: *"Site không vào được."*

Bạn check trình duyệt: `ERR_NAME_NOT_RESOLVED`. Bạn đoán "DNS sai". Mở Cloudflare → thấy CNAME đã add đúng. Vẫn không vào được.

Bạn ngơ:
- DNS server **trả gì khi query**? Đúng hay sai?
- Có phải **cache stale** ở resolver?
- Cloudflare **đã serve record này chưa**?
- Authoritative NS đúng không?

→ Cách duy nhất biết: **query DNS thẳng** từ terminal. Bài này dạy bạn (và bạn) 4 tool CLI thuần để vạch ra "DNS sai ở layer nào".

---

## 1️⃣ `dig` — vua của các tool

**`dig`** = **Domain Information Groper** — đến từ bộ BIND, có sẵn trên macOS/Linux. Windows cần cài qua [BIND Tools](https://www.isc.org/download/) hoặc dùng WSL.

### Syntax cơ bản

`dig` có **4 phần** trong syntax — mỗi phần tùy chọn (trừ `name`). Cấu trúc rất linh hoạt: chỉ định resolver, loại record, format output đều được qua flag. Bảng giải thích từng phần:

```bash
dig [@server] [name] [type] [+options]
```

| Phần | Ý nghĩa | Default |
|---|---|---|
| `@server` | Hỏi resolver/auth nào | Resolver mặc định OS |
| `name` | Domain query | (required) |
| `type` | Loại record (A/MX/TXT/NS...) | A |
| `+options` | Thêm chi tiết | — |

### Ví dụ tiêu chuẩn

Lệnh đơn giản nhất `dig google.com` cho ra output có **6 section** đầy đủ — nhiều info hơn `nslookup` hoặc `host`. Đây là output bạn sẽ gặp daily khi debug:

```bash
$ dig google.com

; <<>> DiG 9.10.6 <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 42891
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             300     IN      A       142.250.190.46

;; Query time: 23 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)
;; WHEN: Thu May 23 14:00:00 +07 2026
;; MSG SIZE  rcvd: 55
```

### Đọc output — 5 section

Output `dig` chia thành **5+1 section** rõ ràng — đọc theo thứ tự sẽ chẩn đoán được vấn đề. Quan trọng nhất là `status` (NOERROR/NXDOMAIN/SERVFAIL) ở HEADER và record trong ANSWER:

| Section | Ý nghĩa |
|---|---|
| **HEADER** | Metadata: opcode, status, flags. `status: NOERROR` = OK. `NXDOMAIN` = domain không tồn tại. |
| **QUESTION** | Câu hỏi gửi đi: `google.com IN A` |
| **ANSWER** | **Câu trả lời quan trọng nhất**: TTL + record |
| **AUTHORITY** | NS responsible (đôi khi hiển thị) |
| **ADDITIONAL** | Bonus info (IP của NS, etc.) |
| **Footer** | Query time + server hỏi + timestamp |

### Tham số `+` hữu ích

`dig` có **~50 flag `+`** điều chỉnh output — nhớ 5-6 cái dưới là đủ cho 95% case. `+short` cho output 1 dòng dùng trong script, `+trace` cho debug đường đi DNS:

```bash
dig +short google.com           # Chỉ trả IP, 1 dòng
# 142.250.190.46

dig +trace google.com           # Toàn bộ đường đi root → TLD → auth
# Hữu ích khi debug "DNS đi qua server nào"

dig +noall +answer google.com   # Chỉ ANSWER section, bỏ verbose
# google.com. 300 IN A 142.250.190.46

dig +nostats google.com         # Bỏ footer
dig +nocomments google.com      # Bỏ comments
dig +tcp google.com             # TCP thay UDP (DNS dùng UDP default, TCP cho query lớn)
```

### Query loại record cụ thể

Mặc định `dig` query A record (IPv4). Thêm record type ở cuối để hỏi MX/NS/TXT/AAAA/SOA. 6 dạng dùng phổ biến khi debug email setup, IPv6, hoặc verify TXT:

```bash
dig google.com MX               # Mail server
dig google.com NS               # Nameservers
dig google.com TXT              # SPF, verification
dig google.com AAAA             # IPv6
dig google.com SOA              # Zone metadata
dig google.com ANY              # Tất cả (nhiều server từ chối để chống abuse)
```

### Hỏi server cụ thể (bypass cache)

```bash
dig @1.1.1.1 google.com         # Hỏi Cloudflare
dig @8.8.8.8 google.com         # Hỏi Google
dig @ns1.google.com google.com  # Hỏi authoritative trực tiếp (source of truth)
```

→ Khi 2 resolver trả khác nhau = **1 trong 2 đang cache stale**. Auth là chân lý.

### Reverse DNS — IP → domain

```bash
dig -x 142.250.190.46

;; ANSWER SECTION:
46.190.250.142.in-addr.arpa. 86400 IN PTR sof02s32-in-f14.1e100.net.
```

→ `PTR` record. `1e100.net` = `10^100` = Google.

---

## 2️⃣ `nslookup` — phổ thông, có trên Windows

**`nslookup`** = **Name Server Lookup** — có trên Windows/Mac/Linux mặc định. Đơn giản hơn `dig`, ít chi tiết hơn.

### Cú pháp

```bash
nslookup [name] [server]
```

### Ví dụ

```bash
$ nslookup google.com

Server:    192.168.1.1
Address:   192.168.1.1#53

Non-authoritative answer:
Name:    google.com
Address: 142.250.190.46
```

→ "**Non-authoritative answer**" = từ resolver cache, không phải auth.

### Query loại record

```bash
nslookup -type=MX google.com
nslookup -type=NS google.com
nslookup -type=TXT google.com
```

### Hỏi server cụ thể

```bash
nslookup google.com 1.1.1.1
nslookup google.com 8.8.8.8
```

### Interactive mode

```bash
$ nslookup
> set type=MX
> google.com
> set type=NS
> github.com
> exit
```

→ Hữu ích khi query nhiều domain liên tục.

### `nslookup` vs `dig`?

| Tiêu chí | `nslookup` | `dig` |
|---|---|---|
| Có sẵn Windows | ✅ | ❌ (cần cài) |
| Output gọn | ✅ | ❌ (verbose) |
| Chi tiết debug | ❌ | ✅ |
| Hiện TTL | ❌ | ✅ |
| `+trace` (full path) | ❌ | ✅ |
| Recommend | Khi cần nhanh | Khi debug |

---

## 3️⃣ `host` — gọn nhất, cho script

**`host`** = utility BIND, gọn nhất. Có trên Linux/Mac, không có Windows.

```bash
$ host google.com
google.com has address 142.250.190.46
google.com has IPv6 address 2607:f8b0:4006:823::200e
google.com mail is handled by 10 smtp.google.com.
```

→ 1 lệnh trả nhiều record (A + AAAA + MX) — best cho mục đích "check toàn diện".

### Query loại record

```bash
host -t MX google.com
host -t NS github.com
host -t TXT _dmarc.acmeshop.vn
```

### Verbose

```bash
host -v google.com              # Verbose (gần giống dig)
host -a google.com              # All record types
```

### Cho script

```bash
# Lấy IP để dùng trong script
IP=$(host -t A example.com | awk '{print $4}')
echo "IP is $IP"
```

→ Output predictable hơn `dig`, dễ parse.

---

## 4️⃣ `whois` — info đăng ký domain

**`whois`** không phải tool DNS thuần — query database **WHOIS** chứa info đăng ký domain: owner, registrar, expiry, contact.

```bash
$ whois google.com

Domain Name: GOOGLE.COM
Registry Domain ID: 2138514_DOMAIN_COM-VRSN
Registrar: MarkMonitor Inc.
Updated Date: 2024-09-09T15:39:04Z
Creation Date: 1997-09-15T04:00:00Z
Registry Expiry Date: 2028-09-14T04:00:00Z
Name Server: NS1.GOOGLE.COM
Name Server: NS2.GOOGLE.COM
...
```

### Use case `whois`

| Hỏi gì | Câu trả lời |
|---|---|
| Domain còn không? | "No match for ..." = available |
| Khi expire? | `Registry Expiry Date` |
| Registrar nào? | `Registrar` |
| Ai chủ? (nếu chưa privacy) | `Registrant Name/Org` |
| Nameserver hiện tại? | `Name Server` |

→ Privacy GDPR (2018) ẩn nhiều info cá nhân. Domain `.com` còn 1 phần, `.eu`/`.de` gần như ẩn hết.

### Phiên bản web

- [whois.com](https://whois.com)
- [who.is](https://who.is)
- ICANN lookup: [lookup.icann.org](https://lookup.icann.org)

---

## 5️⃣ Bảng so sánh 4 tool

| Tool | Có sẵn | Output | Debug power | Best for |
|---|---|---|---|---|
| **dig** | Linux/Mac | Verbose, đủ field | ⭐⭐⭐⭐⭐ | Debug DNS chuyên sâu |
| **nslookup** | All OS | Gọn | ⭐⭐⭐ | Check nhanh, Windows |
| **host** | Linux/Mac | Gọn nhất | ⭐⭐⭐⭐ | Script, check toàn diện 1 lệnh |
| **whois** | Linux/Mac (cài Windows) | Bản đăng ký | — | Info domain owner/expiry |

→ **Bắt buộc thuộc lòng:** `dig +short`, `dig @1.1.1.1`, `dig +trace`, `nslookup` (Windows).

---

## 6️⃣ 5 case debug DNS phổ biến

### Case 1 — "Site mới deploy, vào không được"

```bash
# Step 1: Hỏi authoritative trực tiếp (source of truth)
dig @ns1.cloudflare.com acmeshop.vn

# Step 2: So sánh với resolver public
dig @1.1.1.1 acmeshop.vn
dig @8.8.8.8 acmeshop.vn

# Step 3: Hỏi resolver mặc định (cache ISP)
dig acmeshop.vn
```

→ Khác kết quả = **cache stale** ở 1 trong 3.

→ Giống = config sai (sai IP, sai CNAME).

### Case 2 — "Email tới domain bị bounce"

```bash
# Check MX records
dig acmeshop.vn MX

# Check SPF
dig acmeshop.vn TXT | grep spf

# Check DMARC
dig _dmarc.acmeshop.vn TXT

# Check DKIM (cần biết selector — google._domainkey, k1._domainkey...)
dig google._domainkey.acmeshop.vn TXT
```

→ Thiếu/sai record nào = email broken.

### Case 3 — "SSL cert lỗi domain mismatch"

```bash
# Check domain trỏ đúng server không
dig +short acmeshop.vn
# 203.0.113.10

# Server có cert cho domain đó không?
openssl s_client -connect 203.0.113.10:443 -servername acmeshop.vn </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates
```

→ Xem [bài HTTPS](../../../http-https/lessons/01_basic/04_https-tls.md).

### Case 4 — "Subdomain mới tạo không hoạt động"

```bash
# 1. Hỏi auth trực tiếp
dig @ns1.cloudflare.com api.acmeshop.vn

# 2. Nếu auth có nhưng resolver không có:
#    → Negative cache stale ở resolver
#    → Đợi SOA minimum TTL hoặc switch resolver tạm thời
dig @1.1.1.1 api.acmeshop.vn

# 3. Flush OS cache
sudo dscacheutil -flushcache  # Mac
```

### Case 5 — "DNS spoof? Có ai chặn DNS của tao?"

```bash
# Hỏi nhiều resolver công khai, so sánh
for srv in 1.1.1.1 8.8.8.8 9.9.9.9 208.67.222.222; do
  echo "=== $srv ==="
  dig @$srv +short google.com
done

# Cả 4 trả khác nhau với resolver mặc định = ISP đang chặn/redirect
dig +short google.com
```

→ Nếu ISP redirect (kiểu chặn 4chan/torrent), giá trị return sẽ khác hẳn.

---

## 7️⃣ Online tool — khi không có terminal

| Tool | URL | Use case |
|---|---|---|
| **DNSchecker** | [dnschecker.org](https://dnschecker.org) | Check propagation 30+ resolver toàn cầu |
| **MXToolbox** | [mxtoolbox.com](https://mxtoolbox.com) | Check MX + SPF + DKIM + blacklist |
| **WhatsMyDNS** | [whatsmydns.net](https://whatsmydns.net) | Propagation worldwide visual |
| **Google Public DNS** | [dns.google](https://dns.google) | Query DNS qua HTTPS, browser thân thiện |
| **DNSViz** | [dnsviz.net](https://dnsviz.net) | Phân tích DNSSEC chain |
| **WHOIS** | [whois.com](https://whois.com), [lookup.icann.org](https://lookup.icann.org) | Info domain owner |
| **CrtSh** | [crt.sh](https://crt.sh) | Check certs đã issue cho domain (Cert Transparency) |

---

## 8️⃣ Tips chuyên gia

### Tip 1 — Alias `dig` cho quick check

```bash
# ~/.zshrc
alias d='dig +short'
alias da='dig @1.1.1.1 +short'
alias dt='dig +trace'
```

→ `d google.com` → 142.250.190.46 (1 dòng).

### Tip 2 — Script check propagation đa-resolver

```bash
#!/bin/bash
# check-propagate.sh <domain>
DOMAIN=$1
for srv in 1.1.1.1 8.8.8.8 9.9.9.9 208.67.222.222 \
           203.162.4.191 8.26.56.26; do
  printf "%-20s %s\n" "$srv" "$(dig @$srv +short $DOMAIN | head -1)"
done
```

### Tip 3 — Check toàn diện 1 lệnh

```bash
# Function ~/.zshrc
dnsfull() {
  for t in A AAAA MX NS TXT SOA; do
    echo "=== $t ==="
    dig +short $1 $t
  done
}
# dnsfull acmeshop.vn
```

### Tip 4 — Reverse DNS xem ai gửi spam

```bash
# Spam email ghi IP 198.51.100.42
dig -x 198.51.100.42 +short
# 42.100.51.198.in-addr.arpa. → server-name.example.com.
```

→ Trace gốc spam.

---

## ⚠️ 5 pitfall hay vướng

1. **`dig google.com` không bypass cache** → vẫn dùng resolver ISP. Phải `dig @1.1.1.1` hoặc `+trace`.
2. **Tin `dig` 100%** → resolver ISP có thể cache stale. Luôn so sánh ít nhất 2 resolver.
3. **`nslookup` trên Windows lỗi format** → ít chi tiết hơn `dig`. Dùng `nslookup -debug -type=A google.com`.
4. **Quên TTL trong output** → `dig` show TTL còn lại (đếm ngược). 100 lần dig liên tiếp sẽ thấy TTL giảm dần — bình thường, không phải bug.
5. **WHOIS data lỗi thời** → registrar có thể chưa sync. Hỏi nhiều WHOIS server (`whois -h whois.iana.org google.com`).

---

## ✅ Self-check

1. Lệnh nhanh nhất để chỉ lấy IP của 1 domain?
2. Cách hỏi authoritative NS trực tiếp (bypass cache resolver)?
3. Lệnh check toàn bộ chuỗi root → TLD → auth?
4. Tool nào tốt nhất cho debug propagation đa-vùng địa lý?
5. Khi nào dùng `whois` thay vì `dig`?

<details>
<summary>Gợi ý đáp án</summary>

1. `dig +short example.com` (1 dòng) hoặc `host example.com` (gồm A+AAAA+MX).

2. `dig @<auth-ns> example.com`. Tìm `<auth-ns>` bằng `dig example.com NS` trước. Ví dụ: `dig @ns1.cloudflare.com acmeshop.vn`.

3. `dig +trace example.com` — chạy iterative từ root, không dùng resolver cache.

4. **DNSchecker.org** (web) — show 30+ resolver toàn cầu cùng lúc. Terminal `dig` chỉ check 1 resolver tại thời điểm.

5. Khi muốn biết **info đăng ký** (owner, registrar, expiry date), KHÔNG phải IP/MX/CNAME. `whois example.com`.
</details>

---

## ⚡ Cheatsheet

### `dig` essentials

```bash
dig example.com                       # Default — A record
dig +short example.com                # Chỉ IP
dig example.com MX                    # Mail server
dig example.com NS                    # Nameserver
dig example.com TXT                   # SPF, DKIM, verify
dig @1.1.1.1 example.com              # Hỏi resolver cụ thể
dig @ns1.example.com example.com      # Hỏi auth (source of truth)
dig +trace example.com                # Full chain root→TLD→auth
dig -x 142.250.190.46                 # Reverse: IP → domain
dig +short example.com @1.1.1.1 +tries=2 +time=3   # Reliable timeout
```

### `nslookup` essentials

```bash
nslookup example.com
nslookup -type=MX example.com
nslookup example.com 1.1.1.1
nslookup -debug example.com           # Verbose
```

### `host` essentials

```bash
host example.com                      # All record types ngầm
host -t MX example.com
host -a example.com                   # Show tất cả
```

### `whois` essentials

```bash
whois example.com
whois -h whois.iana.org example.com   # Hỏi IANA root WHOIS
whois 8.8.8.8                         # WHOIS IP (ai sở hữu IP)
```

---

## 📘 Glossary

| Thuật ngữ | Ý nghĩa |
|---|---|
| **`dig`** | Domain Information Groper — DNS query CLI tool chính |
| **`nslookup`** | Name Server Lookup — DNS query CLI cũ, có sẵn mọi OS |
| **`host`** | DNS query CLI gọn, output predictable |
| **`whois`** | Query WHOIS database — info đăng ký domain |
| **PTR record** | Pointer — reverse DNS (IP → domain) |
| **Non-authoritative answer** | Trả lời từ resolver cache, không phải từ auth |
| **Source of truth** | Authoritative NS — câu trả lời gốc của domain |
| **WHOIS** | Database public chứa info đăng ký domain |
| **Reverse DNS** | Tra ngược IP → domain (qua PTR record) |

---

## 🔗 Links

### Trong cluster
- ← Trước: [DNS Resolution](02_dns-resolution.md)
- → Tiếp: [DNS Setup & Security](04_dns-setup-and-security.md)
- ↑ Cluster: [dns README](../../README.md)

### External
- 📖 [DigitalOcean: dig tutorial](https://www.digitalocean.com/community/tutorials/an-introduction-to-dns-terminology-components-and-concepts)
- 📖 [Julia Evans: How DNS works (zine)](https://wizardzines.com/zines/dns/)
- 📖 [Cloudflare: DNS troubleshooting](https://developers.cloudflare.com/dns/troubleshooting/)
- 📖 [Manpage `dig(1)`](https://man7.org/linux/man-pages/man1/dig.1.html)

---

> 🎯 *Sau bài này bạn có 4 vũ khí debug DNS thật. Bài cuối cluster — `04_dns-setup-and-security.md` — dạy đăng ký domain, đổi nameserver, propagation, DNSSEC, DoH/DoT.*

---

## 📌 Changelog

- **v1.1.0 (25/05/2026)** — Apply Blueprint v0.5.4+ §3.6: thêm lead-in 2-3 câu trước §1 dig "Syntax cơ bản" + "Ví dụ tiêu chuẩn" + "Đọc output 5 section" bảng + "Tham số +" flag list + "Query loại record" examples. Thêm Changelog section.

- **v1.0.0 (23/05/2026)** — Bản đầu tiên. Cluster `dns/` lesson 4/5. Cover: 4 tool (`dig` deep + `nslookup` basic + `host` quick + `whois` registrar info) + decision tree khi dùng tool nào + 5 use case debug DNS + DoH/DoT modern (DNS over HTTPS/TLS).
