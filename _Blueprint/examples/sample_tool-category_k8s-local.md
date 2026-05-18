# 🛠️ K8s local — Chọn cluster để học/dev trên máy mình

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 19/05/2026\
> **Cập nhật:** 19/05/2026\
> **Loại:** Tool category — tham khảo + so sánh\
> **Đọc trước:** [K8s là gì](../../10_DevOps/kubernetes/lessons/01_basic/00_what-is-k8s.md)

> 🎯 *Production K8s chạy hàng chục server. Để học/dev trên 1 laptop, ta cần "K8s thu nhỏ" gói gọn trong máy mình. File này giúp bạn so sánh 3 lựa chọn phổ biến và pick đúng cho nhu cầu.*

---

## Tình huống

Bạn vừa học K8s, muốn `kubectl apply` thử YAML mà chưa muốn:
- Đăng ký AWS EKS (tốn tiền, scary bill)
- Mua server riêng (overkill)
- Xin quyền cluster công ty (chậm, bị giới hạn)

Bạn cần 1 cluster K8s **chạy ngay trên laptop**, **free**, **bật trong 1 phút**.

Trên thị trường hiện có 3 lựa chọn chính: **Minikube**, **Kind**, **k3d**. Tất cả đều free + open source, nhưng triết lý + use case khác nhau.

---

## Nhanh — 3 dòng quyết định

| Bạn là... | Pick |
|---|---|
| Beginner, mới học K8s, muốn UI/addon đầy đủ | **Minikube** ⭐ |
| Đã quen Docker, viết CI test trên K8s | **Kind** |
| Cần lightweight, IoT/edge, raspberry pi | **k3d** |

> 💡 Không chắc → cứ Minikube. Stable nhất cho beginner.

---

## 📊 Bảng so sánh đầy đủ

| Tiêu chí | Minikube | Kind | k3d |
|---|---|---|---|
| **Tuổi** | 2016 (lâu, ổn) | 2018 | 2019 |
| **Backend** | VM (VirtualBox/HyperKit/Docker) | Docker container | Docker container (k3s) |
| **Đa node?** | ✅ Có (chậm) | ✅ Có (nhanh) | ✅ Có (nhanh nhất) |
| **Tốc độ khởi tạo** | ~60-90s | ~30-50s | ~15-25s |
| **RAM tối thiểu** | 2GB | 2GB | 512MB |
| **Addon built-in** | ⭐ Nhiều (Dashboard, Ingress, Registry, GPU) | Ít | Ít |
| **GUI?** | Có Dashboard built-in | Không | Không |
| **CI/CD friendly?** | OK (nhưng chậm) | ⭐ Tốt nhất | Tốt |
| **Multi-OS** | Mac/Linux/Win | Mac/Linux/Win | Mac/Linux/Win |
| **Tích hợp ARM (M1/M2/M3)?** | ✅ | ✅ | ✅ |
| **K8s version có thể chọn?** | ✅ | ✅ | ✅ (k3s flavor) |
| **Tài liệu** | ⭐ Phong phú nhất | Tốt | Khá |
| **Sponsorship** | CNCF / Google | Kubernetes SIG | Rancher (SUSE) |

---

## 🎯 Khuyến nghị theo case

### Case 1 — Beginner học K8s lần đầu

→ **Minikube**

Lý do:
- Dashboard built-in (`minikube dashboard`) — UI đẹp, dễ thấy Pod/Service trực quan
- Addon `ingress`, `metrics-server`, `registry` bật bằng 1 lệnh: `minikube addons enable ingress`
- Tài liệu Vietnamese + English nhiều nhất
- Cộng đồng Stack Overflow trả lời nhanh

Nhược: chậm khởi tạo (60-90s), tốn RAM hơn Kind.

### Case 2 — Viết CI test K8s

→ **Kind** (Kubernetes IN Docker)

Lý do:
- Chạy K8s thành Docker container — CI runner (GitHub Actions, GitLab CI) đã có Docker rồi, bật Kind là xong
- Cluster lên 30s — đủ chạy 1 batch test rồi tear down
- Multi-node giả lập production tốt (3 control plane + 3 worker)

Nhược: thiếu Dashboard và addon — không thân thiện cho beginner.

### Case 3 — Raspberry Pi / IoT / edge

→ **k3d** (wrapper của k3s)

Lý do:
- k3s là phiên bản K8s tối giản — bỏ bớt cloud controller, alpha features
- RAM ~512MB là chạy được
- Lightweight nhất cho hardware yếu

Nhược: thiếu vài feature mainstream (vd PodSecurityPolicy) — không dùng cho production lớn.

---

## 🧭 Đi vào từng tool

Sau khi pick được, đọc tool guide chi tiết:

| Tool | User guide |
|---|---|
| Minikube | [📄 minikube.md](./minikube.md) — cài + UI tour + addon + troubleshoot |
| Kind | [📄 kind.md](./kind.md) (chưa có — viết sau) |
| k3d | [📄 k3d.md](./k3d.md) (chưa có — viết sau) |

> 💡 Mỗi tool guide chỉ tập trung **chính nó** — không so sánh nữa. So sánh đã ở file này.

---

## 🌟 Alternative khác (ít phổ biến hơn nhưng đáng biết)

| Tool | Đặc biệt khi |
|---|---|
| **Docker Desktop K8s** | Đã cài Docker Desktop → tick 1 ô là có K8s. Nhược: lock vào 1 version, không multi-node |
| **MicroK8s** | Canonical (Ubuntu) — snap-based, đơn giản trên Ubuntu |
| **Rancher Desktop** | Rancher Labs — GUI mạnh, multi-engine (k3s/containerd) |
| **Colima** | Mac M1 thay thế Docker Desktop + có K8s built-in |
| **OrbStack** | Mac-only, FAST, paid |

---

## 💸 So sánh chi phí

Cả 5 tool ở trên đều **free + open source**. Khác với cloud K8s (EKS/GKE/AKS) tốn $73-150/cluster/tháng base + node fee.

→ Học K8s ở local **không tốn 1 xu**. Đừng nhảy cloud sớm.

---

## 🔌 Tích hợp AI / Copilot?

Hiện tại (2026-05) chưa tool nào trong list có AI built-in. Tuy nhiên có thể combine:

- **K8sGPT** (open source) — chẩn đoán cluster bằng LLM
- **Kubectl AI** — natural language → kubectl command
- Cài thêm như extension Lens — xem [Lens user guide](../k8s-gui/lens.md) (chưa có)

---

## 🛠️ Các công cụ hỗ trợ phổ biến (cần cài kèm)

Dù pick tool nào, các utility sau gần như bắt buộc:

| Tool | Dùng để | Link guide |
|---|---|---|
| **kubectl** | CLI giao tiếp K8s API | (chưa có — viết sau) |
| **helm** | Package manager K8s | (chưa có) |
| **k9s** | TUI quản lý cluster | (chưa có) |
| **stern** | Tail logs nhiều Pod cùng lúc | (chưa có) |
| **kubectx + kubens** | Đổi context/namespace nhanh | (chưa có) |
| **Lens** | GUI quản lý cluster | (chưa có) |

---

## 📦 Repo OSS hữu ích

| Repo | Khi nào tham khảo |
|---|---|
| [kubernetes/minikube](https://github.com/kubernetes/minikube) | Issue khi cài Minikube |
| [kubernetes-sigs/kind](https://github.com/kubernetes-sigs/kind) | Cấu hình Kind cluster |
| [k3d-io/k3d](https://github.com/k3d-io/k3d) | k3d docs |
| [awesome-kubernetes](https://github.com/ramitsurana/awesome-kubernetes) | Bộ sưu tập tool/learn |
| [k8sgpt-ai/k8sgpt](https://github.com/k8sgpt-ai/k8sgpt) | AI diagnose cluster |

---

## 🔗 Liên kết

- 📚 Bài lesson K8s → [10_DevOps/kubernetes/lessons/01_basic/00_what-is-k8s.md](../../10_DevOps/kubernetes/lessons/01_basic/00_what-is-k8s.md)
- 🗺️ Lab series → [docker-to-k8s lab](../../00_Roadmaps/lab-series/docker-to-k8s_lab-series.md) (chưa có)
- 🛠️ Cluster GUI → [Lens](../k8s-gui/lens.md) (chưa có)

---

## 📌 Changelog

- **v1.0.0 (19/05/2026)** — Bản đầu tiên. So sánh 3 tool chính (Minikube/Kind/k3d) + alternative + utility kèm theo.
