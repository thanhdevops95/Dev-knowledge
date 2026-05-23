# Bài #8 — Pod là gì? Demo `kubectl run`

> 🎯 **Đây là khái niệm nền tảng nhất** — đơn vị triển khai NHỎ NHẤT trên K8s không phải Container mà là **Pod**.

---

## 📋 Metadata

- **Bài số:** #8
- **Module:** 03-pod-and-kubectl
- **Cấp độ:** `BEGINNER`
- **Thời lượng video gốc:** ~7 phút
- **Prerequisites:** [Module 02 — Setup](../02-environment-setup/README.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Định nghĩa được **Pod** và phân biệt với **Container**
- [ ] Tạo Pod đầu tiên bằng `kubectl run`
- [ ] Xem trạng thái Pod với `kubectl get pods` và `kubectl describe`
- [ ] Hiểu khái niệm **Horizontal Scaling** (scale ngang)
- [ ] Biết cạm bẫy về **image pull policy** (lý do code không update)

---

## 📚 Nội Dung

### 1. Pod là Gì?

**Pod** = đơn vị triển khai nhỏ nhất trong K8s. **KHÔNG phải Container.**

```
                  Worker Node (1 IP)
   ┌──────────────────────────────────────────┐
   │                                          │
   │  ┌─────── Pod 1 (1 IP) ────────┐         │
   │  │   ┌────────────┐             │         │
   │  │   │ Container 1│             │         │
   │  │   │ port 8080  │             │         │
   │  │   └────────────┘             │         │
   │  └─────────────────────────────┘         │
   │                                          │
   │  ┌─────── Pod 2 (1 IP) ────────┐         │
   │  │   ┌────────────┐ ┌─────────┐│         │
   │  │   │ App        │ │ Logger  ││         │
   │  │   │ Container  │ │ sidecar ││         │
   │  │   │ port 8080  │ │ container│         │
   │  │   └────────────┘ └─────────┘│         │
   │  └─────────────────────────────┘         │
   └──────────────────────────────────────────┘
```

**Đặc điểm Pod:**

- 1 Pod chiếm **1 IP** (không phải Container chiếm IP)
- 1 Pod có thể chứa **1 hoặc nhiều Container**
- Container trong cùng 1 Pod **chia sẻ network** (gọi nhau qua `localhost`)
- Container trong cùng 1 Pod **chia sẻ volume**
- 1 Pod được scale **cùng nhau** (không thể scale 1 container riêng)

---

### 2. Khi Nào Dùng Multi-Container Pod?

**Phổ biến: 1 Pod = 1 Container** (best practice).

**Ngoại lệ (Sidecar Pattern):**

```
┌─── Pod ───────────────────────────┐
│  ┌──────────────┐ ┌─────────────┐ │
│  │  Main App    │ │  Sidecar    │ │
│  │  (business   │ │  (logging,  │ │
│  │   logic)     │ │   monitoring│ │
│  └──────────────┘ │   external) │ │
│                   └─────────────┘ │
└──────────────────────────────────┘
```

**Khi nào nên?**
- Sidecar logging
- Sidecar service mesh (Istio Envoy)
- Sidecar adapter (chuyển đổi protocol)

> ⚠️ **Trade-off:** Nhồi 2 container thì gọi nhau nhanh qua localhost, NHƯNG khi scale phải scale CẢ HAI cùng nhau!

---

### 3. Horizontal Scaling vs Vertical Scaling

```
PROBLEM: 1 Pod (1GB RAM, 0.5 CPU) không đủ phục vụ 10K user!
         ↓
   Có 2 cách scale:

┌─────────────── VERTICAL ───────────────┐
│   Cấp Pod thành 4GB RAM, 2 CPU         │
│   ❌ Có giới hạn (RAM Node, CPU Node)  │
│   ❌ Phải restart Pod để áp config mới │
└────────────────────────────────────────┘

┌─────────────── HORIZONTAL ─────────────┐
│   Tạo 4 Pod giống nhau (1GB mỗi cái)   │
│   ✅ Best Practice trên K8s             │
│   ✅ Scale gần như vô hạn              │
│   ✅ HA (1 Pod chết, các Pod khác OK)  │
└────────────────────────────────────────┘
```

K8s thiên về **Horizontal Scaling**. Nếu hết tài nguyên 1 Node, K8s tự tạo Pod ở Node khác (hoặc tạo Node mới với Cluster Autoscaler).

---

## 💻 Hands-On / Demo

### 4. Tạo Pod Đầu Tiên

```bash
# Trước khi bắt đầu — đảm bảo cluster đang chạy
kubectl get pods
# No resources found in default namespace.  ← OK!

# Tạo Pod
kubectl run app-1 --image=nginx --port=80

# Output:
# pod/app-1 created
```

**Diễn giải command:**
- `kubectl run` — chạy 1 Pod
- `app-1` — tên Pod
- `--image=nginx` — image dùng (lấy từ Docker Hub mặc định)
- `--port=80` — container expose port 80

### 5. Xem Trạng Thái Pod

```bash
# Liệt kê Pod
kubectl get pods

# NAME    READY   STATUS    RESTARTS   AGE
# app-1   1/1     Running   0          15s

# Watch real-time (như docker ps -a -w)
kubectl get pods --watch
# hoặc viết tắt:
kubectl get pods -w

# Xem chi tiết Pod
kubectl describe pod app-1

# Output (rút gọn):
# Name:         app-1
# Status:       Running
# IP:           172.17.0.7
# Containers:
#   app-1:
#     Image:        nginx
#     Container ID: docker://abc123...
#     Image ID:     docker.io/library/nginx@sha256:...
#     Port:         80/TCP
# Events:
#   Type    Reason     Age  Message
#   Normal  Scheduled  20s  Successfully assigned default/app-1 to minikube
#   Normal  Pulling    19s  Pulling image "nginx"
#   Normal  Pulled     15s  Successfully pulled image "nginx"
#   Normal  Created    15s  Created container app-1
#   Normal  Started    15s  Started container app-1
```

### 6. Trạng thái phổ biến của Pod

| Status              | Ý nghĩa                         |
| ------------------- | ------------------------------- |
| `Pending`           | Đang lập lịch / chờ resources   |
| `ContainerCreating` | Đang pull image / tạo container |
| `Running`           | Đang chạy                       |
| `Completed`         | Đã xong (Pod 1 lần)             |
| `CrashLoopBackOff`  | ❌ Crash lặp lại                 |
| `ImagePullBackOff`  | ❌ Pull image lỗi                |
| `Error`             | ❌ Lỗi chung                     |

### 7. Xóa Pod

```bash
kubectl delete pod app-1
# pod "app-1" deleted
```

---

### 8. ⚠️ Cạm Bẫy: Image Pull Policy

> 💬 *"Mình bị chuyện này và mất loay hoay nửa ngày — cứ nghĩ mình làm sai code!"*

**Vấn đề:** Bạn update image `myapp:v1` trên Docker Hub, rồi `kubectl run` lại — code KHÔNG thay đổi. Vì sao?

**Nguyên nhân:** Image policy mặc định = `IfNotPresent` → nếu Node đã có cache image, nó **không pull lại**.

```
┌──────────────────── Worker Node ────────────────────┐
│                                                       │
│  Local Cache: myapp:v1 (cũ, từ lần trước)            │
│                                                       │
│  kubectl run → Tag = v1                               │
│   → Policy: IfNotPresent                              │
│   → Tìm cache: TÌM THẤY → DÙNG cache CŨ! ❌         │
│   (KHÔNG pull từ Docker Hub mới)                     │
└──────────────────────────────────────────────────────┘
```

**Giải pháp:**

| Cách                      | Lệnh / Cách dùng                                       |
| ------------------------- | ------------------------------------------------------ |
| **1. Đổi tag**            | Build & push `v2`, dùng `--image=myapp:v2`             |
| **2. Dùng `latest`**      | `--image=myapp:latest` + đặt `imagePullPolicy: Always` |
| **3. Force pull mỗi lần** | Set `imagePullPolicy=Always` trong YAML                |

**Best Practice:** Đừng dùng `:latest` cho production. Mỗi build = mỗi tag (semver hoặc git SHA).

---

## ⚠️ Lưu Ý

- 🔥 **Đơn vị triển khai = Pod** (không phải Container)
- 🔥 1 Pod = 1 IP, container trong cùng Pod gọi nhau qua `localhost`
- 🔥 Image Policy mặc định = `IfNotPresent` → cẩn thận khi dev
- ⚠️ Multi-container Pod là **đặc biệt** — đa số trường hợp nên 1 Pod = 1 Container
- ⚠️ `kubectl run` là **imperative** — production nên dùng YAML (declarative, sẽ học ở Bài #14)

---

## ✅ Self-Check

1. **Đơn vị triển khai nhỏ nhất trên K8s là gì?**
   <details>
   <summary>Đáp án</summary>
   **Pod** (không phải Container).
   </details>

2. **2 container trong cùng 1 Pod giao tiếp với nhau như thế nào?**
   <details>
   <summary>Đáp án</summary>
   Qua `localhost` (chia sẻ network namespace). VD: `http://localhost:8080`.
   </details>

3. **Câu lệnh nào tạo Pod đơn giản nhất?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl run <pod-name> --image=<image-name> --port=<port>
   ```

   </details>

4. **Image Policy mặc định là gì? Hậu quả?**
   <details>
   <summary>Đáp án</summary>
   `IfNotPresent` — nếu Node đã có cache image, KHÔNG pull mới. Kết quả: code update ở registry nhưng Pod chạy code cũ.
   </details>

5. **K8s scale theo chiều ngang hay dọc?**
   <details>
   <summary>Đáp án</summary>
   **Horizontal (ngang)** — best practice. Tạo nhiều Pod thay vì cấp Pod to hơn.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #7 — K8s Versions](../02-environment-setup/02-kubernetes-version.md)
- ➡️ [Bài #11 — kubectl logs](02-kubectl-logs.md)
- 🏠 [Quay về index Module 03](README.md)

### Tài Nguyên

- 📖 [Pod (Official Docs)](https://kubernetes.io/docs/concepts/workloads/pods/)
- 📖 [Image Pull Policy](https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy)
- 📺 Video gốc: `Decopy_✅ #8 _ Pod là gì_..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Đa phần các bạn sẽ thấy 1 Pod có 1 Container. Multi-container Pod là trường hợp đặc thù — không phổ biến."*

> 💬 *"Mình bị chuyện image pull policy và mất loay hoay NỬA NGÀY — cứ nghĩ mình làm sai. Hóa ra cache local."*

> 💬 *"Kubernetes thiên về horizontal scaling — đó cũng là best practice."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
