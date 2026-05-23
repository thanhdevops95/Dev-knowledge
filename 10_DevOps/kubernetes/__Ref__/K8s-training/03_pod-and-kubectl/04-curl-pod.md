# Bài #33 — Curl Pod (Test Networking Giữa Các Namespace)

> 🎯 Bài thực hành dùng **curl Pod** để chứng minh: **Namespace KHÔNG cô lập network mặc định** — Pod ở namespace khác có thể gọi nhau bình thường.

---

## 📋 Metadata

- **Bài số:** #33
- **Module:** 03-pod-and-kubectl
- **Cấp độ:** `INTERMEDIATE`
- **Thời lượng video gốc:** ~5 phút
- **Prerequisites:** [Bài #12 — kubectl exec](03-kubectl-exec.md), [Bài #32 — Namespace](../09-namespace/01-namespace.md)
- **Last Updated:** 09/05/2026

> ⚠️ **Bài này NÊN học SAU Bài #32 (Namespace) và Bài #30 (Services).** Nếu bạn đang theo lộ trình tuần tự, có thể skip và quay lại sau.

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Hiểu **DNS naming convention** của Service trong K8s: `<svc>.<ns>.svc.cluster.local`
- [ ] Tạo **curl Pod** debug cross-namespace networking
- [ ] Hiểu sự khác nhau giữa **Service Port** và **NodePort**
- [ ] Biết khi nào dùng cluster-internal port vs external NodePort

---

## 📚 Nội Dung

### 1. DNS Naming Convention Trong K8s

Mọi Service trong K8s đều có **tên DNS** theo công thức:

```
<service-name>.<namespace>.svc.cluster.local
```

**Phân tích:**

```
nodeport-service.namespace1.svc.cluster.local
       │              │       │       │
       │              │       │       └─ Tên cluster (mặc định: cluster.local)
       │              │       └───────── Cố định: "svc"
       │              └───────────────── Tên namespace
       └──────────────────────────────── Tên service
```

> 💡 Trong **cùng namespace**: chỉ cần dùng `<service-name>` (gọn).
> Cross namespace: cần đầy đủ `<service-name>.<namespace>` hoặc lâu hơn.

---

### 2. Service Port vs NodePort

```
┌────────────── K8s Cluster ───────────────────┐
│                                              │
│  ┌─── Namespace ns1 ───┐                     │
│  │                     │                     │
│  │   Service (8080) ←──── PORT BÊN TRONG     │
│  │     │                  (cluster-internal) │
│  │     ▼                                     │
│  │   Pod:8080                                │
│  │                                           │
│  │  Service NodePort: 32487                  │
│  │     ↑                                     │
│  │     │ PORT BÊN NGOÀI                      │
│  └─────┴─────────────────┘                   │
│        ↑                                     │
└────────┴─────────────────────────────────────┘
         │
   User bên ngoài cluster
   (truy cập qua: <node-ip>:32487)
```

| Port                      | Vai trò                | Ai dùng                |
| ------------------------- | ---------------------- | ---------------------- |
| **Service Port** (`8080`) | Port bên trong cluster | Pod gọi Pod khác       |
| **NodePort** (`32487`)    | Port public ra Node    | User bên ngoài cluster |

**Quy tắc quan trọng:** Pod ở **trong cluster** luôn dùng **Service Port** (8080), KHÔNG dùng NodePort!

---

## 💻 Hands-On / Demo

### Setup: Tạo Curl Pod

Sử dụng image `curlimages/curl` (chứa `curl`, sleep mãi mãi để Pod luôn alive).

**File `curl-pod.yaml`:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: curl-pod
spec:
  containers:
    - name: curl
      image: curlimages/curl:latest
      command: ["sleep", "36000"]
```

```bash
# Apply
kubectl apply -f curl-pod.yaml

# Verify
kubectl get pods
# NAME       READY   STATUS    RESTARTS   AGE
# curl-pod   1/1     Running   0          5s
# (sẽ ở trong namespace `default` vì không chỉ định)
```

---

### Test 1: Curl Service ở Namespace KHÁC

Giả sử bạn đã có:
- Service `nodeport-service` ở namespace `ns1` (trỏ Pod port 8080)
- Service `nodeport-service` ở namespace `ns2` (trỏ Pod port 8080)

```bash
# Chui vào curl-pod
kubectl exec -it curl-pod -- sh

# Bên trong: gọi service ở ns1
~ $ curl http://nodeport-service.ns1.svc.cluster.local:8080
# Output: HTML trả về từ Pod ở ns1

# Gọi service ở ns2
~ $ curl http://nodeport-service.ns2.svc.cluster.local:8080
# Output: HTML trả về từ Pod ở ns2

# Gọi web bên ngoài (vd: cloudflare-protected site)
~ $ curl https://viet.vn
# Output: trang chủ viet.vn
```

→ **Kết luận quan trọng:**
- ✅ Pod ở namespace `default` gọi được Service ở `ns1` và `ns2`
- ✅ Pod gọi internet được (DNS hoạt động bình thường)
- → **Namespace KHÔNG cô lập network** mặc định.

---

### Test 2: Load Balancing tự động

Service tự động cân bằng tải giữa các Pod backend:

```bash
~ $ curl http://nodeport-service.ns1.svc.cluster.local:8080
# Trả về: hostname=pod-app-79xxx

~ $ curl http://nodeport-service.ns1.svc.cluster.local:8080
# Trả về: hostname=pod-app-S4xxx   ← Pod KHÁC!

~ $ curl http://nodeport-service.ns1.svc.cluster.local:8080
# Trả về: hostname=pod-app-79xxx
```

→ Service tự **load balance** round-robin giữa 2 Pod backend.

---

### Test 3: Lưu Ý Khi Dùng NodePort Bên Trong

```bash
# ❌ KHÔNG nên dùng NodePort khi đang ở trong cluster
~ $ curl http://nodeport-service.ns1.svc.cluster.local:32487
# Có thể fail (NodePort là cho external)

# ✅ Đúng: dùng Service Port
~ $ curl http://nodeport-service.ns1.svc.cluster.local:8080
```

---

### Cleanup

```bash
# Cách 1: xóa từng resource
kubectl delete pod curl-pod
kubectl delete svc nodeport-service -n ns1
kubectl delete svc nodeport-service -n ns2

# Cách 2 (nhanh): xóa cả namespace → mọi resource trong đó tự xóa
kubectl delete namespace ns1
kubectl delete namespace ns2
```

> 💡 **Tip:** Tạo bằng Declarative (YAML) thì xóa cũng dễ:
>
> ```bash
> kubectl delete -f my-manifest.yaml
> ```

---

## ⚠️ Lưu Ý

- 🔥 **Cùng namespace**: chỉ cần `<service>` (vd: `curl http://my-svc:8080`)
- 🔥 **Khác namespace**: cần đầy đủ `<service>.<namespace>` (hoặc full FQDN)
- 🔥 **Pod gọi Pod khác**: dùng **Service Port** (cluster-internal), KHÔNG NodePort
- 🔥 **External user**: dùng **NodePort** hoặc **LoadBalancer**
- ⚠️ Namespace mặc định **không cô lập network** — cần **NetworkPolicy** để cô lập (sẽ học sau)
- ⚠️ Xóa Namespace = xóa **toàn bộ** resource trong đó (cẩn thận!)

---

## ✅ Self-Check

1. **DNS pattern đầy đủ của 1 service tên `api` ở namespace `prod` là gì?**
   <details>
   <summary>Đáp án</summary>

   ```
   api.prod.svc.cluster.local
   ```

   </details>

2. **Pod ở namespace `app` muốn gọi service `db` cùng namespace, nên dùng URL nào?**
   <details>
   <summary>Đáp án</summary>

   ```
   http://db        ← gọn nhất
   http://db.app    ← rõ ràng hơn
   http://db.app.svc.cluster.local   ← FQDN
   ```

   Cả 3 đều OK trong cùng namespace.
   </details>

3. **Pod nội cluster gọi 1 Service nên dùng Service Port (8080) hay NodePort (32487)?**
   <details>
   <summary>Đáp án</summary>
   **Service Port (8080)** — vì đang ở trong cluster.
   </details>

4. **Lệnh nào xóa toàn bộ resource trong 1 namespace?**
   <details>
   <summary>Đáp án</summary>

   ```bash
   kubectl delete namespace <ns-name>
   ```

   Mọi Pod, Service, Deployment, ConfigMap... bên trong sẽ bị xóa theo.
   </details>

5. **Mặc định, Namespace có cô lập network giữa các Pod khác namespace không?**
   <details>
   <summary>Đáp án</summary>
   **KHÔNG**. Mặc định mọi Pod gọi nhau được. Muốn cô lập → dùng **NetworkPolicy**.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #12 — kubectl exec](03-kubectl-exec.md)
- ➡️ [Module 04 — Expose Pod (NodePort)](../04-expose-pod-nodeport/README.md)
- 🏠 [Quay về index Module 03](README.md)

### Liên Quan
- [Bài #30 — Services Types](../08-services/01-services-types-ly-thuyet.md)
- [Bài #32 — Namespace](../09-namespace/01-namespace.md)

### Tài Nguyên

- 📖 [DNS for Services and Pods](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/)
- 📖 [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)
- 📺 Video gốc: `Decopy_✅ #33 Curl Pod..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Các bạn đi thi, đi làm — thấy cấu trúc service kiểu này: `<service>.<namespace>.svc.cluster.local`. `svc` là cố định, `cluster.local` là tên cluster mặc định. Cần phải nhớ!"*

> 💬 *"Khuyến nghị về mặt lâu dài: tạo tất cả tài nguyên dạng **Declarative (YAML)** — sau này xóa, sửa, version control rất tiện."*

> 💬 *"Khi delete 1 Namespace, **tất cả** tài nguyên trong đó tự động bị xóa luôn — Pod, Service, Deployment... cẩn thận!"*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
