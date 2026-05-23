# Bài 34 — PV & PVC

> ⚠️ **`hostPath` chỉ chạy trên single-node cluster** (Minikube, Kind 1 node, Docker Desktop). Trên cluster thật nhiều node, pod có thể bị schedule sang node khác → data biến mất. Production phải dùng **StorageClass + Dynamic Provisioning** (EBS/GCEPD/Azure Disk/Ceph/Longhorn...). Học sâu ở **Bài 63 (Bonus) — `K8s/63-storageclass/`**.

## Lệnh thủ công

```bash
# 1. Apply PV trước (cluster-scoped)
kubectl apply -f pv.yaml

# 2. Apply PVC (namespace-scoped)
kubectl apply -f pvc.yaml

# 3. Xem trạng thái — PVC phải `Bound`
kubectl get pv
kubectl get pvc -n myapp-dev

# 4. Mount vào deployment
kubectl apply -f deployment.yaml
kubectl rollout restart deployment/myapp-deployment -n myapp-dev

# 5. Verify mount
POD=$(kubectl get pod -n myapp-dev -l app=myapp -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD -n myapp-dev -- ls -la /app/logs
kubectl exec -it $POD -n myapp-dev -- df -h | grep logs
```

## Kết quả mong đợi

- PVC STATUS `Bound`.
- Trong pod, `/app/logs` là mount point khác filesystem chính.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| PVC `Pending` mãi | Cluster không có default StorageClass; với Minikube `minikube addons enable storage-provisioner` đã enable mặc định |

## Bài kế tiếp

```bash
cp -r ../34-pv-pvc ../35-redis-on-k8s
cd ../35-redis-on-k8s
```
