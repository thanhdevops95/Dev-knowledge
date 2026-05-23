# Bài #9 — NodePort: Cơ Chế Hoạt Động

> 🎯 Bài lý thuyết — hiểu **3 lớp port** (Container Port, Service Port, NodePort) trước khi hands-on ở Bài #10.

---

## 📋 Metadata

- **Bài số:** #9
- **Module:** 04-expose-pod-nodeport
- **Cấp độ:** `BEGINNER → INTERMEDIATE`
- **Thời lượng video gốc:** ~5 phút
- **Prerequisites:** [Module 03 — Pod & kubectl](../03-pod-and-kubectl/README.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Hiểu **vì sao** Pod không thể truy cập trực tiếp từ Internet
- [ ] Phân biệt **3 lớp port**: Container Port → Pod Port → Service NodePort
- [ ] Biết **2 loại Service** expose ra Internet: NodePort & LoadBalancer
- [ ] Hiểu giải port chuẩn của NodePort: **30000-32767**

---

## 📚 Nội Dung

### 1. Vấn Đề: User Bên Ngoài KHÔNG Truy Cập Được Pod

```
        🌍 Internet
              │
              ▼
    ┌─────── Node (10.10.5.8) ──────────┐
    │                                    │
    │   ┌─── Pod (10.99.9.9) ────┐      │
    │   │   Container :8080      │      │
    │   └────────────────────────┘      │
    │                                    │
    └────────────────────────────────────┘

❌ User KHÔNG thể curl http://10.99.9.9:8080
   (Pod IP là cluster-internal, không routable từ Internet)

✅ User CHỈ có thể curl đến IP của Node (10.10.5.8)
```

→ **Cần "cánh cửa"** từ Internet → Node → Pod → Container.

---

### 2. 3 Lớp Port Trong Hành Trình Network

```
                                  🌍 User
                                    │
                                    │ HTTP request
                                    ▼
       ┌────────── Node (10.10.5.8) ─────────────────────┐
       │                                                  │
       │     [3] NodePort: 30988  ◄── EXPOSE PUBLIC      │
       │            │                                     │
       │            ▼                                     │
       │   ┌── Pod (10.99.9.9) ────────────────┐         │
       │   │                                    │         │
       │   │   [2] Pod Port: 8081               │         │
       │   │            │                       │         │
       │   │            ▼                       │         │
       │   │   ┌─── Container ─────┐           │         │
       │   │   │  [1] Container    │           │         │
       │   │   │      Port: 8080    │           │         │
       │   │   └────────────────────┘           │         │
       │   └────────────────────────────────────┘         │
       └──────────────────────────────────────────────────┘
```

| Lớp     | Tên Port                        | Phạm vi         | Ai dùng                                 |
| ------- | ------------------------------- | --------------- | --------------------------------------- |
| **[1]** | **Container Port**              | 0-65535         | Code bên trong (vd: `app.listen(8080)`) |
| **[2]** | **Pod Port** (= Container Port) | 0-65535         | Pod khác trong cluster                  |
| **[3]** | **NodePort**                    | **30000-32767** | User ngoài Internet (qua Node IP)       |

> 💡 Trong `kubectl run --port=80`, port đó là **Container Port**.

---

### 3. NodePort vs LoadBalancer — 2 Cách Expose

K8s có **2 loại Service** giúp expose Pod ra Internet:

```
┌─────────────────────────────────────────────────────────────┐
│  NodePort                                                    │
│  ─ Mở port (30000-32767) trên TẤT CẢ Node                   │
│  ─ User truy cập: http://<bất-kỳ-node-IP>:<NodePort>        │
│  ─ ✅ Đơn giản, miễn phí                                    │
│  ─ ❌ Không có DNS friendly URL                             │
│  ─ ❌ Phải biết Node IP                                     │
│  ─ ❌ Mỗi Node IP = 1 endpoint riêng                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  LoadBalancer                                                │
│  ─ Cloud provider tạo 1 Load Balancer thật (vd: AWS ELB)    │
│  ─ User truy cập: http://my-app.example.com:80              │
│  ─ ✅ DNS friendly                                          │
│  ─ ✅ HA tự động, scale tự động                             │
│  ─ ❌ Tốn tiền (mỗi LB ~$20/tháng)                          │
│  ─ ❌ Chỉ chạy được trên cloud provider                     │
└─────────────────────────────────────────────────────────────┘
```

> 🎓 **Bài này tập trung vào NodePort.** LoadBalancer học sau ở Bài #30.

---

### 4. NodePort — Chi Tiết Cơ Chế

#### Single Pod, Single Node

```
User → http://10.10.5.8:30988
         │
         ▼ (kube-proxy match NodePort 30988 với Service)
       Service (cluster-internal)
         │
         ▼ (route to Pod)
       Pod 10.99.9.9:8081
         │
         ▼
       Container :8080
```

#### Multi Pod, Multi Node — Cùng NodePort, Khác IP

```
                     🌍 User
                       │
        ┌──────────────┴──────────────┐
        ▼                              ▼
   Node 1: 10.10.5.8              Node 2: 10.10.5.9
   :30988                          :30988          ← CÙNG PORT!
        │                              │
        ▼                              ▼
    Pod app-1 (NodeA)              Pod app-1 (NodeB)
    (replica 1)                    (replica 2)
```

→ **Đặc điểm:** NodePort **giống nhau trên mọi Node**, nhưng IP khác → user truy cập **bất kỳ Node nào** cũng được, kube-proxy sẽ load balance.

> ⚠️ **Khó khăn:** User phải biết IP Node. Nếu Node bị thay đổi (auto-scale tăng/giảm) → URL bị đổi → khó!

---

### 5. Vì Sao Cần LoadBalancer?

NodePort không tiện cho production:
- IP Node thay đổi khi auto-scale
- User phải nhớ IP, không có DNS đẹp
- Không có HA built-in

→ **LoadBalancer giải quyết hết:** dùng AWS ELB / GCP LB / Azure LB → 1 IP/DNS cố định, cluster sau đó tự định tuyến.

```
User → my-app.example.com (DNS)
         │
         ▼
       AWS ELB (managed by AWS)
         │
         ▼ Tự động phân phối tải
   ┌─────┴─────┐
   ▼           ▼
Node 1     Node 2
:30988     :30988
   │           │
   ▼           ▼
Pod app-1  Pod app-1
```

> 💰 **Chi phí:** Mỗi LB tốn ~$15-25/tháng tùy cloud → production thường gom nhiều app vào **1 Ingress** (sẽ học sau).

---

## ⚠️ Lưu Ý

- 🔥 **NodePort range bắt buộc: 30000-32767** (không thể dùng 80/443 trực tiếp)
- 🔥 NodePort mở trên **TẤT CẢ Node** dù Pod chỉ chạy 1 Node
- 🔥 NodePort thường dùng cho **dev/test** hoặc **internal**, hiếm cho public production
- ⚠️ Khi Node bị thay (auto-scale), IP thay đổi → URL gãy
- ✅ Production: dùng **LoadBalancer + Ingress** thay NodePort

---

## ✅ Self-Check

1. **Có 3 lớp port nào?**
   <details>
   <summary>Đáp án</summary>
   1. **Container Port** — port code lắng nghe (vd: 8080)
   2. **Pod Port** — thường = Container Port
   3. **NodePort** — port public ra ngoài (30000-32767)
   </details>

2. **Vì sao user không gọi trực tiếp Pod IP từ Internet được?**
   <details>
   <summary>Đáp án</summary>
   Pod IP là **cluster-internal**, không routable từ ngoài Internet. User chỉ tới được Node IP.
   </details>

3. **Range chuẩn của NodePort?**
   <details>
   <summary>Đáp án</summary>
   **30000-32767** (mặc định K8s).
   </details>

4. **2 loại Service nào expose Pod ra Internet?**
   <details>
   <summary>Đáp án</summary>
   **NodePort** và **LoadBalancer**.
   </details>

5. **Cluster có 3 Node, NodePort là 30988. User gọi vào Node nào cũng được?**
   <details>
   <summary>Đáp án</summary>
   **Đúng** — NodePort mở trên tất cả Node. kube-proxy sẽ tự route tới Pod thực sự (kể cả Pod ở Node khác).
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Module 03 — Pod & kubectl](../03-pod-and-kubectl/README.md)
- ➡️ [Bài #10 — NodePort Hands-On](02-nodeport-service-expose-pod.md)
- 🏠 [Quay về index Module 04](README.md)

### Tài Nguyên

- 📖 [Service Types](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types)
- 📖 [NodePort range config](https://kubernetes.io/docs/reference/command-line-tools-reference/kube-apiserver/)
- 📺 Video gốc: `Decopy_✅ #9 _ NodePort _ Cách Hoạt Động..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"User không thể chui vào trong Pod được, chỉ có thể truy cập IP của Node — vì Node bản chất là 1 con máy chủ bình thường."*

> 💬 *"NodePort sinh ra port ngẫu nhiên trong giải 30000-32767. Muốn chỉ định port cụ thể? Phải dùng Declarative (YAML) — sẽ học sau."*

> 💬 *"Nếu muốn user gọi qua DNS đẹp, không nhớ IP, có HA — phải dùng LoadBalancer. Nó hoạt động dựa vào công cụ LB của cloud provider (AWS ELB...)."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
