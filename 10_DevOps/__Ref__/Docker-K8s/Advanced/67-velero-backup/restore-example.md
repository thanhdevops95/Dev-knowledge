# Kịch bản Restore (Bài 67)

Mô phỏng "disaster" rồi khôi phục từ backup `myapp-backup`.

## 1. Xác nhận backup tồn tại

```bash
velero backup get
velero backup describe myapp-backup
# Cần Phase: Completed
```

## 2. Mô phỏng disaster — xóa namespace

```bash
kubectl delete namespace myapp-dev
kubectl get ns | grep myapp-dev      # KHÔNG còn
```

## 3. Restore từ backup

```bash
velero restore create myapp-restore --from-backup myapp-backup

# Theo dõi
velero restore describe myapp-restore
velero restore logs myapp-restore
```

## 4. Verify

```bash
kubectl get ns myapp-dev             # đã xuất hiện lại
kubectl get all -n myapp-dev         # Deployment, Service, Pod đầy đủ
kubectl get pvc -n myapp-dev         # PVC restore
kubectl get configmap,secret -n myapp-dev
```

## 5. Quan sát giới hạn

- **PV data:** chỉ phục hồi nếu cluster có CSI snapshot driver (đã set `snapshotVolumes: true`) HOẶC bật Restic/Kopia. Lab cơ bản với `--use-volume-snapshots=false` chỉ phục hồi manifest PVC, dữ liệu trong PV **không có**.
- **Resource scope:** Velero backup theo namespace. Nếu app có ClusterRole/ClusterRoleBinding tham chiếu namespace bị xóa, cần backup riêng `--include-cluster-resources=true`.

## 6. Dọn dẹp test

```bash
velero restore delete myapp-restore
```

## Câu hỏi suy ngẫm

- Nếu mất cả etcd thì Velero restore có cứu được không? (gợi ý: không — Velero cần cluster mới hoạt động trước).
- Backup chéo cluster (DR sang region khác) cần gì? (gợi ý: cùng bucket S3 + Velero ở cluster đích).
