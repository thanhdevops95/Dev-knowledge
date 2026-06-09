# ☸️ Kubernetes — Container Orchestration Platform

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 26/05/2026

> 🎯 *Kubernetes (K8s) là chuẩn công nghiệp về điều phối container ở quy mô lớn. Nó tự động hóa việc triển khai, mở rộng, phục hồi và quản lý hàng ngàn container trên cụm máy chủ.*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu kiến trúc Cluster (Control Plane vs Worker Nodes) và triết lý Declarative của K8s
- [x] Làm chủ các tài nguyên tính toán cơ bản: Pods, Deployments và cơ chế tự phục hồi (self-healing)
- [x] Định tuyến mạng hiệu quả giữa các service bên trong cluster (ClusterIP, NodePort, LoadBalancer)
- [x] Phân tách cấu hình và bảo mật thông tin nhạy cảm sử dụng ConfigMap và Secret
- [x] Thiết lập môi trường chạy đa người dùng (multi-tenancy) an toàn qua Namespaces và RBAC
- [x] Đóng gói và phiên bản hóa ứng dụng K8s dưới dạng các gói Helm Charts
- [x] Triển khai Ingress Controller, Cert-Manager tự động hóa TLS Let's Encrypt
- [x] Quản lý lưu trữ trạng thái (Stateful Workloads) với StatefulSet, PV, PVC
- [x] Thiết lập hệ thống tự động co giãn tài nguyên linh hoạt (HPA, VPA, KEDA, Cluster Autoscaler)

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic — Cụm Cluster Cơ bản (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`What is Kubernetes`](./lessons/01_basic/00_what-is-kubernetes.md) | 🌱 Intro | ✅ 🌟 | K8s là gì, so sánh vs Docker Compose, kiến trúc Control Plane/Nodes, distro local (Minikube/Kind). |
| **01** | [`Pods & Deployments`](./lessons/01_basic/01_pods-and-deployments.md) | 🌳 Lesson | ✅ 🌟 | Quản lý Pod (đơn vị nhỏ nhất), Deployment, labels/selectors, rolling update, liveness/readiness probes. |
| **02** | [`Services & Networking`](./lessons/01_basic/02_services-and-networking.md) | 🌳 Lesson | ✅ 🌟 | 4 loại Service (ClusterIP, NodePort, LoadBalancer, ExternalName), DNS nội bộ, Ingress basics. |
| **03** | [`ConfigMaps & Secrets`](./lessons/01_basic/03_configmaps-and-secrets.md) | 🌳 Lesson | ✅ 🌟 | Quản lý cấu hình với ConfigMap & Secret, inject bằng Env/File mount, tích hợp External Secrets. |
| **04** | [`Namespaces & RBAC`](./lessons/01_basic/04_namespaces-and-rbac.md) | 🌳 Lesson | ✅ 🌟 | Phân chia môi trường bằng Namespaces, thiết lập quyền hạn chi tiết với RBAC (Role, Bindings, ServiceAccount). |

### 📖 Lộ trình Intermediate — Chuyên sâu Production (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Intermediate Overview`](./lessons/02_intermediate/00_intermediate-overview.md) | 🌱 Intro | ✅ 🌟 | Bức tranh tổng thể về các thách thức vận hành Kubernetes trên môi trường Production thực tế. |
| **01** | [`Helm Package Manager`](./lessons/02_intermediate/01_helm-package-manager.md) | 🌳 Lesson | ✅ 🌟 | Templating hóa các manifest K8s với Helm, cấu trúc Chart, values, hooks và quản lý release. |
| **02** | [`Ingress, Cert-Manager & TLS`](./lessons/02_intermediate/02_ingress-cert-manager-tls.md) | 🌳 Lesson | ✅ 🌟 | Setup Ingress-Nginx production, tự động hóa cấp phát chứng chỉ SSL/TLS bằng Cert-Manager. |
| **03** | [`StatefulSet & Storage`](./lessons/02_intermediate/03_statefulset-and-storage.md) | 🌳 Lesson | ✅ 🌟 | Triển khai Stateful apps (Database) với StatefulSet, cơ chế StorageClass, PV/PVC và sao lưu dữ liệu. |
| **04** | [`Autoscaling & Operators`](./lessons/02_intermediate/04_autoscaling-and-operators.md) | 🌳 Lesson | ✅ 🌟 | Tự động co giãn (HPA, VPA, Cluster Autoscaler), mở rộng Kubernetes với CRD và Custom Operators. |

### 📚 Hướng dẫn & Tài liệu đính kèm
*   ✅ [`00_kubernetes-complete-guide.md`](./00_kubernetes-complete-guide.md) — Sách hướng dẫn toàn diện (Complete Reference Guide) dành cho việc tra cứu nhanh cú pháp và kiến trúc Kubernetes.

---

## 🚀 Lộ trình đề xuất

*   **Bước 1:** Bắt đầu bằng việc nắm chắc toàn bộ **Lộ trình Basic (00 - 04)** để xây dựng được nền móng vững chắc.
*   **Bước 2:** Thực hành deploy một ứng dụng web (FastAPI/NodeJS) có kết nối Database PostgreSQL trên cluster local Minikube sử dụng các kiến thức basic.
*   **Bước 3:** Chuyển sang cụm bài **Lộ trình Intermediate (00 - 04)** để nâng cấp hệ thống lên mức chuẩn Production (đóng gói Helm, chạy HTTPS, cấu hình auto-scaling).

---

## 💡 Tài nguyên & Công cụ khuyên dùng

*   **Minikube / Kind:** Cụm Kubernetes ảo gọn nhẹ chạy ngay trên Docker local để thực hành học tập.
*   **Lens / K9s:** Giao diện đồ họa (Lens) hoặc terminal UI (K9s) giúp quản lý và xem logs, shell vào Pods cực kỳ trực quan.
*   **Kube-Prometheus-Stack:** Helm Chart chuẩn để cài đặt nhanh cụm Prometheus & Grafana giám sát toàn bộ cluster.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Khởi tạo file README khung (skeleton).
- **v1.0.0 (26/05/2026)** — Biên soạn hoàn chỉnh mục lục chi tiết cho module Kubernetes, kết nối đầy đủ các bài học Basic & Intermediate hiện có.
