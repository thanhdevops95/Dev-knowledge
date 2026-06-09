# ⚡ Serverless

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 01/06/2026\
> **Trạng thái:** ✅ Basic cluster hoàn chỉnh (5/5 bài)

> 🎯 *Serverless — vendor-neutral concept cluster. So sánh AWS Lambda + GCP Cloud Functions/Run + Azure Functions + Cloudflare Workers. FaaS architecture, event-driven patterns, anti-patterns, cost + cold start + observability.*

---

## 🚀 Quick start

- [00_what-is-serverless-overview](lessons/01_basic/00_what-is-serverless-overview.md)
- [01_function-as-a-service-deep](lessons/01_basic/01_function-as-a-service-deep.md)
- [02_event-driven-and-triggers](lessons/01_basic/02_event-driven-and-triggers.md)
- [03_serverless-patterns-and-anti-patterns](lessons/01_basic/03_serverless-patterns-and-anti-patterns.md)
- [04_serverless-cost-cold-start-and-observability](lessons/01_basic/04_serverless-cost-cold-start-and-observability.md)

---

## 📖 Lessons — Basic cluster (5 bài)

| # | Bài | Trọng tâm |
|---|---|---|
| 00 | [Serverless overview](lessons/01_basic/00_what-is-serverless-overview.md) | 4 vendor compare + anti-pattern |
| 01 | [FaaS deep](lessons/01_basic/01_function-as-a-service-deep.md) | Cold start + isolate vs container + concurrency |
| 02 | [Event-driven + triggers](lessons/01_basic/02_event-driven-and-triggers.md) | HTTP/queue/storage/cron + DLQ + idempotency |
| 03 | [Patterns + anti-patterns](lessons/01_basic/03_serverless-patterns-and-anti-patterns.md) | API/file/ETL/cron/saga + 6 anti-pattern |
| 04 | [Cost + cold start + observability](lessons/01_basic/04_serverless-cost-cold-start-and-observability.md) | Pricing 4 vendor + break-even + hidden cost (NAT/egress/log) + cold start mitigation + 3 pillars observability + hands-on audit bill |


---

## 🔗 Liên kết & Tài nguyên

### 🧭 Định hướng lộ trình học

- ⬅️ **Bài trước:** [11_cloud](../README.md)
- ↑ **Về cụm:** [☁️ 11_cloud — Tổng quan cụm Cloud](../README.md)
- ➡️ **Bài tiếp theo:** [Serverless là gì — Bức tranh tổng thể & 4 nhà cung cấp lớn](lessons/01_basic/00_what-is-serverless-overview.md)

### 🧩 Các chủ đề có thể bạn quan tâm

- ☁️ **Triển khai trên AWS:** [Lambda + API Gateway — Nhập môn Serverless](../aws/lessons/01_basic/04_lambda-and-api-gateway.md)
- ☁️ **Triển khai trên GCP:** [GCP Cloud Functions + Cloud Run + API Gateway](../gcp/lessons/01_basic/04_cloud-functions-cloud-run-and-api-gateway.md)
- ☁️ **Triển khai trên Azure:** [Azure Functions + App Service + Container Apps](../azure/lessons/01_basic/04_functions-and-app-service.md)
- ☁️ **Edge compute:** [Cloudflare Workers + Pages — Edge compute & static + dynamic](../cloudflare/lessons/01_basic/02_workers-and-pages.md)
- 💰 **Quản lý chi phí:** [Cloud Cost Management (FinOps)](../cloud-cost-management/README.md)

### 🌐 Tài nguyên tham khảo khác

- 📖 [Serverless Framework](https://www.serverless.com/) — framework triển khai serverless đa vendor.
- 📖 [SST (Serverless Stack)](https://sst.dev/) — bộ công cụ build app serverless trên AWS.
- 📖 [Knative](https://knative.dev/) — nền tảng serverless mã nguồn mở chạy trên Kubernetes.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Skeleton ban đầu.
- **v1.0.0 (24/05/2026)** — Basic cluster hoàn chỉnh 5/5 bài. Vendor-neutral concept cluster.
- **v1.1.0 (01/06/2026)** — Bỏ cột "Thời lượng" và tổng "~103 phút đọc" (ước tính không chuẩn); sửa mô tả bài 04 cho khớp nội dung thực (bỏ "6-layer guardrail/30-item checklist" sai, thay bằng break-even + hidden cost + 3 pillars observability + hands-on audit); chuẩn hoá mục Liên kết & Tài nguyên theo khung 3 sub (Định hướng/Chủ đề liên quan/Tài nguyên khác) với marker ⬅️/➡️/↑ và link-text = tiêu đề H1 thực; đổi field "Status" → "Trạng thái".
