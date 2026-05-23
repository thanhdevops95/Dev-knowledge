# Module 08 — Services (2 bài)

> 🎯 Networking trong K8s — cách Pod giao tiếp với nhau và thế giới bên ngoài.

---

## 📋 Mục Tiêu Module

- ✅ Hiểu vấn đề Pod IP thay đổi
- ✅ Phân biệt 4 loại Service
- ✅ Hands-on tạo ClusterIP, NodePort, LoadBalancer
- ✅ Hiểu cơ chế DNS trong cluster

---

## 📚 Danh Sách Bài

| # | Bài | Cấp độ | Thời lượng |
|---|-----|--------|------------|
| #30 | [Services Overview (4 loại)](01-services-types-overview.md) | INTERMEDIATE | ~15' |
| #31 | [Demo Services](02-services-demo.md) | INTERMEDIATE | ~12' |

**Tổng:** ~27 phút

---

## 🗺️ Ma Trận Chọn Loại Service

```
                  ┌──── Truy cập từ đâu? ────┐
                  ▼                           ▼
            INTERNAL                      EXTERNAL
                │                            │
                │                  ┌─────────┴─────────┐
                │                  ▼                   ▼
        ┌───────┴────────┐    Có Cloud LB?       Không Cloud LB
        ▼                ▼        │                    │
   ClusterIP         ExternalName ▼                    ▼
   (default)        (CNAME ngoài) LoadBalancer    NodePort
   DB, internal API                Production    Dev/Demo
```

---

## 🔗 Navigation

- ⬅️ Module trước: [07-deployment](../07-deployment/README.md)
- ➡️ Module tiếp: [09-namespace](../09-namespace/README.md)

---

**Tác giả:** Mr.Rom
**Ngày tạo:** 09/05/2026
