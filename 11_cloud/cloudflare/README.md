# ☁️ Cloudflare

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 01/06/2026\
> **Status:** ✅ Basic cluster hoàn chỉnh (5/5 bài)

> 🎯 *Cloudflare — vendor edge-first 320+ POPs toàn cầu. 3 trụ cột: Network (CDN/DNS/SSL), Security (WAF/Bot/DDoS/Zero Trust), Developer Platform (Workers/Pages/R2/D1). Khác paradigm AWS/GCP — edge-distributed.*

---

## 🚀 Quick start

- [00_what-is-cloudflare-overview](lessons/01_basic/00_what-is-cloudflare-overview.md)
- [01_cdn-dns-and-ssl](lessons/01_basic/01_cdn-dns-and-ssl.md)
- [02_workers-and-pages](lessons/01_basic/02_workers-and-pages.md)
- [03_r2-and-d1-and-queues](lessons/01_basic/03_r2-and-d1-and-queues.md)
- [04_security-zero-trust-and-waf](lessons/01_basic/04_security-zero-trust-and-waf.md)

---

## 📖 Lessons — Basic cluster (5 bài)

| # | Bài | Trọng tâm |
| --- | --- | --- |
| 00 | [Cloudflare overview](lessons/01_basic/00_what-is-cloudflare-overview.md) | 3 pillars + Account/Zone + wrangler + Free Tier |
| 01 | [CDN + DNS + SSL](lessons/01_basic/01_cdn-dns-and-ssl.md) | DNS proxied + SSL modes + Cache rules + Universal SSL |
| 02 | [Workers + Pages](lessons/01_basic/02_workers-and-pages.md) | V8 isolate edge + KV + Durable Objects + Pages |
| 03 | [R2 + D1 + Queues](lessons/01_basic/03_r2-and-d1-and-queues.md) | R2 zero egress + D1 SQLite edge + Queues + Hyperdrive |
| 04 | [Security + Zero Trust + WAF](lessons/01_basic/04_security-zero-trust-and-waf.md) | WAF + Bot + DDoS + Zero Trust + cloudflared + Turnstile |


---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ↑ **Về cụm:** [11_cloud — Cloud Platforms](../README.md)

### 🧩 Các chủ đề liên quan

- ☁️ [AWS](../aws/), [GCP](../gcp/) — đóng vai *origin server* phía sau Cloudflare edge
- ↑ **Về cụm:** [DNS cluster](../../05_networking/dns/) — nền tảng để hiểu phần DNS proxied của Cloudflare

### 🌐 Tài nguyên tham khảo khác

- 📖 [Cloudflare docs](https://developers.cloudflare.com/)
- 📖 [Workers docs](https://developers.cloudflare.com/workers/)
- 📖 [Zero Trust docs](https://developers.cloudflare.com/cloudflare-one/)

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (24/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. Edge-first paradigm, khác region-based AWS/GCP.
- **v1.1.0 (01/06/2026)** — Chuẩn hoá mục Liên kết & Tài nguyên theo 3 sub-section chuẩn (Định hướng / Chủ đề liên quan / Tài nguyên tham khảo).
