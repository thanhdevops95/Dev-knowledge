# Bài 39 — StatefulSet

> **Khái niệm:** giống Deployment nhưng pod có **identity ổn định** (tên `redis-cluster-0`, `-1`, `-2`) và mỗi pod có **PVC riêng**.

## Lệnh thủ công

```bash
kubectl apply -f redis-headless.yaml
kubectl apply -f redis-statefulset.yaml

# Đợi pod ready
kubectl rollout status statefulset/redis-cluster -n myapp-dev

# Xem
kubectl get statefulsets -n myapp-dev
kubectl get pods -n myapp-dev | grep redis-cluster
kubectl get pvc -n myapp-dev      # Mỗi pod có PVC riêng

# Pod xóa rồi tạo lại — tên VẪN giữ
kubectl delete pod redis-cluster-0 -n myapp-dev
kubectl get pods -n myapp-dev -w   # Ctrl+C khi thấy redis-cluster-0 quay lại
```

## Kết quả mong đợi

- 3 pod: `redis-cluster-0`, `redis-cluster-1`, `redis-cluster-2`.
- 3 PVC: `data-redis-cluster-0`, `data-redis-cluster-1`, `data-redis-cluster-2`.
- Tên + PVC ổn định qua restart.

## Câu hỏi

- StatefulSet khác Deployment? *(identity ổn định, ordered start/stop, storage gắn liền với pod)*
- Tại sao cần Headless Service? *(`clusterIP: None` — DNS trả về IP từng pod thay vì 1 IP service; cần cho cluster mode)*

## Bài kế tiếp

```bash
cp -r ../39-statefulset ../40-helm
cd ../40-helm
```
