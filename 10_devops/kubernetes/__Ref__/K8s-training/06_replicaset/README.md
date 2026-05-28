# Module 06 — ReplicaSet

> **Mục đích:** Hiểu **ReplicaSet** — cơ chế K8s đảm bảo luôn có đúng N Pod chạy. Đồng thời hiểu **giới hạn** của nó để chuyển sang Deployment ở Module 07.

---

## 📋 Metadata Module

- **Số bài:** 5
- **Tổng thời lượng video:** ~22 phút
- **Cấp độ:** `INTERMEDIATE`
- **Prerequisites:** [Module 05 — YAML 101](../05-imperative-vs-declarative/README.md)

---

## 🗺️ Danh Sách Bài Học

| # | Bài Học | Mô Tả | Thời Lượng |
|---|---------|-------|------------|
| 01 | [Giới thiệu ReplicaSet](01-gioi-thieu-replicaset.md) | Khái niệm, manifest, self-healing | ~10 phút |
| 02 | [Cơ chế Labels vs Selector](02-replicaset-labels-vs-selector.md) | Demo trap: Pod ăn ké RS | ~3 phút |
| 03 | [Expose RS Imperative](03-expose-replicaset-imperative.md) | `kubectl expose rs` | ~2 phút |
| 04 | [Expose RS Declarative](04-expose-replicaset-declarative.md) | NodePort YAML, fixed nodePort | ~3 phút |
| 05 | [Edit RS & Giới thiệu Deployment](05-edit-replicaset-va-deployment.md) | Giới hạn RS, vì sao cần Deployment | ~4 phút |

---

## 🎯 Sau Module Này, Bạn Sẽ:

- ✅ Hiểu ReplicaSet đảm bảo HA bằng cơ chế self-healing
- ✅ Viết được manifest RS đầy đủ
- ✅ Hiểu **rủi ro thiết kế label đơn giản**
- ✅ Expose RS bằng cả 2 cách Imperative + Declarative
- ✅ Hiểu **vì sao production dùng Deployment** thay RS trực tiếp

---

## 🛠️ Cheat Sheet

```bash
# CRUD
kubectl apply -f rs.yaml
kubectl get rs
kubectl describe rs <name>
kubectl edit rs <name>            # Sửa replicas OK; sửa image phải xóa Pod thủ công
kubectl delete rs <name>          # Xóa cả Pod thuộc RS

# Expose
kubectl expose rs <name> --type=NodePort --port=80   # Imperative
kubectl apply -f service.yaml                         # Declarative

# Test self-healing
kubectl delete pod <pod-name>     # RS tự tạo lại
```

---

## ⚠️ Quan Trọng

> RS có nhược điểm: KHÔNG cập nhật Pod khi đổi template. Production dùng **Deployment** (Module 07).

---

## 🔗 Tiếp Theo

➡️ **[Module 07 — Deployment](../07-deployment/README.md)** (10 bài về Deployment đầy đủ)
