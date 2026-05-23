# Bài #4 — Cluster Architecture (Kiến Trúc Cluster K8s)

> ⭐ **Bài quan trọng nhất Module 01** — Hiểu kiến trúc giúp bạn debug, troubleshoot, và đi thi CKA dễ dàng.

---

## 📋 Metadata

- **Bài số:** #4
- **Module:** 01-core-concepts
- **Cấp độ:** `BEGINNER → INTERMEDIATE`
- **Thời lượng video gốc:** ~10 phút
- **Prerequisites:** [Bài #2 — K8s là gì?](01-kubernetes-la-gi.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Vẽ được **sơ đồ kiến trúc K8s** với 2 thành phần: Control Plane + Data Plane
- [ ] Liệt kê **5 component** trong Control Plane và chức năng từng cái
- [ ] Liệt kê **3 component** trên mỗi Worker Node và chức năng từng cái
- [ ] Hiểu **luồng request** từ Admin → API Server → Scheduler → Kubelet
- [ ] Phân biệt **Cluster** vs **Control Plane** vs **Worker Node**

---

## 📚 Nội Dung

### 1. Tổng Quan: 2 Phần Của 1 Cluster

```
┌─────────────────────────── KUBERNETES CLUSTER ──────────────────────────┐
│                                                                         │
│  ┌─────────────────────┐         ┌─────────────────────┐                │
│  │   CONTROL PLANE     │         │     DATA PLANE      │                │
│  │  (Master Node)      │ ◄────► │   (Worker Nodes)     │                │
│  │                     │         │                     │                │
│  │  - api-server       │         │  Worker 1: Pods     │                │
│  │  - etcd             │         │  Worker 2: Pods     │                │
│  │  - scheduler        │         │  Worker N: Pods     │                │
│  │  - controller-mgr   │         │                     │                │
│  │  - cloud-controller │         │                     │                │
│  └─────────────────────┘         └─────────────────────┘                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

| Phần              | Tên gọi khác      | Chạy gì?                               |
| ----------------- | ----------------- | -------------------------------------- |
| **Control Plane** | Master Node       | "Bộ não" — quản lý, điều phối          |
| **Data Plane**    | Worker Node, Node | "Cơ bắp" — chạy ứng dụng (Pod) thực sự |

> 💡 **Best practice:** Ứng dụng (user workload) **chỉ deploy trên Worker Node**, không deploy trên Master Node.

---

### 2. Control Plane — 5 Component

#### 2.1. `kube-apiserver` (cổng vào duy nhất)

```
Admin / kubectl ──HTTPS──► kube-apiserver ──► etcd / scheduler / controller / kubelet
```

- **Chức năng:** Tiếp nhận **mọi request** từ user (qua `kubectl`), từ các component khác.
- **Là điểm trung tâm** giao tiếp — mọi thứ đi qua nó.
- ⚠️ **Quan trọng nhất** → cần High Availability (HA) trong production.

#### 2.2. `etcd` (database key-value)

- **Chức năng:** Cơ sở dữ liệu **key-value** lưu **toàn bộ trạng thái cluster**.
- Là dự án thuộc CNCF (cùng tổ chức với K8s).
- ⚠️ **Quan trọng thứ 2** → backup thường xuyên!

```
etcd lưu gì?
├─ Spec của tất cả các Pod, Deployment, Service…
├─ Trạng thái hiện tại của cluster
├─ Cấu hình ConfigMap, Secret
└─ Mọi resource khác
```

#### 2.3. `kube-scheduler` (lập lịch)

- **Chức năng:** Quyết định **Pod nào chạy trên Node nào**.
- Tính toán dựa trên: tài nguyên còn lại, label selector, taint/toleration, affinity rules…
- ⚠️ Lưu ý: Scheduler **KHÔNG trực tiếp** triển khai Pod — chỉ quyết định và báo cho `kube-apiserver`.

#### 2.4. `kube-controller-manager` (giám sát baseline)

- **Chức năng:** Đảm bảo trạng thái thực tế = trạng thái mong muốn.
- Ví dụ: `ReplicaSet` muốn 5 Pod → Controller liên tục kiểm tra. Nếu chỉ có 4 → tạo thêm 1.
- Bao gồm nhiều controller con: Node Controller, Replication Controller, Endpoint Controller…

#### 2.5. `cloud-controller-manager` (kết nối cloud)

- **Chức năng:** Tích hợp với **cloud provider** (AWS, GCP, Azure…).
- Ví dụ: tạo Service type `LoadBalancer` → cloud-controller gọi AWS API tạo ELB.
- Khi chạy on-premise (Minikube/Kind), component này KHÔNG có/không hoạt động.

---

### 3. Worker Node — 3 Component

```
┌──────────────────── Worker Node ────────────────────┐
│                                                      │
│  ┌─────────────┐     ┌──────────────────────┐       │
│  │  kubelet    │     │  Container Runtime    │       │
│  │  (đại diện) │ ──► │  (Docker/containerd)  │       │
│  └─────────────┘     │                       │       │
│         ▲            │   ┌─────┐  ┌─────┐    │       │
│         │            │   │ Pod │  │ Pod │    │       │
│         │            │   └─────┘  └─────┘    │       │
│         │            └──────────────────────┘       │
│  ┌─────────────┐                                     │
│  │ kube-proxy  │  ← định tuyến network giữa các Pod │
│  └─────────────┘                                     │
└──────────────────────────────────────────────────────┘
              ▲
              │ giao tiếp 2 chiều với
              │
        kube-apiserver
```

#### 3.1. `kubelet` (đại diện K8s trên Node)

- **Chức năng:** Nhận lệnh từ `kube-apiserver` → triển khai Pod trên Node.
- Báo cáo trạng thái Pod (running, crashed, ready…) ngược về `kube-apiserver`.
- Ví dụ thân thiện: **"Thuyền trưởng" của 1 con thuyền (Node) chở nhiều container.**

#### 3.2. `kube-proxy` (network routing)

- **Chức năng:** Quản lý quy tắc network để các Pod nói chuyện với nhau (kể cả khác Node).
- Triển khai dưới dạng **DaemonSet** (chạy trên TẤT CẢ Node, kể cả Master).
- Hoạt động cùng với CoreDNS để resolve service name.

#### 3.3. Container Runtime (CRI)

- **Chức năng:** Thực sự chạy container.
- K8s định nghĩa interface chuẩn **CRI** (Container Runtime Interface) → hỗ trợ nhiều runtime:
  - **containerd** (mặc định hiện đại)
  - **CRI-O**
  - Docker (deprecated từ K8s 1.24)

---

### 4. Luồng Request: "Tôi muốn deploy 1 Pod"

Hành trình của 1 lệnh `kubectl apply -f pod.yaml`:

```
[1] Admin gõ:
    $ kubectl apply -f pod.yaml
                    │
                    ▼
[2] kube-apiserver nhận request, validate, lưu vào etcd
                    │
                    ▼
[3] kube-scheduler watch: "Có Pod mới chưa được assign Node!"
    → Tính toán: Node nào phù hợp nhất? (resource, affinity...)
    → Quyết định: "Pod này → Worker Node 2"
    → Báo lại cho kube-apiserver
                    │
                    ▼
[4] kube-apiserver ghi assignment vào etcd
                    │
                    ▼
[5] kubelet trên Worker Node 2 watch: "Có Pod assign cho mình!"
    → Gọi Container Runtime (containerd) tạo container
                    │
                    ▼
[6] Container Runtime pull image, start container
                    │
                    ▼
[7] kubelet báo cáo trạng thái: "Pod is Running" → kube-apiserver → etcd
                    │
                    ▼
[8] $ kubectl get pods   ← thấy Pod đã Running ✅
```

> 🔑 **Điểm mấu chốt:** Mọi component đều giao tiếp QUA `kube-apiserver`. Không có component nào "nhảy cóc" — đây là pattern **Hub-and-Spoke**.

---

## 💻 Hands-On / Demo

Bài này là lý thuyết. Khi bạn đã có cluster (Bài #6), có thể kiểm tra các component:

```bash
# Xem các Node trong cluster
kubectl get nodes

# Xem các component của Control Plane (chạy dưới dạng Pod trong namespace kube-system)
kubectl get pods -n kube-system

# Output mẫu (cluster Minikube):
# coredns-787d4945fb-xxxxx                  1/1     Running
# etcd-minikube                              1/1     Running
# kube-apiserver-minikube                    1/1     Running
# kube-controller-manager-minikube           1/1     Running
# kube-proxy-xxxxx                           1/1     Running
# kube-scheduler-minikube                    1/1     Running

# Xem chi tiết 1 component
kubectl describe pod kube-apiserver-minikube -n kube-system
```

---

## ⚠️ Lưu Ý

- 🔥 **Mọi giao tiếp đi qua `kube-apiserver`** — không có ngoại lệ.
- 🔥 **etcd là single source of truth** — backup là sống còn.
- 🔥 Trên **EKS/GKE/AKS**, cloud provider quản lý Control Plane → bạn không cần cài đặt/maintain.
- ⚠️ Nếu Control Plane **down**, các Pod đang chạy trên Worker **vẫn hoạt động bình thường**, nhưng không thể tạo/sửa/xóa resource mới.
- ⚠️ Production: Control Plane phải **HA** (3+ instance API Server, 3+ instance etcd).

---

## ✅ Self-Check

1. **Cluster K8s gồm 2 phần chính nào?**
   <details>
   <summary>Đáp án</summary>
   **Control Plane** (Master) và **Data Plane** (Worker Nodes).
   </details>

2. **Liệt kê 5 component của Control Plane.**
   <details>
   <summary>Đáp án</summary>
   1. `kube-apiserver`
   2. `etcd`
   3. `kube-scheduler`
   4. `kube-controller-manager`
   5. `cloud-controller-manager` (chỉ có trên cloud)
   </details>

3. **Component nào quyết định Pod sẽ chạy trên Node nào?**
   <details>
   <summary>Đáp án</summary>
   **`kube-scheduler`** — nhưng nó chỉ quyết định và báo cho `kube-apiserver`, không trực tiếp tạo Pod.
   </details>

4. **`kubelet` chạy ở đâu, làm gì?**
   <details>
   <summary>Đáp án</summary>
   `kubelet` chạy trên **mỗi Worker Node**. Nhiệm vụ:
   - Nhận lệnh từ `kube-apiserver` để tạo/xóa Pod
   - Gọi Container Runtime để thực thi
   - Báo cáo trạng thái Pod ngược về `kube-apiserver`
   </details>

5. **Nếu etcd bị crash hoàn toàn, hậu quả là gì?**
   <details>
   <summary>Đáp án</summary>
   Mất **toàn bộ trạng thái cluster** — tất cả config (Deployment, Service, ConfigMap…) biến mất. Đây là lý do **etcd backup** là việc sống còn trong production.
   </details>

6. **Pod đang chạy trên Worker, nếu Control Plane down thì sao?**
   <details>
   <summary>Đáp án</summary>
   **Vẫn chạy bình thường!** Pod đã được assign rồi — kubelet vẫn quản lý local. Chỉ là không tạo/sửa/xóa resource mới được.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #3 — Lý do nên & không nên dùng K8s](02-khi-nao-nen-dung-k8s.md)
- ➡️ [Bài #6 — Cài đặt Minikube, kubectl, Docker](../02-environment-setup/01-cai-dat-minikube-kubectl-docker.md)
- 🏠 [Quay về index Module 01](README.md)

### Tài Nguyên

- 📖 [Kubernetes Components (Official)](https://kubernetes.io/docs/concepts/overview/components/)
- 📖 [Cluster Architecture Detail](https://kubernetes.io/docs/concepts/architecture/)
- 📖 [etcd Documentation](https://etcd.io/docs/)
- 📺 Video gốc: `Decopy_✅ #4 _ Cluster Architecture..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Trong các Note có thể có hàng trăm Node trong hệ thống — đó là chuyện bình thường. Cho nên Scheduler phải đủ thông minh để chọn đúng Node phù hợp nhất."*

> 💬 *"`kubelet` giống như chủ nhà / thuyền trưởng — quản lý nội bộ của 1 Node, chở nhiều container ở đây."*

> 💬 *"Sau này dùng Amazon EKS thì việc giao tiếp giữa Control Plane và Worker Node đã được làm hộ mình rất nhiều thứ rồi — các bạn không cần lo phần đó nữa."*

> 💬 *"`kube-apiserver` và `etcd` là 2 component CỰC KỲ quan trọng → production luôn ưu tiên HA cho 2 cái này."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
