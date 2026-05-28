# Bài 64 — Kustomize cơ bản 🔴

> **Tiên quyết:** Hoàn thành Bài 63; `kubectl` v1.14+ có built-in Kustomize (hoặc cài `kustomize` standalone).
> **Cấu trúc:** `base/` + `overlays/dev/` + `overlays/prod/`.

## Trước khi apply

Mở `base/deployment.yaml` và `overlays/prod/kustomization.yaml`, thay `<YOUR_DOCKERHUB_USERNAME>` bằng username Docker Hub thật.

## Lệnh thủ công

### Render — xem output trước khi apply

```bash
# Render base (chưa có patch)
kubectl kustomize base/

# Render overlay dev (replicas=1, namespace=myapp-dev)
kubectl kustomize overlays/dev/

# Render overlay prod (replicas=5, namePrefix=prod-, namespace=myapp-prod)
kubectl kustomize overlays/prod/
```

### Apply

```bash
# Apply overlay dev
kubectl apply -k overlays/dev/

# Apply overlay prod
kubectl apply -k overlays/prod/

# Xoá
kubectl delete -k overlays/dev/
kubectl delete -k overlays/prod/
```

## Kết quả mong đợi

- `kubectl kustomize overlays/dev/` render output có `namespace: myapp-dev`, `replicas: 1`.
- `kubectl kustomize overlays/prod/` render output có `namePrefix: prod-`, `namespace: myapp-prod`, `replicas: 5`.
- Apply `overlays/prod/` tạo Deployment `prod-myapp-deployment` trong `myapp-prod`.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| `accumulating resources: ...` | Đường dẫn `resources:` sai (relative path); kiểm tra `../../base` |
| Patch không apply | `patches[].path` không tồn tại hoặc tên resource trong patch khác với base |
| `command "kustomize" not found` | Dùng `kubectl kustomize` thay vì binary `kustomize` standalone |

## So sánh Kustomize vs Helm

| Tiêu chí | Kustomize | Helm |
|----------|-----------|------|
| Cú pháp | YAML thuần + patch | Go template trong YAML |
| Logic phức tạp | ❌ (cố tình giới hạn) | ✅ (if/range/functions) |
| Built-in `kubectl` | ✅ (`-k`) | ❌ (cần `helm` binary) |
| Package & version | ❌ | ✅ |
| Phù hợp khi | Cấu hình app riêng | Đóng gói chart phân phối |

## Câu hỏi

- Khi nào pick Kustomize, khi nào pick Helm?
  *(Kustomize: cấu hình app riêng cho nhiều env. Helm: đóng gói phân phối cho người khác cài.)*
- Có thể dùng cả hai?
  *(Có — Helm chart từ vendor + Kustomize patch để override nhẹ. Pattern `helmCharts:` trong kustomization.yaml.)*

## Bài kế tiếp

```bash
cd ../../Advanced
```
