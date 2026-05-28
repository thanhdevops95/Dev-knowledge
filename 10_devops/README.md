# ⚙️ 10_devops — Platform Engineering & Lifecycle Automation

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 26/05/2026

> 🚀 **Status:** Đã hoàn thiện toàn bộ các cấu phần DevOps Core (Docker, Kubernetes, CI/CD, IaC, Observability) với đầy đủ lộ trình Basic & Intermediate. Các L2 khác đang được cập nhật dần.

---

## 🎯 Chủ đề này có gì

Thư mục **10_devops** là nơi đóng gói toàn bộ tri thức về cách tự động hóa vòng đời phần mềm (*Software Development Lifecycle - SDLC*), thiết lập hạ tầng tin cậy và xây dựng nền tảng phát triển ứng dụng hiện đại (*Platform Engineering*).

Mục tiêu cốt lõi: Giúp bạn đi từ việc chạy ứng dụng local thủ công đến việc đóng gói container, lập lịch cluster, tự động hóa quy trình CI/CD, kiểm soát hạ tầng bằng code (IaC), và giám sát vận hành toàn diện ở quy mô production.

---

## 📂 Danh sách các chủ đề con (L2)

| L2 Module | Trạng thái | Nội dung chính |
|---|---|---|
| 🐳 [`docker/`](./docker/) | 🚀 10 bài | Containerization: Setup + 4 bài Basic + 5 bài Intermediate (BuildKit, Security, Optimization, Registry). |
| ☸️ [`kubernetes/`](./kubernetes/) | 🚀 11 bài | Orchestration: 5 bài Basic + 5 bài Intermediate (Helm, Ingress, StatefulSet, Autoscaling) + 1 Complete Guide. |
| 🔄 [`ci-cd/`](./ci-cd/) | 🚀 10 bài | Automation Pipelines: 5 bài Basic (GitHub Actions, GitLab CI, Patterns) + 5 bài Intermediate (ArgoCD GitOps, Secret Management, Progressive Delivery). |
| 🏗️ [`iac/`](./iac/) | 🚀 10 bài | Infrastructure as Code: 5 bài Basic (Terraform core) + 5 bài Intermediate (Terragrunt, Atlantis, Advanced State, Alternatives). |
| 📊 [`observability/`](./observability/) | 🚀 10 bài | System Monitoring: 5 bài Basic (Prometheus, Loki, OTel basics) + 5 bài Intermediate (LogQL, OTel Instrumentation, SRE Practices). |
| ⚓ [`gitops/`](./gitops/) | 🚧 1 bài | GitOps Basics: Định nghĩa, mô hình Pull vs Push, 1 bài placeholder basic. |
| 🕸️ [`service-mesh/`](./service-mesh/) | ❌ Chưa có | Service-to-service communication: Quản lý traffic, bảo mật mTLS (Istio, Cilium Service Mesh) — dự kiến. |

> Chi tiết sitemap mở rộng → xem [`../_blueprint/01_sitemap-detail.md`](../_blueprint/01_sitemap-detail.md).

---

## 🚀 Hướng dẫn đọc và học tập

| Bạn là... | Lộ trình đọc đề xuất |
|---|---|
| 🟢 **Beginner (Chưa biết gì)** | Đọc `00_overview.md` trước để nắm bức tranh toàn cảnh. Sau đó bắt đầu học từ **Docker Basic** → **CI/CD Basic** → **IaC Basic** → **Kubernetes Basic** → **Observability Basic**. |
| 🟡 **Developer muốn làm quen vận hành** | Tập trung vào **Docker Basic/Intermediate** + **CI/CD Basic** để có khả năng tự deploy và viết pipeline tự động cho ứng dụng của mình. |
| 🟠 **SysAdmin / Ops chuyển hướng sang DevOps** | Skim nhanh các bài Basic. Tập trung tối đa vào phần **Intermediate** của **IaC**, **Kubernetes** và **Observability** để nắm các kiến thức thiết kế ở quy mô Production. |
| 🧭 **Học theo định hướng nghề nghiệp** | Truy cập thư mục [`../00_roadmaps/career/`](../00_roadmaps/career/) và chọn lộ trình mong muốn (ví dụ: DevOps Engineer, SRE, Platform Engineer) để được chỉ đường đi qua các bài học trong folder này một cách logic nhất. |

---

## 🤝 Hướng dẫn đóng góp bài viết

Nếu bạn muốn bổ sung nội dung hoặc sửa đổi bài viết trong thư mục này:
1. Đọc kỹ hướng dẫn chung tại [`../_blueprint/README.md`](../_blueprint/README.md).
2. Sử dụng các file template mẫu trong [`../_blueprint/templates/`](../_blueprint/templates/).
3. Tuân thủ văn phong chia sẻ, giải nghĩa và kể chuyện (Narrative style) tại [`../_blueprint/03_writing-style.md`](../_blueprint/03_writing-style.md).
4. Chạy lại script tự động hóa để đồng bộ hóa danh mục toàn kho:
   ```bash
   python3 _scripts/sync-catalog.py
   ```

---

## 📌 Changelog

- **v1.0.0 (26/05/2026)** — Đồng bộ hóa toàn bộ L2 core, cập nhật mục lục chi tiết chứa đầy đủ các lộ trình Basic và Intermediate.
- **v0.2.0 (16/05/2026)** — Bộ Docker basic hoàn chỉnh (5 bài) — L1 chính thức có content.
- **v0.1.0 (16/05/2026)** — Khởi tạo thư mục khung (skeleton).
