# Bài 29 — Deployment: quản lý nhiều pod

## Lệnh thủ công

```bash
# 1. Xóa pod cũ (Bài 27) — Deployment sẽ quản lý pod thay bạn
kubectl delete pod myapp-pod -n myapp-dev 2>/dev/null

# 2. Sửa deployment.yaml: thay <YOUR_DOCKERHUB_USERNAME> bằng tên thật, rồi apply
kubectl apply -f deployment.yaml

# 3. Quan sát
kubectl get deployments -n myapp-dev
kubectl get replicasets -n myapp-dev
kubectl get pods -n myapp-dev      # 3 pod tên myapp-deployment-xxxxx

# 4. Test self-healing: xóa 1 pod
POD=$(kubectl get pod -n myapp-dev -l app=myapp -o jsonpath='{.items[0].metadata.name}')
kubectl delete pod $POD -n myapp-dev
kubectl get pods -n myapp-dev      # pod mới sẽ tự được tạo

# 5. Scale lên 5
kubectl scale deployment myapp-deployment --replicas=5 -n myapp-dev
kubectl get pods -n myapp-dev

# 6. Scale xuống 3
kubectl scale deployment myapp-deployment --replicas=3 -n myapp-dev
```

## Kết quả mong đợi

- `kubectl get pods -l app=myapp -n myapp-dev` luôn có đúng số pod = `replicas`.
- Sau xóa 1 pod, chỉ vài giây sẽ có pod mới (cùng `myapp-deployment-` prefix).

## Bài kế tiếp

→ [Bài 30 — Service](../30-service/)
