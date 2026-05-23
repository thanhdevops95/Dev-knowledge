# Bài #10 — Sử Dụng NodePort Service Để Expose Pod (Hands-On)

> 🎯 **Hands-on lần đầu** — tạo NodePort Service bằng `kubectl expose` (Imperative).

---

## 📋 Metadata

- **Bài số:** #10
- **Module:** 04-expose-pod-nodeport
- **Cấp độ:** `BEGINNER`
- **Thời lượng video gốc:** ~7 phút
- **Prerequisites:** [Bài #9 — NodePort Cơ chế](01-nodeport-co-che-hoat-dong.md), Pod đang chạy
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Tạo **NodePort Service** bằng `kubectl expose`
- [ ] Phân biệt rõ **`port`** vs **`targetPort`** vs **`nodePort`**
- [ ] Truy cập Pod qua NodePort (cả Minikube và máy thật)
- [ ] Biết shortcut `svc` cho `service`

---

## 📚 Nội Dung

### 1. `kubectl expose` — Tạo Service Imperative

#### Cú pháp tổng quát

```bash
kubectl expose pod <pod-name> \
  --name=<service-name> \
  --port=<service-port> \
  --target-port=<container-port> \
  --type=NodePort
```

| Flag              | Ý nghĩa                                |
| ----------------- | -------------------------------------- |
| `--name`          | Tên Service (vd: `service-1`)          |
| `--port`          | Port của Service (cluster-internal)    |
| `--target-port`   | Port của container bên trong           |
| `--type=NodePort` | Loại service (mặc định là `ClusterIP`) |

> 💡 Nếu bỏ `--target-port` thì sẽ = `--port`. Nên ghi rõ cả 2 cho dễ debug.

---

### 2. Service Types (Tổng quan)

```
ClusterIP   ← Default. Cluster-internal only
NodePort    ← Expose qua port của Node (30000-32767)  ← Bài này
LoadBalancer ← Cloud LB (AWS ELB, GCP LB...)
ExternalName ← Map qua DNS bên ngoài (vd: api.external.com)
```

---

## 💻 Hands-On / Demo

### Setup: Tạo Pod

```bash
# Tạo Pod với image có web server (nginx)
kubectl run app-1 --image=nginx --port=80

# Verify
kubectl get pods
# NAME    READY   STATUS    RESTARTS   AGE
# app-1   1/1     Running   0          10s
```

---

### Bước 1: Expose Pod Bằng NodePort

```bash
kubectl expose pod app-1 \
  --name=service-1 \
  --port=80 \
  --target-port=80 \
  --type=NodePort

# Output:
# service/service-1 exposed
```

---

### Bước 2: Xem Service

```bash
# Liệt kê services
kubectl get services
# hoặc viết tắt:
kubectl get svc

# NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
# kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP        1h
# service-1    NodePort    10.97.105.123   <none>        80:31214/TCP   30s
```

**Phân tích cột `PORT(S)`:**

```
80:31214/TCP
│   │
│   └── NodePort (random trong 30000-32767)
└────── Service Port (port internal trong cluster)
```

> 💡 NodePort là **random** khi tạo bằng Imperative. Muốn chỉ định? Dùng YAML (Bài #14 sẽ học).

---

### Bước 3: Xem Chi Tiết Service

```bash
kubectl describe service service-1

# Output:
# Name:                     service-1
# Namespace:                default
# Labels:                   run=app-1
# Selector:                 run=app-1                  ← Quan trọng!
# Type:                     NodePort
# IP:                       10.97.105.123
# Port:                     <unset>  80/TCP
# TargetPort:               80/TCP
# NodePort:                 <unset>  31214/TCP         ← External port
# Endpoints:                10.99.9.9:80               ← Pod IP:port
# Session Affinity:         None
# External Traffic Policy:  Cluster
```

> 🔑 **Selector** quyết định Service trỏ đến Pod nào (dựa trên labels). Khi dùng `kubectl run`, K8s tự gán label `run=app-1`.

---

### Bước 4: Truy Cập Service

#### Option A: Trên Minikube (cho học)

```bash
# Get URL truy cập
minikube service service-1 --url

# Output (ví dụ):
# http://192.168.58.2:31214

# Mở browser
minikube service service-1
```

> 💡 Minikube tự xử lý port-forward từ máy bạn → Node của Minikube. **Trên cluster thật không cần.**

#### Option B: Trên máy chủ thật (production)

```bash
# Lấy IP của Node
kubectl get nodes -o wide

# NAME       STATUS   ROLES           INTERNAL-IP    EXTERNAL-IP
# worker-1   Ready    <none>          10.10.5.8      54.123.45.67

# Truy cập (qua external IP)
curl http://54.123.45.67:31214

# Hoặc internal (từ máy khác trong VPC)
curl http://10.10.5.8:31214
```

---

### Bước 5: Cleanup

```bash
kubectl delete service service-1
kubectl delete pod app-1
```

---

## 📊 Sơ Đồ Toàn Cảnh

```
┌─── kubectl expose ────────────────────────────────────────┐
│                                                            │
│  USER                                                      │
│    │ http://10.10.5.8:31214                                │
│    ▼                                                       │
│  ┌──── Node (10.10.5.8) ──────────────────────────────┐   │
│  │  NodePort: 31214 ◄─── kube-proxy mở port này       │   │
│  │      │                                              │   │
│  │      ▼                                              │   │
│  │  Service: service-1                                 │   │
│  │  ─ Type: NodePort                                   │   │
│  │  ─ Selector: run=app-1                              │   │
│  │  ─ port: 80, targetPort: 80, nodePort: 31214        │   │
│  │      │                                              │   │
│  │      ▼ (selector match label)                       │   │
│  │  ┌── Pod app-1 ──────┐                              │   │
│  │  │ label: run=app-1   │                              │   │
│  │  │ container :80      │                              │   │
│  │  └────────────────────┘                              │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Lưu Ý

- 🔥 NodePort tạo bằng Imperative là **random** — production nên dùng YAML để fix port
- 🔥 Service dựa trên **Selector** match Pod label → đổi label Pod = mất kết nối
- 🔥 Service hoạt động **cluster-wide** — Pod chạy ở Node nào, NodePort mọi Node đều route được
- ⚠️ Trên Minikube, IP NodePort là Minikube VM IP — dùng `minikube service` cho tiện
- ⚠️ Khi Pod restart, Pod IP thay đổi → Service tự update endpoint (không cần làm gì)

---

## ✅ Self-Check

1. **Lệnh nào tạo NodePort Service?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl expose pod <pod> --name=<svc> --port=<p> --target-port=<tp> --type=NodePort
   ```

   </details>

2. **Phân biệt `port`, `targetPort`, `nodePort` trong output `80:31214/TCP`?**
   <details>
   <summary>Đáp án</summary>
   - `port = 80` — Service port (internal)
   - `targetPort` (mặc định = port) — Container port bên trong Pod
   - `nodePort = 31214` — Port public ra Node (random 30000-32767)
   </details>

3. **Service tìm Pod backend như thế nào?**
   <details>
   <summary>Đáp án</summary>
   Qua **Selector** — match label của Pod. VD: `run=app-1`.
   </details>

4. **Lệnh viết tắt của `kubectl get services`?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl get svc
   ```

   </details>

5. **Trên Minikube, cách dễ nhất để mở browser truy cập NodePort là gì?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   minikube service <service-name>
   # hoặc chỉ lấy URL:
   minikube service <service-name> --url
   ```

   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #9 — NodePort Cơ Chế](01-nodeport-co-che-hoat-dong.md)
- ➡️ [Bài #11 — kubectl logs](../03-pod-and-kubectl/02-kubectl-logs.md) (đã học)
- ➡️ [Module 05 — Imperative vs Declarative](../05-imperative-vs-declarative/README.md)

### Tài Nguyên

- 📖 [kubectl expose](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#expose)
- 📖 [Service Concept](https://kubernetes.io/docs/concepts/services-networking/service/)
- 📺 Video gốc: `Decopy_✅ #10 _ Sử Dụng NodePort Service..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Mới đầu nhìn nó cũng phức tạp. Các bạn cứ làm thử 5-6 lần là quen ngay. Nhưng nếu bỏ lâu không làm, sẽ bị quên — thậm chí nhầm. Nên cố gắng hands-on thường xuyên!"*

> 💬 *"Trong Help (`kubectl expose --help`) có rất nhiều ví dụ. Khi đi thi chứng chỉ, các bạn được mở tài liệu — quen với --help là một cách rất tốt!"*

> 💬 *"Muốn chỉ định cố định cái NodePort thay vì để random — phải dùng Declarative (YAML manifest) ở Bài #14."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
