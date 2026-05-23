# Bài #32 — Namespace (Phân Vùng Logic Trong Cluster)

> 🎯 **Khái niệm core của K8s** — phân chia tài nguyên trong cluster thành nhiều "phòng" riêng.

---

## 📋 Metadata

- **Bài số:** #32
- **Module:** 09-namespace
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~13 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu **Namespace là gì** và tại sao cần
- [ ] Tạo Namespace bằng Imperative + Declarative
- [ ] Triển khai resource vào namespace cụ thể
- [ ] Liệt kê 4 namespace mặc định của K8s

---

## 📚 Nội Dung

### 1. Namespace Là Gì?

**Namespace = "phòng riêng" trong cluster** để:

- 🔥 **Isolate** tài nguyên (Pod, Service, Deployment)
- 🔥 **Trùng tên** ở các namespace khác nhau (`pod-1` ở `dev` ≠ `pod-1` ở `prod`)
- 🔥 **Limit** tài nguyên cho từng nhóm (CPU, RAM)
- 🔥 **Phân quyền** (RBAC) — dev chỉ thao tác namespace `dev`

```
┌────────────────── Cluster ────────────────────┐
│                                                │
│  ┌─── ns: dev ────┐    ┌─── ns: prod ──┐      │
│  │  pod-1          │    │  pod-1         │      │
│  │  app-svc        │    │  app-svc       │      │
│  │  CPU limit: 4   │    │  CPU: 32       │      │
│  └─────────────────┘    └────────────────┘      │
│                                                │
│  ┌─── ns: test ───┐    ┌─── ns: shared ┐      │
│  │  ...           │    │  ...           │      │
│  └─────────────────┘   └────────────────┘      │
│                                                │
└────────────────────────────────────────────────┘
```

---

### 2. 4 Namespace Mặc Định

```bash
kubectl get namespaces
# NAME              STATUS   AGE
# default           Active   10d   ← Khi không chỉ định, resource tạo ở đây
# kube-system       Active   10d   ← System pods (CoreDNS, kube-proxy...)
# kube-public       Active   10d   ← Read-only cho mọi user
# kube-node-lease   Active   10d   ← Heartbeat của Node lên Control Plane
```

---

### 3. Tạo Namespace

**Imperative:**

```bash
kubectl create namespace dev
# namespace/dev created

kubectl get ns
# NAME    STATUS    AGE
# dev     Active    7s
# ...
```

**Declarative:**

```yaml
# ns.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: ns1
---
apiVersion: v1
kind: Namespace
metadata:
  name: ns2
```

```bash
kubectl apply -f ns.yaml
# namespace/ns1 created
# namespace/ns2 created
```

> 💡 Namespace **không có** `spec` — chỉ cần `metadata.name`.

---

### 4. Triển Khai Resource Vào Namespace

**Cách 1: Flag `-n`:**

```bash
kubectl run pod-1 --image=nginx --port=80 -n dev
kubectl get pod -n dev
```

**Cách 2: YAML với `metadata.namespace`:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-1
  namespace: dev      # ← Namespace ở metadata
spec:
  containers:
    - name: nginx
      image: nginx:1.24
```

```bash
kubectl apply -f pod.yaml
```

---

### 5. Trùng Tên Ở Khác Namespace

```bash
# Tạo pod-1 ở default
kubectl run pod-1 --image=nginx -n default

# Cùng tên pod-1, nhưng ở dev → OK
kubectl run pod-1 --image=nginx -n dev

# Verify
kubectl get pod -n default     # pod-1
kubectl get pod -n dev         # pod-1
```

> 🔥 K8s định danh resource bằng `<namespace>/<name>`.

---

### 6. Resource Có/Không Có Namespace

```bash
kubectl api-resources --namespaced=true   # có namespace
# pods, services, deployments, configmaps...

kubectl api-resources --namespaced=false  # KHÔNG có namespace
# nodes, namespaces, persistentvolumes, clusterroles...
```

| Có namespace | Không có namespace |
|--------------|---------------------|
| Pod, Service, Deployment | Node, Namespace, ClusterRole, PersistentVolume |
| ConfigMap, Secret, RS | StorageClass, ClusterIssuer |

---

### 7. Liệt Kê Resource Tất Cả Namespace

```bash
# Tất cả Pod ở mọi namespace
kubectl get pods --all-namespaces
# = kubectl get pods -A

# Tất cả Service ở mọi namespace
kubectl get svc -A

# Liệt kê Pod ở namespace cụ thể
kubectl get pods -n kube-system
```

---

### 8. Network Mặc Định: KHÔNG Isolate

> ⚠️ **Quan trọng:** Mặc định **mọi Pod ở mọi namespace** đều có thể giao tiếp với nhau!

```
Pod A (ns: dev)  ─────►  Pod B (ns: prod)   ✅ KẾT NỐI ĐƯỢC
```

**Để isolate** cần dùng:

- 🔒 **NetworkPolicy** (built-in)
- 🔒 **Calico**, **Cilium** (CNI plugins nâng cao)

→ Bài #33 sẽ demo việc kết nối cross-namespace.

---

## 💻 Hands-On / Demo

```bash
# 1. Tạo 2 namespace
kubectl create ns ns1
kubectl create ns ns2

# 2. Tạo Pod ở ns1
kubectl run pod-1 --image=nginx -n ns1

# 3. Tạo Service ở ns2
cat <<EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app1
  namespace: ns2
spec:
  replicas: 2
  selector:
    matchLabels:
      app: app1
  template:
    metadata:
      labels:
        app: app1
    spec:
      containers:
        - name: nginx
          image: nginx:1.24
---
apiVersion: v1
kind: Service
metadata:
  name: app1-svc
  namespace: ns2
spec:
  type: NodePort
  selector:
    app: app1
  ports:
    - port: 80
      targetPort: 80
EOF

# 4. Verify
kubectl get pod -A
kubectl get svc -A

# 5. Cleanup
kubectl delete ns ns1 ns2
# (xóa namespace = xóa tất cả resource trong đó!)
```

---

## ⚠️ Lưu Ý

- 🔥 **Xóa namespace** = xóa **tất cả resource** trong đó!
- 🔥 Tên namespace phải lowercase, alphanumeric, dash (DNS-compliant)
- 💡 Namespace = **logical**, KHÔNG phải physical (có thể chạy trên nhiều Node)
- ⚠️ Mặc định **không isolate network** — cần NetworkPolicy

---

## ✅ Self-Check

1. **Khi không chỉ định namespace, resource tạo ở đâu?**
   <details>
   <summary>Đáp án</summary>
   `default` namespace.
   </details>

2. **Có thể có 2 Pod cùng tên `pod-1` trong cluster không?**
   <details>
   <summary>Đáp án</summary>
   **Có** — nếu ở **2 namespace khác nhau**.
   </details>

3. **Resource nào KHÔNG thuộc namespace?**
   <details>
   <summary>Đáp án</summary>
   `Node`, `Namespace` (chính nó), `PersistentVolume`, `ClusterRole`, `StorageClass`.
   </details>

4. **Default namespace mặc định có những namespace nào?**
   <details>
   <summary>Đáp án</summary>
   `default`, `kube-system`, `kube-public`, `kube-node-lease`.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Module 08 — Services](../08-services/README.md)
- ➡️ [Bài #34 — Namespace vs Cluster](02-namespace-vs-cluster.md)
- 🔗 Liên quan: [Bài #33 — Curl Pod (cross-namespace)](../03-pod-and-kubectl/04-curl-pod.md)

### Tài Nguyên

- 📖 [Namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
