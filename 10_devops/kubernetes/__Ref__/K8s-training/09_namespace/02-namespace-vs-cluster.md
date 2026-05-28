# Bài #34 — Namespace vs Cluster (Phân Biệt)

> 🎯 Hiểu rõ sự khác biệt **vật lý vs logic** giữa Cluster và Namespace.

---

## 📋 Metadata

- **Bài số:** #34
- **Module:** 09-namespace
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~5 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Phân biệt **Cluster** (vật lý) vs **Namespace** (logic)
- [ ] Hiểu Namespace KHÔNG gắn với Node cụ thể
- [ ] Hiểu use case multi-tenant (mỗi customer = 1 namespace)

---

## 📚 Nội Dung

### 1. Cluster = Vật Lý

```
┌─────────────────── Cluster ────────────────────┐
│                                                 │
│  ┌─── Node 1 ───┐  ┌─── Node 2 ───┐  ┌─Node 3─┐│
│  │  Server vật lý│  │  Server vật lý│  │ Server ││
│  │  CPU/RAM/HDD  │  │  CPU/RAM/HDD  │  │ ...    ││
│  └───────────────┘  └───────────────┘  └────────┘│
│                                                 │
│  ┌─── Control Plane ─────────────────────┐      │
│  │  API Server, etcd, Scheduler, ...     │      │
│  └────────────────────────────────────────┘      │
└──────────────────────────────────────────────────┘

   Cluster = Tổng hợp Server vật lý
```

---

### 2. Namespace = Logic

```
            ┌──────── Cluster ───────────┐
            │                            │
            │   Node 1   Node 2   Node 3 │
            │                            │
            ├────────────────────────────┤
            │ Logical View (Namespaces): │
            │                            │
            │  ┌──── ns: dev ────────────┐
            │  │ pod-A (trên Node 1)     │
            │  │ pod-B (trên Node 2)     │  ← Pod có thể trên BẤT KỲ Node nào
            │  └─────────────────────────┘
            │                            │
            │  ┌──── ns: prod ───────────┐
            │  │ pod-X (trên Node 1)     │
            │  │ pod-Y (trên Node 2)     │
            │  │ pod-Z (trên Node 3)     │
            │  └─────────────────────────┘
            │                            │
            │  ┌──── ns: test ───────────┐
            │  │ pod-T (trên Node 1)     │
            │  └─────────────────────────┘
            │                            │
            └────────────────────────────┘
```

→ **Namespace KHÔNG gắn với Node nào.** Pod của 1 namespace có thể nằm rải rác trên nhiều Node.

---

### 3. So Sánh

| Tiêu chí | Cluster | Namespace |
|----------|---------|-----------|
| **Bản chất** | Vật lý (server) | Logic |
| **Số lượng** | 1 K8s/cluster | Nhiều /cluster |
| **Chia sẻ resource** | Có (CPU/RAM của Node) | Có (qua ResourceQuota) |
| **Network** | Có sẵn | KHÔNG isolate (cần NetworkPolicy) |
| **Phân quyền** | Cluster admin | Namespace admin (RBAC) |
| **Chi phí** | Tốn (server) | Không (ảo) |

---

### 4. Use Case Multi-Tenant (SaaS)

**Scenario:** SaaS company có 100 khách hàng, mỗi khách dùng app riêng.

```
┌──────── Cluster (chia sẻ) ─────────┐
│                                    │
│ ┌─ ns: customer-A ──────┐          │
│ │  app + db + cache     │          │
│ └───────────────────────┘          │
│                                    │
│ ┌─ ns: customer-B ──────┐          │
│ │  app + db + cache     │          │
│ └───────────────────────┘          │
│                                    │
│ ┌─ ns: customer-C ──────┐          │
│ │  app + db + cache     │          │
│ └───────────────────────┘          │
│                                    │
│        ... 100 customers           │
└────────────────────────────────────┘
```

**Lợi ích:**

- ✅ Mỗi customer **isolate** logic
- ✅ Có thể đặt **ResourceQuota** riêng cho từng tenant
- ✅ Phân quyền **RBAC** riêng (mỗi tenant chỉ thấy ns của mình)
- ✅ Tiết kiệm chi phí (chia sẻ chung Node)

---

### 5. Cấp Phát Tài Nguyên Theo Namespace

```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-quota
  namespace: dev
spec:
  hard:
    requests.cpu: "4"        # Tối đa 4 CPU
    requests.memory: 8Gi     # Tối đa 8 GB RAM
    limits.cpu: "8"
    limits.memory: 16Gi
    pods: "20"               # Tối đa 20 Pod
```

```bash
kubectl apply -f resource-quota.yaml
```

→ Mọi Pod trong `dev` mà cố vượt limit này sẽ **bị từ chối** bởi Kubernetes!

> 💡 Module 10 sẽ học chi tiết về ResourceQuota + LimitRange.

---

## 💻 Hands-On / Demo

```bash
# Xem các Node của cluster
kubectl get nodes
# NAME       STATUS   ROLES           AGE
# minikube   Ready    control-plane   10d

# Xem Pod đang chạy ở Node nào
kubectl get pods -A -o wide

# Tạo namespace + Pod, kiểm tra Pod nằm ở Node nào
kubectl create ns demo
kubectl run test --image=nginx -n demo
kubectl get pod -n demo -o wide
# Pod chạy trên Node nào? → có thể bất kỳ Node nào
```

---

## ⚠️ Lưu Ý

- 🔥 **Cluster là vật lý** — chia sẻ chi phí thật (server, network, lưu trữ)
- 🔥 **Namespace là ảo** — không tốn thêm chi phí
- 💡 Namespace KHÔNG quyết định Pod chạy ở Node nào (đó là job của Scheduler)
- 💡 Có thể "ép" Pod vào Node cụ thể bằng `nodeSelector`, `nodeAffinity`, `taints/tolerations`

---

## ✅ Self-Check

1. **Cluster và Namespace khác nhau ở điểm nào?**
   <details>
   <summary>Đáp án</summary>
   - Cluster = vật lý (server)
   - Namespace = logic (chỉ là khái niệm)
   </details>

2. **Pod thuộc namespace `dev` có chạy trên Node cố định không?**
   <details>
   <summary>Đáp án</summary>
   **Không**. Pod có thể chạy trên bất kỳ Node nào trong cluster — Scheduler quyết định.
   </details>

3. **Tại sao Namespace là core value của K8s?**
   <details>
   <summary>Đáp án</summary>
   - Multi-tenant SaaS: mỗi customer = 1 namespace
   - Phân chia môi trường: dev/staging/prod
   - Resource limit, RBAC theo namespace
   - Tiết kiệm chi phí (chia sẻ cluster)
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #32 — Namespace](01-namespace.md)
- ➡️ [Module 10 — Resource Management](../10-resource-management/README.md)

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Namespace là một core value của K8s. Nếu các bạn không dùng namespace thì mình cũng không biết các bạn dùng K8s để làm gì."*

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
