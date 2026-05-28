# Bài 63 — StorageClass + Dynamic Provisioning

> **Tiên quyết:** Hoàn thành Bài 62; cluster có StorageClass (Minikube có sẵn `standard`).
> **File:** `pvc-dynamic.yaml`, `storageclass-custom.yaml`.

## Lệnh thủ công

```bash
# 1. Xem StorageClass có sẵn
kubectl get sc
# Minikube: 'standard' (default) dùng hostpath-provisioner
# Kind: 'standard' với rancher.io/local-path

# 2. Apply PVC dynamic — KHÔNG cần tạo PV trước
kubectl apply -f pvc-dynamic.yaml

# 3. Quan sát — PV được auto-tạo
kubectl get pvc -n myapp-dev
kubectl get pv         # PV mới xuất hiện
# PVC STATUS: Bound

# 4. (Optional) Apply custom StorageClass — chỉ syntax demo, provisioner cloud không chạy local
kubectl apply -f storageclass-custom.yaml
kubectl get sc

# 5. Xóa custom SC khi xong
kubectl delete -f storageclass-custom.yaml
```

## Kết quả mong đợi

- `kubectl get sc` thấy ít nhất 1 default StorageClass.
- Apply `pvc-dynamic.yaml` → PV tự tạo sau vài giây, PVC `Bound`.
- Apply custom SC (`fast-ssd`) thành công về mặt syntax.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| PVC `Pending` mãi | Không có default SC; `kubectl get sc` để xem; chọn `storageClassName:` cụ thể |
| PV không xóa khi xóa PVC | `reclaimPolicy: Retain` — admin phải xóa thủ công |
| Custom SC `fast-ssd` không tạo PV | Provisioner `kubernetes.io/aws-ebs` chỉ chạy trên AWS — đây là demo syntax |

## 3 ReclaimPolicy

| Policy | Khi xóa PVC |
|--------|-------------|
| `Delete` | PV + disk thật bị xóa |
| `Retain` | PV chuyển sang `Released`, disk được giữ (admin xóa thủ công) |
| `Recycle` | (deprecated) |

## Câu hỏi

- `volumeBindingMode: Immediate` vs `WaitForFirstConsumer`?
  *(Immediate: PV bind ngay khi PVC tạo. WaitForFirstConsumer: đợi pod schedule rồi mới bind — tốt cho topology aware.)*
- Production data quan trọng → ReclaimPolicy là gì?
  *(`Retain` — phòng khi xóa nhầm PVC vẫn còn data trên disk.)*

## Bài kế tiếp

```bash
cd ../64-kustomize
```
