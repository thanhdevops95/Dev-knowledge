# 🕸️ Service Mesh — Giao tiếp & bảo mật microservice

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** 20/05/2026\
> **Cập nhật:** 14/06/2026

> 🎯 *Service Mesh là tầng hạ tầng chuyên xử lý giao tiếp service-to-service giữa các microservice — mã hoá (mTLS), định tuyến (canary/retry/circuit-breaking) và quan sát — mà KHÔNG cần sửa code ứng dụng. Cách làm: tiêm một proxy (sidecar Envoy) cạnh mỗi pod, điều khiển tập trung bởi control plane. Chủ đề này dạy từ khái niệm + sidecar, traffic management, mTLS/authz, cho tới so sánh Istio/Linkerd/Cilium và vận hành production (multi-cluster, Kiali, ambient mesh).*

---

## 🎯 Mục tiêu tổng

Sau khi đi qua chủ đề này, bạn sẽ:
- [x] Hiểu service mesh giải bài toán gì, **sidecar pattern**, **control plane vs data plane**
- [x] Nắm kiến trúc Istio (istiod + Envoy), sidecar injection, và mô hình **ambient** (sidecarless)
- [x] Quản lý traffic: routing, **canary**, retry/timeout, **circuit breaking**, fault injection
- [x] Bật **mTLS tự động** + **AuthorizationPolicy** (zero-trust) giữa các service
- [x] So sánh **Istio / Linkerd / Consul / Cilium** và chọn đúng cho nhu cầu
- [x] (Intermediate) Resilience nâng cao, **multi-cluster mesh**, observability với **Kiali** + tracing, **ambient mesh** + vận hành production

---

## 📂 Cấu trúc Chương trình học

### 📖 Lộ trình Basic — Nền tảng Service Mesh (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Service Mesh là gì`](./lessons/01_basic/00_what-is-service-mesh.md) | 🌱 Intro | ✅ | Bài toán giao tiếp microservice, sidecar pattern, control vs data plane, sidecar vs ambient/eBPF, khi nào cần. |
| **01** | [`Kiến trúc & Sidecar`](./lessons/01_basic/01_architecture-and-sidecar.md) | 🌳 Lesson | ✅ | Data plane (Envoy), control plane (istiod + xDS), sidecar injection, traffic intercept, ambient mode (ztunnel/waypoint). |
| **02** | [`Traffic Management`](./lessons/01_basic/02_traffic-management.md) | 🌳 Lesson | ✅ | VirtualService + DestinationRule, canary theo weight, retry/timeout, circuit breaking (outlier), fault injection, mirroring. |
| **03** | [`Security — mTLS & Authz`](./lessons/01_basic/03_security-mtls-and-authz.md) | 🌳 Lesson | ✅ | mTLS tự động, identity SPIFFE, PeerAuthentication STRICT, AuthorizationPolicy, JWT (RequestAuthentication), zero-trust. |
| **04** | [`Istio vs Linkerd vs Cilium`](./lessons/01_basic/04_istio-vs-linkerd-vs-cilium.md) | 🌳 Lesson | ✅ | So sánh Istio/Linkerd/Consul/Cilium, sidecar vs ambient vs eBPF, overhead, learning curve, chọn cái nào. |

### 📖 Lộ trình Intermediate — Vận hành Production (5 bài)

| # | Bài học | Loại | Trạng thái | Nội dung chính |
|---|---|---|---|---|
| **00** | [`Intermediate Overview`](./lessons/02_intermediate/00_intermediate-overview.md) | 🌱 Intro | ✅ | Vận hành mesh production: resilience nâng cao, multi-cluster, observability sâu, ambient + nâng cấp control plane. |
| **01** | [`Advanced Traffic & Resilience`](./lessons/02_intermediate/01_advanced-traffic-and-resilience.md) | 🌳 Lesson | ✅ | Locality-aware LB, retry budget, rate limiting, egress/ServiceEntry, fault injection sâu, traffic shifting an toàn. |
| **02** | [`Multi-Cluster Mesh`](./lessons/02_intermediate/02_multi-cluster-mesh.md) | 🌳 Lesson | ✅ | Multi-primary vs primary-remote, cross-cluster service discovery, east-west gateway, trust domain. |
| **03** | [`Observability — Kiali & Tracing`](./lessons/02_intermediate/03_observability-kiali-and-tracing.md) | 🌳 Lesson | ✅ | Kiali topology, metrics Prometheus, distributed tracing (Jaeger/Tempo), access log, golden signals của mesh. |
| **04** | [`Ambient Mesh & Production Ops`](./lessons/02_intermediate/04_ambient-mesh-and-production-ops.md) | 🌳 Lesson | ✅ | Istio ambient (ztunnel + waypoint), nâng cấp/canary control plane, tuning hiệu năng sidecar, khi nào sidecarless. |

> ✅ Cụm hoàn chỉnh Basic 5/5 + Intermediate 5/5 (đợt hoàn thiện nhánh DevOps, 06/2026).

---

## 🚀 Lộ trình đề xuất

- **Beginner:** Đọc [Bài 00](./lessons/01_basic/00_what-is-service-mesh.md) để hiểu vì sao cần mesh, rồi [Kiến trúc & Sidecar](./lessons/01_basic/01_architecture-and-sidecar.md). Thực hành [Traffic Management](./lessons/01_basic/02_traffic-management.md) (canary) + [mTLS & Authz](./lessons/01_basic/03_security-mtls-and-authz.md) trên cluster demo. Cuối cùng [so sánh giải pháp](./lessons/01_basic/04_istio-vs-linkerd-vs-cilium.md) để chọn cho dự án.
- **Intermediate:** Khi chạy mesh production, tối ưu resilience + observability với [Kiali & Tracing](./lessons/02_intermediate/03_observability-kiali-and-tracing.md); mở rộng nhiều cluster với [Multi-Cluster Mesh](./lessons/02_intermediate/02_multi-cluster-mesh.md); giảm overhead với [Ambient Mesh](./lessons/02_intermediate/04_ambient-mesh-and-production-ops.md).

## 🔗 Liên kết cụm liên quan

- [Kubernetes](../kubernetes/) — service mesh chạy trên K8s; bổ trợ Service/Ingress + mTLS/cert.
- [Observability](../observability/) — mesh sinh sẵn metrics/traces; Kiali + Prometheus + Jaeger.
- [CI/CD](../ci-cd/) — progressive delivery (canary/blue-green) thường phối hợp với mesh routing.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v0.1.0 (20/05/2026)** — Khởi tạo file README khung (skeleton).
- **v0.2.0 (26/05/2026)** — Cải tiến mô tả dự kiến lộ trình.
- **v1.0.0 (14/06/2026)** — Hoàn thiện cụm **Basic 5/5** (concept + kiến trúc/sidecar + traffic management + mTLS/authz + so sánh giải pháp). Bổ sung lộ trình Intermediate (đang biên soạn).
- **v1.1.0 (14/06/2026)** — Hoàn thiện cụm **Intermediate 5/5** (overview + advanced traffic/resilience + multi-cluster + observability Kiali/tracing + ambient mesh/production ops). Cụm service-mesh hoàn chỉnh.
