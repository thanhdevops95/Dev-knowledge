# Module 04 — Expose Pod với NodePort

> **Mục đích:** Mở Pod ra ngoài Internet (hoặc nội bộ) — qua khái niệm **Service** loại **NodePort**.

---

## 📋 Metadata Module

- **Số bài:** 2
- **Tổng thời lượng video:** ~12 phút
- **Cấp độ:** `BEGINNER → INTERMEDIATE`
- **Prerequisites:** [Module 03 — Pod & kubectl](../03-pod-and-kubectl/README.md)

---

## 🗺️ Danh Sách Bài Học

| # | Bài Học | Mô Tả | Thời Lượng |
|---|---------|-------|------------|
| 01 | [NodePort: Cơ chế hoạt động](01-nodeport-co-che-hoat-dong.md) | 3 lớp port, NodePort vs LoadBalancer | ~5 phút |
| 02 | [NodePort Service Hands-On](02-nodeport-service-expose-pod.md) | `kubectl expose`, port/targetPort/nodePort | ~7 phút |

---

## 🎯 Sau Module Này, Bạn Sẽ:

- ✅ Hiểu **3 lớp port**: Container Port → Pod Port → NodePort
- ✅ Phân biệt **NodePort** (30000-32767) vs **LoadBalancer**
- ✅ Tạo NodePort Service bằng `kubectl expose`
- ✅ Truy cập Pod qua URL `http://<node-ip>:<nodeport>`

---

## 🔗 Tiếp Theo

➡️ **[Module 05 — Imperative vs Declarative](../05-imperative-vs-declarative/README.md)** (Học cách dùng YAML manifest — chuyên nghiệp hơn)
