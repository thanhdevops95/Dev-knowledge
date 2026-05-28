# Bài 40 — Helm: đóng gói app

> **Loại bài:** dùng `helm create` rồi tùy chỉnh.
> **Khác:** bài này dùng `helm` CLI **để tạo** thư mục chart, không cần tự viết từ đầu.

## Tiên quyết

```bash
helm version    # phải ra version
```

Nếu chưa cài:
```bash
# macOS
brew install helm

# Linux
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

## Lệnh thủ công

```bash
# 1. Tạo chart skeleton (Helm tự tạo cấu trúc chuẩn)
helm create myapp-chart

# 2. Sửa myapp-chart/values.yaml — xem ví dụ trong file `values-example.yaml`
# Copy nội dung sang myapp-chart/values.yaml:
cp values-example.yaml myapp-chart/values.yaml

# 3. (Tuỳ chọn) tinh chỉnh templates trong myapp-chart/templates/
# Chart mặc định Helm tạo đã chạy được với nginx; ta override values là đủ cho lab

# 4. Install
helm install myapp ./myapp-chart -n myapp-dev --create-namespace

# 5. Xem
helm list -n myapp-dev
kubectl get all -n myapp-dev -l app.kubernetes.io/instance=myapp

# 6. Upgrade — scale lên 5
helm upgrade myapp ./myapp-chart -n myapp-dev --set replicaCount=5

# 7. History & Rollback
helm history myapp -n myapp-dev
helm rollback myapp 1 -n myapp-dev

# 8. Uninstall
helm uninstall myapp -n myapp-dev
```

## Kết quả mong đợi

- `helm list` thấy release `myapp` STATUS `deployed`.
- `kubectl get pods` thấy pod tạo bởi chart.

## Bài kế tiếp

```bash
cp -r ../40-helm ../41-full-stack
cd ../41-full-stack
```
