# ☁️ DigitalOcean

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 01/06/2026\
> **Status:** ✅ Basic cluster hoàn chỉnh (5/5 bài)

> 🎯 *DigitalOcean — vendor developer-first, pricing predictable. Phù hợp startup, small/medium team. Alternative cho Heroku (App Platform).*

---

## 🚀 Quick start

- [DigitalOcean — Tổng quan + Team/Project + doctl CLI](lessons/01_basic/00_what-is-digitalocean-overview.md)
- [Droplet + Block Storage Volumes — Compute cơ bản DO](lessons/01_basic/01_droplets-and-volumes.md)
- [Spaces — Object Storage + CDN built-in](lessons/01_basic/02_spaces-object-storage-and-cdn.md)
- [Managed Databases — Postgres / MySQL / Redis / MongoDB / Kafka](lessons/01_basic/03_managed-databases.md)
- [App Platform + Functions + DOKS — PaaS + Serverless + K8s](lessons/01_basic/04_app-platform-and-functions.md)

---

## 📖 Lessons — Basic cluster (5 bài)

| # | Bài | Trọng tâm |
|---|---|---|
| 00 | [DO overview](lessons/01_basic/00_what-is-digitalocean-overview.md) | Team/Project + doctl + Tier Pricing |
| 01 | [Droplets + Volumes](lessons/01_basic/01_droplets-and-volumes.md) | Basic/Premium CPU + Volumes + Reserved IP + Snapshot |
| 02 | [Spaces + CDN](lessons/01_basic/02_spaces-object-storage-and-cdn.md) | S3-compatible + CDN built-in + tier pricing |
| 03 | [Managed DBs](lessons/01_basic/03_managed-databases.md) | Postgres/MySQL/Mongo/Redis/Kafka + standby + connection pooling |
| 04 | [App Platform + Functions](lessons/01_basic/04_app-platform-and-functions.md) | PaaS auto-build + Functions + DOKS |

→ **Tổng ~6-8h hands-on** cho cả cụm Basic.

---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ↑ **Về cụm:** [Cloud — Tổng quan các nền tảng đám mây](../README.md)
- ➡️ **Bài tiếp theo:** [DigitalOcean — Tổng quan + Team/Project + doctl CLI](lessons/01_basic/00_what-is-digitalocean-overview.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ **Vendor lớn hơn:** [AWS](../aws/), [GCP](../gcp/), [Azure](../azure/) — khi cần hệ sinh thái dịch vụ rộng và hiện diện toàn cầu.

### 🌐 Tài nguyên tham khảo khác

- [DO docs](https://docs.digitalocean.com/) — tài liệu chính thức của DigitalOcean.
- [doctl CLI](https://docs.digitalocean.com/reference/doctl/) — tham chiếu công cụ dòng lệnh chính thức.
- [DO Marketplace](https://marketplace.digitalocean.com/) — kho image và ứng dụng 1-click cài sẵn.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (24/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. Developer-first niche (alternative Heroku).
- **v1.1.0 (01/06/2026)** — QA fix: bỏ cột "Thời lượng" + dòng "~101 phút đọc" (field thời lượng đọc đã loại toàn kho); link text Quick start dùng tiêu đề H1 thực; chuẩn hoá phần Liên kết & Tài nguyên thành 3 sub canonical (🧭 Định hướng / 🧩 Chủ đề liên quan / 🌐 Tài nguyên khác) + marker ↑ Về cụm.
