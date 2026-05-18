# 📘 Glossary — Kubernetes Pod

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 15/05/2026

> 🎯 *Bảng thuật ngữ EN ↔ VN cho chủ đề Pod. Mỗi entry có giải thích ngắn và link tới bài giảng kỹ.*

| EN | VN | Giải thích | Bài chính |
|---|---|---|---|
| **Pod** | Pod (giữ nguyên) | Đơn vị deploy nhỏ nhất K8s, gồm 1+ container chia sẻ network và storage volume | [Pod basic](./lessons/01_basic/01_pod.md) |
| **Container** | Container (giữ nguyên) | Đơn vị runtime ứng dụng (Docker, containerd) | [Pod basic §1](./lessons/01_basic/01_pod.md#1️⃣-pod-là-gì) |
| **Namespace** | Không gian tên | Cô lập logic resource trong cluster | (sẽ có) |
| **Node** | Node | Máy worker chạy Pod (VM hoặc physical) | (sẽ có) |
| **Manifest** | File khai báo | YAML/JSON mô tả desired state của resource | [Pod basic §2](./lessons/01_basic/01_pod.md#2️⃣-hands-on--tạo-pod-đầu-tiên) |
| **Label** | Nhãn | Key-value gắn vào resource để filter/select | [Pod basic §2](./lessons/01_basic/01_pod.md#2️⃣-hands-on--tạo-pod-đầu-tiên) |
| **Selector** | Bộ chọn | Quy tắc match label, dùng bởi Service/Deployment | (sẽ có) |
| **Imperative** | Mệnh lệnh | "Ra lệnh trực tiếp" qua `kubectl run`, `kubectl create` | [Pod basic §2](./lessons/01_basic/01_pod.md#2️⃣-hands-on--tạo-pod-đầu-tiên) |
| **Declarative** | Khai báo | "Khai báo trạng thái mong muốn" qua YAML + `kubectl apply` | [Pod basic §2](./lessons/01_basic/01_pod.md#2️⃣-hands-on--tạo-pod-đầu-tiên) |
| **Lifecycle** | Vòng đời | Các phase Pod đi qua: Pending → Running → Succeeded/Failed | [Pod basic §3](./lessons/01_basic/01_pod.md#3️⃣-vòng-đời-pod-pod-lifecycle) |
| **CrashLoopBackOff** | (giữ nguyên) | Trạng thái Pod restart liên tục do container crash | [Pod basic — Pitfall](./lessons/01_basic/01_pod.md#-pitfall--best-practice) |
| **Pending** | Chờ | Phase Pod chưa được schedule lên Node hoặc đang pull image | [Pod basic §3](./lessons/01_basic/01_pod.md#3️⃣-vòng-đời-pod-pod-lifecycle) |
| **Running** | Đang chạy | Phase Pod đã có container chạy thật | [Pod basic §3](./lessons/01_basic/01_pod.md#3️⃣-vòng-đời-pod-pod-lifecycle) |
| **Sidecar pattern** | (giữ nguyên) | Pattern: thêm container phụ chạy cùng main container (vd log forwarder) | [Pod overview §3](./00_overview.md#3️⃣-khi-nào-dùng-multi-container-pod) |
| **Init container** | Container khởi tạo | Container chạy 1 lần để chuẩn bị data, exit rồi main container mới start | [Pod overview §3](./00_overview.md#3️⃣-khi-nào-dùng-multi-container-pod) |
| **kubectl** | (giữ nguyên) | CLI tool để tương tác với K8s API | [Pod basic §2](./lessons/01_basic/01_pod.md#2️⃣-hands-on--tạo-pod-đầu-tiên) |
| **Scheduler** | Bộ điều phối | Component của K8s control plane, chọn Node cho Pod | [Pod basic §3](./lessons/01_basic/01_pod.md#3️⃣-vòng-đời-pod-pod-lifecycle) |

---

## 📌 Changelog

- **v1.0.0 (15/05/2026)** — Bản đầu tiên — mẫu cho Blueprint.
