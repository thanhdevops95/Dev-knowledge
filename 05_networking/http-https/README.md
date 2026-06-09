# http-https

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Cập nhật:** 25/05/2026\
> **Status:** ✅ Có bài — cụm `01_basic` đã hoàn chỉnh (6 bài)

## 🎯 Chủ đề này có gì

HTTP/HTTPS — giao thức nền của Web. Cụm bài cơ bản đi từ "HTTP là gì" → methods → status codes → headers → HTTPS/TLS → REST API design.

## 📖 Lessons — 01_basic

| # | Bài | Nội dung |
|---|---|---|
| 00 | [HTTP là gì](lessons/01_basic/00_what-is-http.md) | Request/response, stateless, versions 1.1/2/3, DevTools |
| 01 | [HTTP Methods](lessons/01_basic/01_http-methods.md) | GET/POST/PUT/PATCH/DELETE + idempotent + safe |
| 02 | [HTTP Status Codes](lessons/01_basic/02_http-status-codes.md) | 5 nhóm 1xx-5xx + 20 mã phổ biến |
| 03 | [HTTP Headers](lessons/01_basic/03_http-headers.md) | Content-Type, Auth, Cache, CORS |
| 04 | [HTTPS & TLS](lessons/01_basic/04_https-tls.md) | Cert, handshake, Let's Encrypt, HSTS |
| 05 | [REST API Concepts](lessons/01_basic/05_rest-api-concepts.md) | 6 constraints, resource design, versioning, REST vs GraphQL/gRPC |

## 🚀 Đọc folder này thế nào

| Nhu cầu | Đọc gì |
|---|---|
| Mới bắt đầu | `lessons/01_basic/00_what-is-http.md` rồi đi tuần tự 00 → 05 |
| Tra nhanh status code / header | `lessons/01_basic/02_http-status-codes.md`, `lessons/01_basic/03_http-headers.md` (có cheatsheet cuối bài) |
| Design API | `lessons/01_basic/01_http-methods.md` + `lessons/01_basic/05_rest-api-concepts.md` |
| Theo nghề | Xem [`../00_roadmaps/career/`](../../00_roadmaps/career/) chọn career path đi qua HTTP |

## 📂 Cấu trúc

```
http-https/
├── README.md                ← (file này) index + lộ trình đọc
├── lessons/01_basic/        ← 6 bài cơ bản (đã có)
├── exercises/               ← bài tập (chưa có)
├── recipes/                 ← công thức / troubleshooting (chưa có)
└── setup/                   ← cài đặt + cấu hình (chưa có)
```
