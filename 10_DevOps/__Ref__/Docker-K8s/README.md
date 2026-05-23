# Docker → Kubernetes — Chuỗi 69 bài thực hành thủ công

> **Author:** Mr.Rom\
> **Version:** v2.0.0\
> **App xuyên suốt:** `myapp` Python → Flask → Redis → K8s → Helm/ArgoCD/Istio → Production-grade stack

## Cách học

- Mỗi bài là **1 thư mục riêng** trong `Docker/`, `K8s/`, hoặc `Advanced/`.
- Trong thư mục có: source code (`myapp/` hoặc các YAML), `README.md` chứa **lệnh thủ công** copy-paste, và `KET-QUA.md` lưu output thật khi bạn chạy.
- **Cách chuyển bài:** `cp -r XX-name (XX+1)-next` → đổi tên folder → sửa file theo đề bài kế.
- **Không dùng script `.sh`** — chép từng lệnh vào terminal để hiểu sâu.

## Lộ trình

| Phần | Thư mục | Bài | Index |
|------|---------|-----|-------|
| **Docker** | [`Docker/`](Docker/) | 01-24 (core) + 51-55 (bonus) | [Docker/README.md](Docker/README.md) |
| **Kubernetes** | [`K8s/`](K8s/) | 25-41 (core) + 56-64 (bonus) | [K8s/README.md](K8s/README.md) |
| **Chuyên sâu** | [`Advanced/`](Advanced/) | 42-50 (core) + 65-69 (bonus) | [Advanced/README.md](Advanced/README.md) |

### 🔴 Phần Bonus — Production-grade (Bài 51-69)

19 bài bổ sung từ v2.0.0, **bắt buộc nếu mục tiêu là production**:

| Nhóm | Bài | Chủ đề |
|------|-----|--------|
| Docker | 51-55 | `.dockerignore` + USER + HEALTHCHECK, Restart & Limits, ENTRYPOINT/CMD + Signal, Image Scanning, Buildx multi-arch |
| K8s | 56-64 | Job/CronJob, DaemonSet, Init/Sidecar, RBAC, NetworkPolicy, Affinity/Taints, Quota/PDB, StorageClass, Kustomize |
| Advanced | 65-69 | cert-manager, Prometheus+Grafana, Velero, External/Sealed Secrets, Operator+CRD |

## Quy ước

| Token | Ý nghĩa |
|-------|---------|
| `<YOUR_DOCKERHUB_USERNAME>` | Username Docker Hub của bạn — thay TRƯỚC khi `apply` YAML |
| `<YOUR_GITHUB_USERNAME>` | Username GitHub (Bài 45-47) |
| `myapp-dev` | Namespace mặc định K8s từ Bài 27 |
| `myapp:6.0` | Image cuối của phần Docker, dùng xuyên suốt K8s/Advanced |

## Bắt đầu

→ [Docker/01-pull-image/](Docker/01-pull-image/)

## Tài liệu tham chiếu (đọc theo thứ tự ưu tiên)

| # | File | Khi nào đọc |
|---|------|-------------|
| 1 | 🗺️ [`LEARNING-PATH.md`](LEARNING-PATH.md) | **Đọc trước** để chọn track A (tuyến tính) hoặc B (production-first) |
| 2 | [`docker-k8s-practice.md`](docker-k8s-practice.md) | Đề master 69 bài, mermaid + chú thích (v2.0.1) |
| 3 | 🧠 [`MINIKUBE-LOCAL-TIPS.md`](MINIKUBE-LOCAL-TIPS.md) | Khi gặp lỗi runtime trên macOS local (20 gotcha) |
| 4 | [`LAB-RUN-LOG.md`](LAB-RUN-LOG.md) | Tham khảo 63/69 bài đã verify thực tế + 17 lỗi đã fix |
| 5 | [`DOCUMENT-AUDIT.md`](DOCUMENT-AUDIT.md) | Lịch sử rà soát chất lượng tài liệu |

Phiên bản đề rút gọn: [`Docker/docker-practice.md`](Docker/docker-practice.md), [`K8s/kubernetes-practice.md`](K8s/kubernetes-practice.md), [`Advanced/advanced-practice.md`](Advanced/advanced-practice.md)

> **Khuyến nghị học:** đọc [`LEARNING-PATH.md`](LEARNING-PATH.md) đầu tiên. Đề có 4 bài tổng hợp (41, 44, 46, 50) reference forward sang Bonus → Learning Path giúp bạn biết khi nào cần nhảy đọc Bonus.

## Changelog

- **v2.0.1 (18/05/2026)** — Lab-run verification: chạy thật 68/69 bài trên Docker 29.4 + Minikube 1.38 (Calico CNI + 6GB RAM). Fix thêm 15 lỗi tài liệu phát hiện từ runtime. Tạo [`MINIKUBE-LOCAL-TIPS.md`](MINIKUBE-LOCAL-TIPS.md) với 20 mẹo cho local lab.
- **v2.0.0 (18/05/2026)** — Thêm 19 bài Bonus production-grade (Bài 51-69), fix 9 lỗi kỹ thuật ở các bài cũ, thêm 13 mermaid diagrams + chú thích chi tiết cho học viên.
- **v1.0.0 (14/05/2026)** — Phát hành 50 bài đầu tiên, chia 3 phần Docker/K8s/Advanced.
