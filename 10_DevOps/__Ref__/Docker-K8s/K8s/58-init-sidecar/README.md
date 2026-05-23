# Bài 58 — Init Container + Sidecar Pattern 🔴

> **Tiên quyết:** Hoàn thành Bài 57; hiểu rõ pod lifecycle.
> **File:** `pod-init.yaml`, `pod-sidecar.yaml`.

## Trước khi apply

Mở cả 2 file, thay `<YOUR_DOCKERHUB_USERNAME>` bằng username Docker Hub thật.

## Lệnh thủ công

### Phần A: Init Container — chạy TRƯỚC main container

```bash
# Apply (pod sẽ stuck ở Init:0/2 vì chưa có service `db`)
kubectl apply -f pod-init.yaml -n myapp-dev
kubectl get pods -n myapp-dev -w
# STATUS: Init:0/2 → Init:1/2 → PodInitializing → Running (nếu có db)

# Xem log từng init container
kubectl logs myapp-with-init -c wait-for-db -n myapp-dev
kubectl logs myapp-with-init -c run-migration -n myapp-dev

# describe để thấy phần Init Containers
kubectl describe pod myapp-with-init -n myapp-dev | grep -A 5 "Init Containers"
```

### Phần B: Sidecar — chạy song song với main

```bash
kubectl apply -f pod-sidecar.yaml -n myapp-dev
kubectl get pods -n myapp-dev
# READY 2/2 (myapp + log-shipper)

# Xem log từng container
kubectl logs myapp-with-sidecar -c myapp -n myapp-dev
kubectl logs myapp-with-sidecar -c log-shipper -n myapp-dev
```

## Kết quả mong đợi

- `myapp-with-init`: init container chạy TUẦN TỰ, mỗi cái exit 0 mới qua cái sau; main container chỉ start khi TẤT CẢ init xong.
- `myapp-with-sidecar`: pod có READY `2/2`, hai container chạy song song, share volume `emptyDir`.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| Pod stuck ở `Init:0/1` | Init container đang retry — `kubectl logs <pod> -c wait-for-db` xem nguyên nhân |
| Main container không start | Một trong các init fail; toàn bộ pod sẽ retry theo `restartPolicy` |
| `containers in spec for pod` không đủ | Tên container trong `volumeMounts` phải khớp `volumes` |

## Khi nào dùng Init vs Sidecar?

| Pattern | Mục đích | Ví dụ |
|---------|----------|-------|
| Init Container | "Chuẩn bị" — xong rồi nghỉ | Migration DB, wait-for-dependency, fetch config từ Vault, set permission |
| Sidecar | "Đồng hành" — chạy suốt với main | Log shipper, service mesh proxy (Envoy), config reloader, metric exporter |

## Câu hỏi

- Init container thất bại → main container có start không?
  *(Không. Toàn pod retry theo `restartPolicy`.)*
- Sidecar và main share gì?
  *(Network namespace — gọi nhau qua `localhost`; volume — `emptyDir` chia sẻ. Lifecycle độc lập trừ khi dùng K8s 1.29+ native sidecar.)*

## Bài kế tiếp

```bash
cd ../59-rbac
```
