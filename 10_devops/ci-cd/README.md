# 🔄 CI/CD — Continuous Integration & Continuous Deployment

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 26/05/2026

> 🎯 *CI/CD là trái tim của văn hóa DevOps. Nó tự động hóa quy trình Tích hợp liên tục (CI - kiểm thử, build) và Triển khai liên tục (CD - đưa sản phẩm lên môi trường thật) để rút ngắn chu kỳ phát hành phần mềm và giảm thiểu lỗi thủ công.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu rõ bản chất triết lý CI/CD, các chỉ số đo lường hiệu năng giao hàng (DORA Metrics)
- [x] Thiết lập thành thạo workflow tự động kiểm thử và đóng gói Docker trên **GitHub Actions**
- [x] Làm chủ công cụ **GitLab CI** từ khai báo runner, caching đến quản lý artifacts
- [x] Áp dụng các mô hình phát triển phần mềm (Trunk-based vs Gitflow) tương thích với pipeline
- [x] Nắm vững các chiến lược release: Recreate, Rolling, Blue-Green, Canary và Feature Flags
- [x] Chuyển đổi mô hình Push sang Pull-based GitOps sử dụng **ArgoCD** chạy trong Kubernetes
- [x] Bảo mật chuỗi cung ứng phần mềm thông qua tiêu chuẩn **SLSA Level 3** và Kyverno
- [x] Thiết lập quản lý bí mật (Secrets) nâng cao với HashiCorp Vault và External Secrets Operator

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic — Cơ bản về Pipeline (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`What is CI/CD`](./lessons/01_basic/00_what-is-cicd.md) | 🌱 Intro | ✅ 🌟 | Khái niệm CI/CD, bối cảnh lịch sử, so sánh các công cụ (GitHub Actions, GitLab, Jenkins) và DORA metrics. |
| **01** | [`GitHub Actions`](./lessons/01_basic/01_github-actions.md) | 🌳 Lesson | ✅ 🌟 | Làm chủ workflow YAML, events, jobs/steps, matrix builds, secrets & OIDC, caching và reusable workflows. |
| **02** | [`GitLab CI`](./lessons/01_basic/02_gitlab-ci.md) | 🌳 Lesson | ✅ 🌟 | Làm chủ cấu trúc `.gitlab-ci.yml`, runners, rules/only/except, services (DB container) và environments. |
| **03** | [`Pipeline Patterns`](./lessons/01_basic/03_pipeline-patterns.md) | 🌳 Lesson | ✅ 🌟 | Các pattern phổ biến: PR validation, Monorepo build, Dependency updates, quét lỗ hổng mã nguồn. |
| **04** | [`Deploy Strategies`](./lessons/01_basic/04_deploy-strategies.md) | 🌳 Lesson | ✅ 🌟 | So sánh chi tiết 5 chiến lược triển khai (Recreate, Rolling, Blue-Green, Canary, Feature flags). |

### 📖 Lộ trình Intermediate — Quy trình chuyên sâu Production (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Intermediate Overview`](./lessons/02_intermediate/00_intermediate-overview.md) | 🌱 Intro | ✅ 🌟 | Tổng quan về các trụ cột nâng cao khi vận hành pipeline cho doanh nghiệp lớn (GitOps, Security, Secrets). |
| **01** | [`GitOps with ArgoCD`](./lessons/02_intermediate/01_gitops-with-argocd.md) | 🌳 Lesson | ✅ 🌟 | Khắc phục nhược điểm của mô hình Push. Setup ArgoCD, ApplicationSet, xử lý drift và đồng bộ tự động. |
| **02** | [`Supply Chain Security`](./lessons/02_intermediate/02_supply-chain-security.md) | 🌳 Lesson | ✅ 🌟 | Đạt chuẩn SLSA Level 3, tạo chữ ký số cho pipeline bằng Cosign, verify kiểm duyệt trước khi chạy trên cluster. |
| **03** | [`Secret Management`](./lessons/02_intermediate/03_secret-management.md) | 🌳 Lesson | ✅ 🌟 | Tích hợp HashiCorp Vault, External Secrets Operator, SOPS và Sealed Secrets để mã hóa cấu hình nhạy cảm. |
| **04** | [`Progressive Delivery`](./lessons/02_intermediate/04_progressive-delivery.md) | 🌳 Lesson | ✅ 🌟 | Triển khai an toàn với Argo Rollouts, tự động phân tích metrics Prometheus để quyết định rollback/promote. |

---

## 🚀 Lộ trình đề xuất

*   **Beginner:** Đi từ [Bài 00](./lessons/01_basic/00_what-is-cicd.md) để hiểu tư duy, sau đó chọn thực hành sâu trên **GitHub Actions (Bài 01)** (dễ bắt đầu nhất) hoặc **GitLab CI (Bài 02)** tùy vào dự án hiện tại của bạn.
*   **Intermediate:** Khi đã nắm được cách build/deploy cơ bản, bắt buộc phải học **GitOps (Bài 01)** và **Secret Management (Bài 03)** để hiểu cách tổ chức luồng triển khai thực tế của các doanh nghiệp hiện nay.

---

## 💡 Tài nguyên tham khảo

*   **ArgoCD:** Công cụ GitOps hàng đầu chạy trên Kubernetes.
*   **SLSA (Supply-chain Levels for Software Artifacts):** Khung tiêu chuẩn bảo mật cho việc build và đóng gói phần mềm.
*   **HashiCorp Vault:** Giải pháp quản lý thông tin bảo mật tập trung cho toàn hệ thống.

---

## 📌 Changelog

- **v1.0.0 (26/05/2026)** — Cập nhật mục lục hoàn chỉnh kết nối toàn bộ lộ trình học CI/CD từ Basic đến các kỹ thuật GitOps & Security Intermediate.
- **v0.1.0 (20/05/2026)** — Khởi tạo file README khung (skeleton).
