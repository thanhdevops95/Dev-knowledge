# 📦 Container Registry — Lưu trữ, phân phối & bảo mật container image

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 14/06/2026

> 🎯 *Container Registry là kho lưu trữ + phân phối container image (OCI). Đây là mắt xích nối giữa "build image" và "chạy image ở production": CI build → push lên registry → K8s/server pull về chạy. Chủ đề này dạy từ khái niệm + tag/digest, các registry phổ biến (Docker Hub, GHCR, ECR, GCR/Artifact Registry, ACR, Harbor), cho tới bảo mật supply chain (scan CVE + ký image) và vận hành registry ở quy mô lớn.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu registry là gì, giải phẫu tên image, chuẩn **OCI**, và vấn đề Docker Hub rate limit
- [x] Đặt tag đúng chuẩn + pin image **immutable bằng digest** `@sha256`; hiểu multi-arch manifest
- [x] Dùng **private registry**: Harbor (self-host), ECR/GCR/ACR/GHCR (cloud) + pull secret cho K8s
- [x] Bảo mật supply chain: **scan CVE** (Trivy), **ký image** (cosign/Sigstore), SBOM
- [x] Tích hợp registry vào **CI/CD**: cache, tag strategy, promotion, retention
- [x] (Intermediate) Vận hành Harbor sâu, **HA + replication + DR**, **policy admission** (cosign verify gate), tối ưu chi phí ở quy mô lớn

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic — Nền tảng Registry (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Container Registry là gì`](./lessons/01_basic/00_what-is-container-registry.md) | 🌱 Intro | ✅ | Registry là gì, giải phẫu tên image, public vs private, Docker Hub rate limit, landscape registry, chuẩn OCI. |
| **01** | [`Tags & Digests`](./lessons/01_basic/01_docker-hub-tags-and-digests.md) | 🌳 Lesson | ✅ | push/pull/tag, cạm bẫy `:latest`, pin immutable bằng digest `@sha256`, multi-arch manifest, tag strategy. |
| **02** | [`Private Registries`](./lessons/01_basic/02_private-registries.md) | 🌳 Lesson | ✅ | Harbor (self-host), ECR/Artifact Registry/ACR/GHCR (cloud), auth, `imagePullSecrets` cho Kubernetes. |
| **03** | [`Image Signing & Scanning`](./lessons/01_basic/03_image-signing-and-scanning.md) | 🌳 Lesson | ✅ | Trivy/Grype scan CVE, SBOM (syft), cosign/Sigstore ký + verify image, SLSA provenance cơ bản. |
| **04** | [`Registry trong CI/CD`](./lessons/01_basic/04_registry-in-cicd.md) | 🌳 Lesson | ✅ | Build cache qua registry, tag strategy CI, image promotion dev→prod, retention/cleanup, mirror/pull-through. |

### 📖 Lộ trình Intermediate — Quy mô Production (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Intermediate Overview`](./lessons/02_intermediate/00_intermediate-overview.md) | 🌱 Intro | 🚧 | Registry ở quy mô multi-team/production: HA, geo-replication, policy enforcement, supply-chain hardening, cost. |
| **01** | [`Harbor Deep Dive`](./lessons/02_intermediate/01_harbor-deep-dive.md) | 🌳 Lesson | 🚧 | Kiến trúc Harbor, project + RBAC + robot account, proxy cache (pull-through), retention/immutability/quota, webhook. |
| **02** | [`HA, Replication & DR`](./lessons/02_intermediate/02_high-availability-replication-and-dr.md) | 🌳 Lesson | 🚧 | Storage backend (S3/GCS), multi-replica, geo-replication, registry sau LB/CDN, backup + disaster recovery. |
| **03** | [`Policy & Admission Enforcement`](./lessons/02_intermediate/03_policy-and-admission-enforcement.md) | 🌳 Lesson | 🚧 | Cosign verify gate, Kyverno/OPA Gatekeeper admission (chỉ deploy image signed + scan-pass), SLSA, allowlist. |
| **04** | [`Optimization & Cost at Scale`](./lessons/02_intermediate/04_optimization-and-cost-at-scale.md) | 🌳 Lesson | 🚧 | Garbage collection sâu, chiến lược retention, layer dedup, tối ưu chi phí storage/egress, observability/audit. |

> 🚧 = đang biên soạn trong đợt hoàn thiện nhánh DevOps (06/2026).

---

## 🚀 Lộ trình đề xuất

- **Beginner:** Đọc [Bài 00](./lessons/01_basic/00_what-is-container-registry.md) để nắm khái niệm, rồi [Tags & Digests](./lessons/01_basic/01_docker-hub-tags-and-digests.md) để push image chuẩn. Khi cần kho riêng cho team → [Private Registries](./lessons/01_basic/02_private-registries.md); muốn an toàn supply chain → [Signing & Scanning](./lessons/01_basic/03_image-signing-and-scanning.md); tự động hoá → [Registry trong CI/CD](./lessons/01_basic/04_registry-in-cicd.md).
- **Intermediate:** Tự host registry production thì học [Harbor Deep Dive](./lessons/02_intermediate/01_harbor-deep-dive.md) + [HA/Replication/DR](./lessons/02_intermediate/02_high-availability-replication-and-dr.md); cần chặn image không an toàn vào cluster → [Policy & Admission](./lessons/02_intermediate/03_policy-and-admission-enforcement.md).

## 🔗 Liên kết cụm liên quan

- [Docker](../docker/) — build image (đặc biệt `02_image-security-supply-chain` bổ trợ scan/sign).
- [Kubernetes](../kubernetes/) — pull image qua `imagePullSecrets`, admission control verify chữ ký.
- [CI/CD](../ci-cd/) — pipeline build→scan→sign→push→deploy.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Khởi tạo README khung (skeleton).
- **v1.0.0 (14/06/2026)** — Hoàn thiện cụm **Basic 5/5** (registry concepts + tags/digests + private registries + signing/scanning + CI/CD). Bổ sung lộ trình Intermediate (đang biên soạn).
