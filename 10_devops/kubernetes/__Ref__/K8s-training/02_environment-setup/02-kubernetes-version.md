# Bài #7 — Kubernetes Versions & Version Skew Policy

> 🎯 Bài cực kỳ quan trọng cho **vận hành production**! Nếu bỏ qua, sau này upgrade cluster sẽ rất đau đầu.

---

## 📋 Metadata

- **Bài số:** #7
- **Module:** 02-environment-setup
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~10 phút
- **Prerequisites:** [Bài #4 — Cluster Architecture](../01-core-concepts/03-cluster-architecture.md), [Bài #6 — Setup](01-cai-dat-minikube-kubectl-docker.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Hiểu **format version** của K8s: `MAJOR.MINOR.PATCH`
- [ ] Biết **lifecycle support**: 14 tháng (12 standard + 2 maintenance)
- [ ] Hiểu **Version Skew Policy** giữa các component
- [ ] Biết check version cho cluster của mình

---

## 📚 Nội Dung

### 1. Cấu Trúc Phiên Bản: `MAJOR.MINOR.PATCH`

```
       Ví dụ: 1.29.4
              │ │  │
              │ │  └─ PATCH  (bug fix, security patch)
              │ └──── MINOR  (release mới, feature mới)
              └────── MAJOR  (breaking change lớn — hiếm)
```

K8s release **MINOR mỗi ~4 tháng** → tốc độ rất nhanh!

```
2024:
├─ 1.30 (Apr)
├─ 1.31 (Aug)
└─ 1.32 (Dec)

2025:
├─ 1.33 (Apr)
├─ 1.34 (Aug)
└─ 1.35 (Dec)
```

---

### 2. Support Policy — Vòng Đời 14 Tháng

K8s **chỉ support 3 minor version gần nhất**.

```
Bây giờ là 1.30 mới ra ⇒ Support: 1.30, 1.29, 1.28
                          1.27 → End of Life ❌
```

#### Lifecycle 14 tháng cho mỗi minor version

```
┌──────────────────────────────────────────────────────────────┐
│                      14 THÁNG TỔNG CỘNG                       │
├──────────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐   ┌──────────────┐                 │
│  │ Standard Support     │   │ Maintenance   │   ❌ End of    │
│  │     12 tháng         │ → │   2 tháng     │ → Life (EOL)   │
│  │                      │   │               │                │
│  │  ✓ Bug fixes         │   │ Chỉ critical  │   Không hỗ trợ │
│  │  ✓ Security updates  │   │ + security    │   gì nữa       │
│  │  ✓ Cherry-picks      │   │               │                │
│  └──────────────────────┘   └──────────────┘                 │
└──────────────────────────────────────────────────────────────┘
```

#### Hậu quả nếu không upgrade

- Không nhận **security patch** → cluster bị lỗ hổng
- Không nhận **bug fixes**
- CNCF/Cloud không hỗ trợ → tự bơi

> 💬 *"Đây là một challenge cực kỳ lớn cho các bạn vận hành production với rất nhiều Node — phải upgrade đều đặn."*

---

### 3. Vì Sao EKS/GKE/AKS Lại "Sướng Hơn"?

```
┌─────────────────────────────────────────────────────┐
│  K8s SELF-MANAGED (tự dựng)                          │
│  ❌ Tự upgrade Control Plane (HA → 3 etcd, 3 API…)  │
│  ❌ Tự drain & rebuild Worker Nodes                 │
│  ❌ Tự lo HA, backup, security                      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  EKS / GKE / AKS  (managed)                          │
│  ✅ Cloud lo Control Plane                          │
│  ✅ Upgrade chỉ vài click / vài command             │
│  ✅ HA & backup tự động                             │
│  ❗ Vẫn phải upgrade Worker Nodes                   │
└─────────────────────────────────────────────────────┘
```

→ Đây là 1 trong nhiều lý do **chuyển từ K8s self-managed sang EKS/GKE/AKS**.

---

### 4. ⭐ Version Skew Policy — RẤT QUAN TRỌNG

K8s có nhiều component (apiserver, kubelet, kube-proxy, controller-manager, scheduler, kubectl…). **Các component có thể chạy version khác nhau** — nhưng phải tuân thủ **Skew Policy**.

> ⚠️ Vi phạm policy → component lỗi hoặc cluster crash!

#### Sơ đồ tổng quan

Đặt `x` = version của `kube-apiserver` (mới nhất trong các API server)

```
                     kube-apiserver
                     ┌─────────────┐
                     │      x      │  ← BẢN GỐC THAM CHIẾU
                     └─────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
   Control Plane       Worker Node         Client
   ┌────────────┐    ┌─────────────┐   ┌────────────┐
   │ scheduler  │    │  kubelet    │   │  kubectl   │
   │ controller │    │             │   │            │
   │ cloud-ctrl │    │  kube-proxy │   │            │
   └────────────┘    └─────────────┘   └────────────┘
       x-1               x-3              x±1
```

| Component                               | Range cho phép                   |
| --------------------------------------- | -------------------------------- |
| `kube-apiserver` (giữa các instance HA) | Cùng `x`, hoặc `x-1`             |
| `kubelet`                               | `x-3` ÷ `x` (lùi tối đa 3 minor) |
| `kube-proxy`                            | `x-3` ÷ `x`                      |
| `kube-scheduler`                        | `x-1` ÷ `x`                      |
| `kube-controller-manager`               | `x-1` ÷ `x`                      |
| `cloud-controller-manager`              | `x-1` ÷ `x`                      |
| `kubectl`                               | `x-1` ÷ `x+1` (linh hoạt nhất)   |

#### Ví Dụ Cụ Thể

```
APIServer = 1.30  (x = 1.30)

✅ kubelet 1.27, 1.28, 1.29, 1.30 — OK (x-3 ÷ x)
❌ kubelet 1.31 — KHÔNG OK (mới hơn API server)
❌ kubelet 1.26 — KHÔNG OK (quá cũ, x-4)

✅ scheduler 1.29, 1.30 — OK (x-1 ÷ x)
❌ scheduler 1.28 — KHÔNG OK (x-2)

✅ kubectl 1.29, 1.30, 1.31 — OK (x-1 ÷ x+1)
```

#### Trường Hợp HA Control Plane

Nếu có **2 API server** (HA):

```
APIServer 1: 1.30
APIServer 2: 1.29  (đang trong quá trình upgrade, chậm 1 version)

→ x = MIN(1.30, 1.29) = 1.29
→ Mọi component phải tính skew từ 1.29!
```

→ **Khi rolling upgrade, phải tính theo API server CŨ NHẤT.**

---

### 5. Quy Trình Upgrade An Toàn

K8s upgrade theo thứ tự **bottom-up**:

```
1. Upgrade kube-apiserver        (x → x+1)
2. Upgrade các component CP khác (scheduler, controller, cloud-cm)
3. Upgrade etcd (nếu cần)
4. Upgrade kubelet (Worker Node) — drain Pod trước
5. Upgrade kube-proxy
6. Upgrade kubectl của admin
```

> ⚠️ **Không bao giờ nhảy 2 minor version**! 1.28 → 1.30 phải qua 1.29.

---

## 💻 Hands-On / Demo

```bash
# Check version từng component
kubectl version

# Output:
# Client Version: v1.29.0   ← kubectl
# Server Version: v1.28.3   ← API Server (sau khi connect cluster)

# Check version của Node (kubelet)
kubectl get nodes -o wide

# Output:
# NAME       STATUS   VERSION
# minikube   Ready    v1.28.3   ← đây là kubelet version

# Check tất cả pod hệ thống và xem image version
kubectl get pods -n kube-system -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[0].image}{"\n"}{end}'

# Upgrade Minikube cluster lên version mới
minikube delete
minikube start --kubernetes-version=v1.30.0

# Trên EKS (sau này sẽ học):
# eksctl upgrade cluster --name=my-cluster --version=1.30 --approve
```

---

## ⚠️ Lưu Ý Quan Trọng

- 🚨 **Không bỏ qua minor version** khi upgrade (1.28 → 1.30 phải qua 1.29).
- 🚨 **Đọc CHANGELOG mỗi version** — có thể có deprecation/breaking change.
- 🚨 **Test trên staging trước** khi upgrade production.
- ⚠️ **Backup etcd** trước mọi upgrade.
- ⚠️ **Drain Node** trước khi upgrade kubelet để Pod chuyển sang Node khác.
- ✅ Production: lập **lịch upgrade quarterly** để bám sát support window 14 tháng.

---

## ✅ Self-Check

1. **Format version K8s gồm mấy phần?**
   <details>
   <summary>Đáp án</summary>
   3 phần: **MAJOR.MINOR.PATCH** (vd: 1.29.4)
   </details>

2. **K8s release minor mới mỗi bao lâu?**
   <details>
   <summary>Đáp án</summary>
   Khoảng **4 tháng** (3 lần/năm).
   </details>

3. **Lifecycle support 1 minor version là bao lâu?**
   <details>
   <summary>Đáp án</summary>
   **14 tháng** = 12 tháng standard support + 2 tháng maintenance mode.
   </details>

4. **Nếu APIServer = 1.30, kubelet được phép từ version nào đến nào?**
   <details>
   <summary>Đáp án</summary>
   `1.27` ÷ `1.30` (x-3 ÷ x). Kubelet KHÔNG được mới hơn API server.
   </details>

5. **Component nào "thoải mái" nhất về skew policy?**
   <details>
   <summary>Đáp án</summary>
   **`kubectl`** — được phép `x-1`, `x`, hoặc `x+1`. (Có thể mới hoặc cũ hơn API server 1 minor)
   </details>

6. **Có thể upgrade từ 1.28 → 1.30 trực tiếp không?**
   <details>
   <summary>Đáp án</summary>
   **KHÔNG**. Phải upgrade từng minor version: 1.28 → 1.29 → 1.30.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #6 — Cài đặt Minikube](01-cai-dat-minikube-kubectl-docker.md)
- ➡️ [Bài #8 — Pod là gì?](../03-pod-and-kubectl/01-pod-la-gi.md)
- 🏠 [Quay về index Module 02](README.md)

### Tài Nguyên

- 📖 [Kubernetes Version Skew Policy](https://kubernetes.io/releases/version-skew-policy/)
- 📖 [K8s Release Cycle](https://kubernetes.io/releases/release/)
- 📖 [Kubernetes Releases](https://kubernetes.io/releases/)
- 📺 Video gốc: `Decopy_✅ #7 _ Kubernetes Version..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Đây là challenge cực kỳ lớn cho các bạn vận hành production. Nếu các bạn không quen vấn đề maintenance/operation, đây sẽ là một cái cực kỳ đau đầu."*

> 💬 *"Sau này các bạn dùng EKS thì AWS đã làm hộ rất nhiều rồi — Control Plane HA, upgrade dễ dàng. Tự dựng cluster thì các bạn phải drain rồi stop rồi tạo Node mới rất mất thời gian."*

> 💬 *"Trên Minikube hiện tại của mình: kubectl 1.29, server 1.28 — kubectl mới hơn 1 minor, vẫn OK theo policy."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
