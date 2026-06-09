# dns

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Cập nhật:** 25/05/2026\
> **Status:** ✅ Có bài — cụm `01_basic` đã hoàn chỉnh (5 bài)

## 🎯 Chủ đề này có gì

DNS (Domain Name System) — danh bạ Internet dịch domain (`google.com`) thành IP. Cụm bài cơ bản đi từ "DNS là gì" → records → resolution flow → tools debug → setup + security.

## 📖 Lessons — 01_basic

| # | Bài | Nội dung |
|---|---|---|
| 00 | [DNS là gì](lessons/01_basic/00_what-is-dns.md) | Danh bạ Internet, flow domain → IP, anatomy domain, cache + TTL |
| 01 | [DNS Records](lessons/01_basic/01_dns-records.md) | A/AAAA/CNAME/MX/TXT/NS/SOA + zone file thực tế |
| 02 | [DNS Resolution](lessons/01_basic/02_dns-resolution.md) | Recursive vs iterative, 5 layer cache, propagation, flush |
| 03 | [DNS Tools](lessons/01_basic/03_dns-tools.md) | `dig`, `nslookup`, `host`, `whois` + 5 case debug |
| 04 | [DNS Setup & Security](lessons/01_basic/04_dns-setup-and-security.md) | Đăng ký domain, đổi nameserver, DNSSEC, DoH/DoT, 4 attack |

## 🚀 Đọc folder này thế nào

| Nhu cầu | Đọc gì |
|---|---|
| Mới bắt đầu | `lessons/01_basic/00_what-is-dns.md` rồi đi tuần tự 00 → 04 |
| Tra nhanh records / tool | `lessons/01_basic/01_dns-records.md`, `lessons/01_basic/03_dns-tools.md` (có cheatsheet cuối bài) |
| Theo nghề | Xem [`../00_roadmaps/career/`](../../00_roadmaps/career/) chọn career path đi qua DNS |

## 📂 Cấu trúc

```
dns/
├── README.md                ← (file này) index + lộ trình đọc
├── lessons/01_basic/        ← 5 bài cơ bản (đã có)
├── exercises/               ← bài tập (chưa có)
├── recipes/                 ← công thức / troubleshooting (chưa có)
└── setup/                   ← cài đặt + cấu hình (chưa có)
```
