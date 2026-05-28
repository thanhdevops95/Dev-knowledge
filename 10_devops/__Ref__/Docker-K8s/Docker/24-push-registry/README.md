# Bài 24 — Push image lên Docker Hub

> **Loại bài:** image cuối Docker — chuẩn bị cho phần Kubernetes.
> **Snapshot trước:** copy từ `23-compose/`.

## Tiên quyết

- Đã `docker login` thành công.
- Có image `myapp:6.0` local (build ở Bài 23).
- Biết username Docker Hub của mình (gọi tắt `<your-username>` bên dưới — **thay bằng tên thật**).

## Lệnh thủ công

```bash
# 1. (Nếu chưa) đăng nhập
docker login
# Nhập username + password (hoặc access token)

# 2. Tag image theo format <username>/<repo>:<tag>
docker tag myapp:6.0 <your-username>/myapp:6.0
docker tag myapp:6.0 <your-username>/myapp:latest

# 3. Push
docker push <your-username>/myapp:6.0
docker push <your-username>/myapp:latest

# 4. (tùy chọn) Xóa image local rồi pull lại
docker rmi <your-username>/myapp:6.0
docker pull <your-username>/myapp:6.0
```

## Kết quả mong đợi

- `docker push` upload từng layer (lần đầu chậm, lần sau nhanh do shared layer).
- Mở https://hub.docker.com/r/<your-username>/myapp thấy 2 tag.
- Sau khi xóa rồi pull → image trở lại local.

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| `denied: requested access to the resource is denied` | Chưa login HOẶC tag sai username |
| `repository does not exist` | Bình thường ở lần push đầu (sẽ tự tạo) |
| Tag image lệch giữa kiến trúc CPU | Docker Desktop trên Apple Silicon push arm64 — K8s amd64 sẽ không chạy được. Dùng `docker buildx build --platform linux/amd64,linux/arm64 ...` để build multi-arch |

## Câu hỏi

- Sao push lần 2 cùng image nhanh? *(layer đã có trên hub, chỉ push manifest)*
- Sau push, ai có thể `pull`? *(public repo: ai cũng được; private: chỉ user có quyền)*

## ⚠️ Yêu cầu cho phần Kubernetes

**Repo Docker Hub phải PUBLIC** để K8s pull được mà không cần `imagePullSecrets`. Vào Docker Hub UI → repo `myapp` → Settings → Make Public.

## Hoàn thành Phần Docker

Bạn đã có:
- 24 thư mục bài tập với source và checklist
- Image cuối: `myapp:6.0` (local) và `<your-username>/myapp:6.0` (Docker Hub)
- Stack chạy được trên Compose

**Tiếp theo:** [K8s/](../../K8s/) — bắt đầu từ Bài 25.
