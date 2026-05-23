# Module 05 — Imperative vs Declarative + YAML 101

> **Mục đích:** Chuyển từ "gõ command" sang "viết YAML" — bước ngoặt từ amateur sang pro.

---

## 📋 Metadata Module

- **Số bài:** 2
- **Tổng thời lượng video:** ~13 phút
- **Cấp độ:** `INTERMEDIATE`
- **Prerequisites:** [Module 04 — NodePort](../04-expose-pod-nodeport/README.md)

---

## 🗺️ Danh Sách Bài Học

| # | Bài Học | Mô Tả | Thời Lượng |
|---|---------|-------|------------|
| 01 | [Imperative vs Declarative](01-imperative-vs-declarative.md) | Khái niệm, so sánh, vì sao Production cần Declarative | ~7 phút |
| 02 | [YAML Manifest 101](02-yaml-manifest-101.md) | Syntax YAML, 4 phần manifest, multi-line string | ~6 phút |

---

## 🎯 Sau Module Này, Bạn Sẽ:

- ✅ Phân biệt 2 cách quản lý K8s resource
- ✅ Hiểu vì sao Declarative là **best practice**
- ✅ Viết được manifest Pod đầy đủ
- ✅ Dùng `kubectl apply -f` thay vì `kubectl run`
- ✅ Generate YAML từ Imperative bằng `--dry-run=client -o yaml`

---

## 🛠️ Cheat Sheet

```bash
# Tạo từ YAML
kubectl apply -f manifest.yaml
kubectl apply -f manifests/         # Apply cả thư mục

# Generate YAML mẫu
kubectl run pod --image=nginx --dry-run=client -o yaml > pod.yaml
kubectl create deployment app --image=nginx --dry-run=client -o yaml > deployment.yaml

# Validate YAML
kubectl apply -f manifest.yaml --dry-run=client

# Xóa
kubectl delete -f manifest.yaml
```

---

## 🔗 Tiếp Theo

➡️ **[Module 06 — ReplicaSet](../06-replicaset/README.md)** (Đảm bảo số lượng Pod luôn đúng spec)
