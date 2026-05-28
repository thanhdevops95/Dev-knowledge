# Bài #39 — Resource Quotas (Giới Hạn Tài Nguyên Theo Namespace)

> 🎯 Giới hạn tài nguyên cho cả namespace — quan trọng cho **multi-tenant**.

---

## 📋 Metadata

- **Bài số:** #39
- **Module:** 10-resource-management
- **Cấp độ:** `ADVANCED`
- **Thời lượng video gốc:** ~10 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu **ResourceQuota** là gì
- [ ] Tạo Quota cho CPU/Memory
- [ ] Hiểu Quota chỉ áp dụng nếu Pod **có khai báo** request/limit
- [ ] Use case multi-tenant SaaS

---

## 📚 Nội Dung

### 1. ResourceQuota Là Gì?

**ResourceQuota** = đặt giới hạn tài nguyên **cho cả namespace**.

```
┌─── Namespace: customer-A ────────────┐
│                                      │
│  Quota:                              │
│   - cpu request: 4                   │  ← Tổng tất cả Pod
│   - cpu limit: 8                     │
│   - memory request: 8Gi              │
│   - memory limit: 16Gi               │
│   - pods: 20                         │
│                                      │
│  ┌─── Pod-A ────┐                    │
│  │ req: 1 CPU   │                    │
│  └──────────────┘                    │
│  ┌─── Pod-B ────┐                    │
│  │ req: 1 CPU   │                    │
│  └──────────────┘                    │
│                                      │
│  Tổng đã dùng: 2 CPU / 4 CPU         │
└──────────────────────────────────────┘
```

→ Nếu user cố tạo Pod thứ 5 cần thêm 3 CPU (tổng = 5) → K8s **TỪ CHỐI** với error.

---

### 2. Use Case Multi-Tenant (SaaS)

**Scenario:** SaaS có 3 tier khách:

```
┌─── Customer Free Tier ──┐  Quota: 0.5 CPU, 256Mi RAM
│   (namespace: cust-1)   │
└─────────────────────────┘

┌─── Customer Gold Tier ──┐  Quota: 2 CPU, 4Gi RAM
│   (namespace: cust-2)   │
└─────────────────────────┘

┌─── Customer Plat Tier ──┐  Quota: 8 CPU, 16Gi RAM
│   (namespace: cust-3)   │
└─────────────────────────┘
```

→ Mỗi tier có quota riêng, **chia sẻ chung cluster** → tiết kiệm chi phí.

---

### 3. ResourceQuota YAML

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: ns1
spec:
  hard:
    requests.cpu: "1"        # Tổng request CPU max 1
    requests.memory: 1Gi
    limits.cpu: "2"          # Tổng limit CPU max 2
    limits.memory: 2Gi
    pods: "10"               # Max 10 Pod
```

```bash
# Tạo namespace
kubectl create ns ns1

# Apply quota
kubectl apply -f quota.yaml
# resourcequota/compute-resources created

# Verify
kubectl get resourcequota -n ns1
# NAME                AGE   REQUEST                                       LIMIT
# compute-resources   5s    requests.cpu: 0/1, requests.memory: 0/1Gi    limits.cpu: 0/2, limits.memory: 0/2Gi

kubectl describe resourcequota compute-resources -n ns1
# Name:            compute-resources
# Namespace:       ns1
# Resource         Used  Hard
# --------         ----  ----
# limits.cpu       0     2
# limits.memory    0     2Gi
# pods             0     10
# requests.cpu     0     1
# requests.memory  0     1Gi
```

---

### 4. Hành Vi Khi Vượt Quota

**Pod vi phạm Quota:**

```yaml
# Pod yêu cầu vượt quota
apiVersion: v1
kind: Pod
metadata:
  name: too-big
  namespace: ns1
spec:
  containers:
    - name: app
      image: nginx
      resources:
        requests:
          cpu: "2"     # Quota chỉ 1!
        limits:
          cpu: "3"
```

```bash
kubectl apply -f too-big.yaml
# Error from server (Forbidden):
#   pods "too-big" is forbidden:
#   exceeded quota: compute-resources,
#   requested: requests.cpu=2, used: requests.cpu=0,
#   limited: requests.cpu=1
```

→ K8s **block** ngay từ admission, không tạo Pod.

---

### 5. Quan Trọng: Pod PHẢI Khai Báo Request/Limit

**Nếu Quota set `limits.cpu`, mọi Pod trong namespace PHẢI có `limits.cpu`:**

```yaml
# Pod KHÔNG có limit
apiVersion: v1
kind: Pod
metadata:
  name: no-limit
  namespace: ns1
spec:
  containers:
    - name: app
      image: nginx
      resources:
        requests:
          cpu: "0.5"
        # KHÔNG có limits!
```

```bash
kubectl apply -f no-limit.yaml
# Error: failed quota:
#   must specify limits.cpu, limits.memory
```

→ **Phải khai báo** đầy đủ! Để bypass → dùng **LimitRange** (Bài #40) đặt giá trị mặc định.

---

### 6. Các Loại Resource Quota Hỗ Trợ

```yaml
spec:
  hard:
    # Compute
    requests.cpu: "10"
    requests.memory: 10Gi
    limits.cpu: "20"
    limits.memory: 20Gi

    # Storage
    requests.storage: 100Gi
    persistentvolumeclaims: "10"

    # Object count
    pods: "50"
    services: "10"
    configmaps: "20"
    secrets: "20"
    services.nodeports: "5"
    services.loadbalancers: "2"
```

---

## 💻 Hands-On / Demo

```bash
# 1. Tạo namespace + quota
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Namespace
metadata:
  name: ns1
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: compute-resources
  namespace: ns1
spec:
  hard:
    requests.cpu: "1"
    requests.memory: 1Gi
    limits.cpu: "2"
    limits.memory: 2Gi
EOF

# 2. Verify
kubectl describe resourcequota -n ns1

# 3. Deploy Pod hợp lệ
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: app1
  namespace: ns1
spec:
  containers:
    - name: app
      image: nginx
      resources:
        requests:
          cpu: "500m"
          memory: "512Mi"
        limits:
          cpu: "1"
          memory: "1Gi"
EOF

# 4. Verify quota usage
kubectl describe resourcequota -n ns1
# Used: requests.cpu: 500m/1, ...

# 5. Thử vượt quota
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: app2
  namespace: ns1
spec:
  containers:
    - name: app
      image: nginx
      resources:
        requests:
          cpu: "800m"     # 500 + 800 = 1300m > 1000m!
          memory: "512Mi"
        limits:
          cpu: "1"
          memory: "1Gi"
EOF
# Error: exceeded quota

# 6. Cleanup
kubectl delete ns ns1
```

---

## ⚠️ Lưu Ý

- 🔥 ResourceQuota **chỉ áp dụng** khi Pod khai báo request/limit
- 🔥 Pod tạo TRƯỚC khi áp Quota **không bị ảnh hưởng**
- 💡 Để force Pod khai báo limit → dùng **LimitRange** (Bài #40)
- ⚠️ Quota là **per-namespace** — không có cluster-wide quota built-in
- ✅ Nên dùng **ResourceQuota + LimitRange + RBAC** combo cho multi-tenant

---

## ✅ Self-Check

1. **ResourceQuota áp dụng ở scope nào?**
   <details>
   <summary>Đáp án</summary>
   **Namespace** — không phải cluster, không phải Pod.
   </details>

2. **Pod không có limit, namespace có Quota set `limits.cpu`. Tạo được không?**
   <details>
   <summary>Đáp án</summary>
   **KHÔNG**. Phải khai báo limits.cpu mới deploy được.
   </details>

3. **Use case chính của ResourceQuota?**
   <details>
   <summary>Đáp án</summary>
   - Multi-tenant SaaS (mỗi customer = 1 namespace + 1 quota)
   - Phân chia môi trường (dev/staging/prod)
   - Tránh 1 team "ăn" hết tài nguyên cluster
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Bài #38 — Metrics Server](04-metrics-server.md)
- ➡️ [Bài #40 — Limit Ranges](06-limit-ranges.md)

### Tài Nguyên

- 📖 [Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/)

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
