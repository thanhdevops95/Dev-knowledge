# Bài #30 — Services: ClusterIP vs NodePort vs LoadBalancer vs ExternalName

> 🎯 **Bài lý thuyết quan trọng nhất** về networking trong K8s.

---

## 📋 Metadata

- **Bài số:** #30
- **Module:** 08-services
- **Cấp độ:** `INTERMEDIATE` → `ADVANCED`
- **Thời lượng video gốc:** ~15 phút
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

- [ ] Hiểu **vấn đề** Service giải quyết (Pod IP thay đổi liên tục)
- [ ] Phân biệt **4 loại** Service: ClusterIP, NodePort, LoadBalancer, ExternalName
- [ ] Hiểu cơ chế giao tiếp giữa các Pod / container
- [ ] Biết khi nào dùng loại nào

---

## 📚 Nội Dung

### 1. Vấn Đề: Pod IP Thay Đổi

```
Pod1 IP: 10.10.1.5    ← chết, restart
Pod1 IP: 10.10.1.99   ← IP mới!

App khác đang gọi 10.10.1.5 → ❌ FAIL
```

**Pod IP là ephemeral** (tạm thời). Đặc biệt khi scale:

```
Replica = 3:  Pod-A (10.10.1.5), Pod-B (10.10.1.6), Pod-C (10.10.1.7)
Scale → 5:    Pod-A, Pod-B, Pod-C, Pod-D (10.10.1.10), Pod-E (10.10.1.11)
Scale → 2:    Pod-A bị xóa, IP khác nhau
```

→ Cần **địa chỉ ổn định** + **load-balance** giữa Pods.

---

### 2. Giải Pháp: Service

```
                    ┌──────── Service "app1-svc" ────────┐
                    │   ClusterIP: 10.96.10.8 (cố định)  │
                    │   Selector: app=app1               │
                    └────────────────┬───────────────────┘
                                     │
              ┌──────────────────────┼─────────────────────┐
              ▼                      ▼                     ▼
        Pod-A (10.10.1.5)    Pod-B (10.10.1.6)      Pod-C (10.10.1.7)
        label app=app1       label app=app1         label app=app1
```

**Đặc điểm:**

- 🔥 IP của Service **cố định cho đến khi xóa**
- 🔥 Tự động **load-balance** giữa các Pod khớp selector
- 🔥 K8s `kube-proxy` quản lý routing
- 🔥 K8s `CoreDNS` cho phép gọi qua **DNS name** (không cần nhớ IP)

---

### 3. Bốn Loại Service

```
┌──────────────────────┬────────────┬───────────────────────────────────┐
│ Type                 │ Truy cập   │ Use case                           │
├──────────────────────┼────────────┼───────────────────────────────────┤
│ ClusterIP (default)  │ Internal   │ DB, internal microservices         │
│ NodePort             │ External   │ Dev / Demo / không có cloud LB     │
│ LoadBalancer         │ External   │ Production (cần Cloud Provider)    │
│ ExternalName         │ Internal   │ Trỏ đến DNS bên ngoài cluster      │
└──────────────────────┴────────────┴───────────────────────────────────┘
```

---

### 4. ClusterIP — Mặc Định, Internal

```
                 [User External]  ❌ KHÔNG truy cập được
                        │
                        ✗
              ┌─────────────────┐
              │   ClusterIP     │  10.96.10.8
              │   "psql-svc"    │
              └────────┬────────┘
                       │
              ┌────────┼────────┐
              ▼                 ▼
         Pod psql-1        Pod psql-2
```

**Sử dụng:**

- Database (PostgreSQL, MySQL, Redis, MongoDB...)
- Internal API mà không expose ra ngoài
- Microservices giao tiếp với nhau

---

### 5. NodePort — Public Qua Port Trên Node

```
      [User External]
            │
            │ http://<NodeIP>:31234
            ▼
      ┌──────────┐  ┌──────────┐
      │ Node1    │  │ Node2    │
      │ port:    │  │ port:    │
      │  31234   │  │  31234   │
      └────┬─────┘  └────┬─────┘
           ▼              ▼
        kube-proxy   kube-proxy
              │       │
              ▼       ▼
       ┌──── Service "app-svc" ────┐
       │  ClusterIP + NodePort      │
       └────────┬───────────────────┘
                │
            Pod-A, Pod-B
```

**Đặc điểm:**

- ⚠️ Port nằm trong **30000-32767**
- ⚠️ Truy cập qua IP của **bất kỳ Node nào** (kube-proxy tự routing)
- ⚠️ User phải nhớ IP Node + port — **KHÔNG nice**
- 💡 Phù hợp dev/demo, không production

---

### 6. LoadBalancer — Public Qua Cloud LB

```
           [User External]
                  │
                  │ http://app.example.com  (DNS đẹp)
                  ▼
            ┌──────────────┐
            │  Cloud LB    │  (AWS ELB, GCP LB, Azure LB)
            │  ALB / NLB   │
            └──────┬───────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
     Node1     Node2      Node3
        ↓        ↓          ↓
        Pod-A   Pod-B     Pod-C
```

**Đặc điểm:**

- 🔥 Yêu cầu **Cloud Provider** (AWS / GCP / Azure / DigitalOcean...)
- 🔥 Tự động cấp **Public IP / DNS** đẹp
- 🔥 **Production standard** cho expose service ra ngoài
- ⚠️ Mỗi LB tốn tiền — gom dùng **Ingress** thay thế

> 💡 Trên **Minikube/Kind** → LoadBalancer pending vì không có cloud provider. Phải dùng `minikube tunnel` hoặc `MetalLB`.

---

### 7. ExternalName — Trỏ Đến DNS Bên Ngoài

```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: db.production.example.com
```

→ App gọi `external-db.default.svc.cluster.local` → CNAME đến `db.production.example.com`.

**Use case:** App in-cluster cần kết nối DB **bên ngoài cluster** mà không hard-code DNS.

---

### 8. Cơ Chế Giao Tiếp Giữa Các Container

**Trong cùng 1 Pod:**

```
Pod (10.10.1.5)
├─ Container A — port 8080
└─ Container B — port 8081

A gọi B: http://localhost:8081
B gọi A: http://localhost:8080
```

**Khác Pod (cùng Node hoặc khác Node):**

```
Pod-1 (10.10.1.5)  →  Pod-2 (10.10.1.6, port 8085)
Cách 1 (xấu): http://10.10.1.6:8085   (IP đổi → fail)
Cách 2 (tốt): http://my-service:8085  (qua Service + DNS)
```

→ **kube-proxy + CoreDNS** chạy trên mỗi Node để giải quyết DNS.

---

## ⚠️ Lưu Ý

- 🔥 **Service ≠ Deployment.** Deployment tạo Pod, Service expose Pod.
- 🔥 **Service IP ổn định** suốt đời (đến khi xóa Service)
- 💡 Trong cluster: gọi qua DNS `<service>.<namespace>.svc.cluster.local`
- ⚠️ Phải có `selector` khớp `labels` của Pod để Service phát hiện được Pod

---

## ✅ Self-Check

1. **Tại sao cần Service?**
   <details>
   <summary>Đáp án</summary>
   Vì Pod IP thay đổi liên tục (restart/scale). Service cung cấp địa chỉ ổn định + load-balance.
   </details>

2. **4 loại Service?**
   <details>
   <summary>Đáp án</summary>
   ClusterIP (default, internal), NodePort (external port 30000-32767), LoadBalancer (cloud LB), ExternalName (CNAME).
   </details>

3. **Loại nào dùng cho database?**
   <details>
   <summary>Đáp án</summary>
   `ClusterIP` — không cần expose DB ra Internet.
   </details>

4. **Cùng 1 Pod, 2 container gọi nhau như thế nào?**
   <details>
   <summary>Đáp án</summary>
   Qua `localhost:<port>`. Lưu ý 2 container PHẢI dùng port khác nhau.
   </details>

---

## 🔗 Liên Kết

- ⬅️ [Module 07 — Deployment](../07-deployment/README.md)
- ➡️ [Bài #31 — Demo Services](02-services-demo.md)

### Tài Nguyên

- 📖 [Service Concept](https://kubernetes.io/docs/concepts/services-networking/service/)

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Service là khái niệm rất quan trọng khi các bạn xây dựng hệ thống ở quy mô thực tế."*

---

**Tác giả:** Mr.Rom
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
