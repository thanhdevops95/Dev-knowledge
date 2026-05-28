# Module 09 — Namespace (2 bài)

> 🎯 Phân vùng logic trong cluster — core value của K8s.

---

## 📋 Mục Tiêu Module

- ✅ Hiểu Namespace = phân vùng logic
- ✅ Tạo + quản lý namespace
- ✅ Triển khai resource vào namespace cụ thể
- ✅ Phân biệt Cluster (vật lý) vs Namespace (logic)

---

## 📚 Danh Sách Bài

| # | Bài | Cấp độ | Thời lượng |
|---|-----|--------|------------|
| #32 | [Namespace là gì?](01-namespace.md) | INTERMEDIATE | ~13' |
| #34 | [Namespace vs Cluster](02-namespace-vs-cluster.md) | INTERMEDIATE | ~5' |

> 💡 **Bài #33 (Curl Pod)** đã được học ở [Module 03 — Bài 04](../03-pod-and-kubectl/04-curl-pod.md) (cross-namespace networking demo).

**Tổng:** ~18 phút

---

## 🗺️ Sơ Đồ

```
                      Cluster (vật lý)
                          │
               ┌──────────┼──────────┐
               ▼          ▼          ▼
            Node 1     Node 2     Node 3
               │          │          │
               └──────────┼──────────┘
                          │
        ─── Logical Layer (Namespaces) ───
                          │
        ┌─────────┬───────┼───────┬─────────┐
        ▼         ▼       ▼       ▼         ▼
       dev      prod    test   shared    customer-X
   (logic)   (logic) (logic) (logic)   (logic)
```

---

## 🔗 Navigation

- ⬅️ Module trước: [08-services](../08-services/README.md)
- ➡️ Module tiếp: [10-resource-management](../10-resource-management/README.md)

---

**Tác giả:** Mr.Rom
**Ngày tạo:** 09/05/2026
