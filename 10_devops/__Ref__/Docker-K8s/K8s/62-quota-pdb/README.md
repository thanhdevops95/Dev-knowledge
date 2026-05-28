# Bài 62 — ResourceQuota + LimitRange + PodDisruptionBudget 🔴

> **Tiên quyết:** Hoàn thành Bài 61; deployment myapp đang chạy 2+ replica để test PDB.
> **File:** `resourcequota.yaml`, `limitrange.yaml`, `pdb.yaml`.

## Lệnh thủ công

### Phần A: ResourceQuota — giới hạn ở namespace

```bash
kubectl apply -f resourcequota.yaml

# Xem quota
kubectl get resourcequota -n myapp-dev
kubectl describe resourcequota myapp-quota -n myapp-dev
# Thấy cột Used / Hard
```

### Phần B: LimitRange — default cho pod chưa khai báo

```bash
kubectl apply -f limitrange.yaml

# Test: tạo pod KHÔNG khai resources
kubectl run no-res --image=busybox:1.36 -n myapp-dev --restart=Never -- sleep 3600

# Xem pod đã nhận default
kubectl describe pod no-res -n myapp-dev | grep -A 5 "Limits\|Requests"
```

### Phần C: PodDisruptionBudget

```bash
kubectl apply -f pdb.yaml

# Xem PDB
kubectl get pdb -n myapp-dev

# Test: drain node trong khi PDB block
# (cần cluster nhiều node; nếu Minikube single-node thì skip)
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data
# K8s sẽ chờ cho đến khi có pod khác lên thay
```

## Kết quả mong đợi

- Apply Deployment vượt quota → fail với error rõ ràng.
- Pod KHÔNG khai resources tự nhận `default` từ LimitRange.
- `kubectl drain` block khi violation PDB.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| Deployment apply OK nhưng 0 pod | ResourceQuota đầy — `kubectl describe resourcequota` |
| LimitRange không apply default | LimitRange phải tạo TRƯỚC pod; xóa pod cũ rồi tạo lại |
| PDB vô hiệu | PDB chỉ block voluntary disruption (drain). Hardware failure / pod crash KHÔNG bị block. |

## Câu hỏi

- ResourceQuota có check `requests` hay `limits`?
  *(Cả hai — `requests.cpu`/`requests.memory` và `limits.cpu`/`limits.memory` đều khai báo được.)*
- PDB chỉ hoạt động với voluntary disruption (drain) hay cả hardware failure?
  *(Chỉ voluntary disruption. Hardware failure → pod chết ngay, K8s không can thiệp được.)*

## Bài kế tiếp

```bash
cd ../63-storageclass
```
