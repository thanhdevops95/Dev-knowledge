# Bài 32 — ConfigMap

## Lệnh thủ công

```bash
# 1. Apply ConfigMap
kubectl apply -f configmap.yaml

# 2. Xem
kubectl get configmaps -n myapp-dev
kubectl describe configmap myapp-config -n myapp-dev
kubectl get cm myapp-config -n myapp-dev -o yaml

# 3. Update Deployment dùng ConfigMap (đã sửa sẵn trong deployment.yaml)
kubectl apply -f deployment.yaml

# 4. Restart để pod đọc env mới
kubectl rollout restart deployment/myapp-deployment -n myapp-dev
kubectl rollout status deployment/myapp-deployment -n myapp-dev

# 5. Verify env trong pod
POD=$(kubectl get pod -n myapp-dev -l app=myapp -o jsonpath='{.items[0].metadata.name}')
kubectl exec -it $POD -n myapp-dev -- env | grep APP_
```

## Kết quả mong đợi

- `env | grep APP_` trong pod thấy đủ 4 biến: APP_NAME, APP_ENV, APP_VERSION, LOG_LEVEL.

## Bài kế tiếp

```bash
cp -r ../32-configmap ../33-secret
cd ../33-secret
```
