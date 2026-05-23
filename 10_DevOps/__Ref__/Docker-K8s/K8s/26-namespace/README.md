# Bài 26 — Namespace

> **File trong folder:** `namespaces.yaml`

## Lệnh thủ công

```bash
# 1. Tạo bằng lệnh (để luyện cú pháp)
kubectl create namespace myapp-dev
kubectl create namespace myapp-staging
kubectl create namespace myapp-prod
kubectl get ns

# 2. Tạo bằng YAML (cách khuyến nghị, chuẩn GitOps)
kubectl apply -f namespaces.yaml
kubectl get ns

# 3. Set default namespace để khỏi gõ -n hoài
kubectl config set-context --current --namespace=myapp-dev
kubectl config view --minify | grep namespace
```

## Kết quả mong đợi

`kubectl get ns` thấy thêm `myapp-dev`, `myapp-staging`, `myapp-prod`.

## ⚠️ Lưu ý quan trọng

- Sau bài này có **3 namespace** mô phỏng môi trường thật: `myapp-dev` / `myapp-staging` / `myapp-prod`.
- **Từ Bài 27 trở đi series chỉ dùng `myapp-dev`** để đơn giản hoá — staging/prod tạo ra để bạn thấy pattern, không deploy gì vào.
- Nếu lỡ trộn `kubectl create` (imperative) rồi `kubectl apply -f` (declarative) trên cùng resource → sẽ thấy Warning `missing the kubectl.kubernetes.io/last-applied-configuration annotation`. Không phải lỗi, chỉ là K8s tự patch annotation để lần sau `apply` so sánh được. **Best practice:** chọn 1 style và bám theo.

## Bài kế tiếp

→ [Bài 27 — Pod đầu tiên](../27-pod-first/)
