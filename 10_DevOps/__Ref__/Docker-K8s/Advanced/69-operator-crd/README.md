# Bài 69 — Operator Pattern + CRD cơ bản

> **Mục tiêu:** hiểu cách K8s tự mở rộng — CRD (định nghĩa) + Controller (logic) = Operator.

## Tiên quyết

- Hoàn thành Bài 41.
- Đã từng dùng các CRD ở Bài 45-50, 65, 66 (Application, VirtualService, Certificate, ServiceMonitor...).

## File trong thư mục

- `crd-myapp.yaml` — CRD `myapps.example.com` (Kind `MyApp`, schema, printer columns).
- `myapp-cr.yaml` — Một instance (Custom Resource) `my-instance`.
- `operator-overview.md` — Giải thích Operator + reconcile loop (mermaid).

## Lệnh thủ công

```bash
# 1. Apply CRD
kubectl apply -f crd-myapp.yaml
kubectl get crd | grep myapps.example.com

# 2. Auto-doc do schema sinh ra
kubectl explain myapp.spec
kubectl explain myapp.spec.replicas

# 3. Tạo instance
kubectl apply -f myapp-cr.yaml

# 4. Liệt kê
kubectl get myapps                # hoặc shortname 'ma'
kubectl get myapp my-instance -o yaml

# 5. Validate schema — thử apply spec sai (replicas=0)
#    expect: lỗi validation từ API server
```

## Kết quả mong đợi

- `kubectl get crd myapps.example.com` → Established=True.
- `kubectl get myapps` → bảng có cột `Replicas`, `Image` (do `additionalPrinterColumns`).
- `kubectl explain myapp.spec` ra documentation đúng theo schema.
- Apply CR với `replicas: 0` bị reject (vì `minimum: 1`).

> ⚠️ **Lưu ý:** đến đây MỚI chỉ có CRD — chưa có Controller nào "phản ứng" với `MyApp`. Muốn tạo Deployment/Service thật, cần viết Operator (Kubebuilder hoặc kopf). Xem `operator-overview.md`.

## Câu hỏi

- CRD và Controller — cái nào "định nghĩa schema", cái nào "thực thi logic"?
- Khi nào nên viết Operator riêng vs đóng gói bằng Helm chart?

## Bài kế tiếp

Bạn đã hoàn thành chuỗi 5 bài Advanced Bonus (65–69)! Quay lại [`README.md`](../README.md) để xem lộ trình tổng kết.
