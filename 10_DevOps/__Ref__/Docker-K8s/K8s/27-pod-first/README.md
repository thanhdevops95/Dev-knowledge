# Bài 27 — Pod đầu tiên

> **Tiên quyết:** namespace `myapp-dev` đã tạo (Bài 26); image `<your-username>/myapp:6.0` public trên Docker Hub.
> **File:** `pod.yaml`, `namespaces.yaml` (copy từ Bài 26).

## Trước khi apply — sửa pod.yaml

Mở `pod.yaml`, thay **`<YOUR_DOCKERHUB_USERNAME>`** bằng username Docker Hub thật.

> 💡 **`imagePullPolicy: IfNotPresent`:** Trên local cluster (Minikube/Kind/Docker Desktop), image build trên host KHÔNG có sẵn trong cluster. Nếu image chưa public hoặc cluster offline, hãy load thủ công TRƯỚC khi apply:
> ```bash
> # Minikube:
> minikube image load <YOUR_DOCKERHUB_USERNAME>/myapp:6.0
> # Kind:
> kind load docker-image <YOUR_DOCKERHUB_USERNAME>/myapp:6.0 --name myapp-cluster
> ```
> Với image public trên Docker Hub thì K8s tự pull, không cần load.

## Lệnh thủ công

```bash
# 1. Apply
kubectl apply -f namespaces.yaml    # (nếu chưa tạo namespace)
kubectl apply -f pod.yaml

# 2. Kiểm tra
kubectl get pods -n myapp-dev
kubectl get pods -n myapp-dev -o wide
kubectl describe pod myapp-pod -n myapp-dev

# 3. Test app qua port-forward
# Terminal 1:
kubectl port-forward pod/myapp-pod 8080:5000 -n myapp-dev

# Terminal 2:
curl http://localhost:8080
curl http://localhost:8080/health
curl http://localhost:8080/config
```

## Kết quả mong đợi

- `kubectl get pod myapp-pod -n myapp-dev` → STATUS `Running`, READY `1/1`.
- `curl /health` → `{"status":"ok"}`.
- `curl /config` → JSON có `APP_ENV=kubernetes`, `APP_NAME=K8s App`, `APP_VERSION=6.0` (xác nhận env vars trong `pod.yaml` được inject vào container).
- ⚠️ `curl /` → **500 Internal Server Error** là **đúng kỳ vọng** ở bài này. Trang chủ cố connect Redis nhưng Redis chưa có trong cluster (sẽ thêm ở Bài 35). Không phải lỗi cấu hình.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| `ImagePullBackOff` | Username sai HOẶC repo Docker Hub đang private — đặt lại Public. Nếu dùng image local: chạy `minikube image load <username>/myapp:6.0` |
| `ErrImagePull` | Tag sai (`:6.0` không tồn tại) hoặc image chưa load vào cluster |
| `curl /` trả 500 | **Không phải lỗi** — Redis chưa có, sẽ fix ở Bài 35. Test `/health` và `/config` để verify app hoạt động |
| `curl` timeout | Port-forward chưa chạy hoặc bị Ctrl+C |

Debug: `kubectl describe pod myapp-pod -n myapp-dev` → đọc phần **Events**.

## Câu hỏi

- Pod khác Container thế nào? *(Pod = 1 hoặc nhiều container chạy chung network/storage namespace)*
- Tại sao app chưa kết nối Redis? *(Chưa có Redis trong cluster — sẽ học ở Bài 35)*

## Bài kế tiếp

→ [Bài 28 — Pod debug](../28-pod-debug/)
