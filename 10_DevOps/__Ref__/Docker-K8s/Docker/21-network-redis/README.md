# Bài 21 — Network: Redis + app

> **Loại bài:** đại nâng cấp — thêm Redis, app `myapp:5.0`, học custom network.
> **Snapshot trước:** copy từ `20-wait/`.

## File thay đổi

| File | Thay đổi |
|------|----------|
| `myapp/app.py` | thêm import `redis`, đếm visitor — **dùng `host="redis"`** (tên service trong network) |
| `myapp/requirements.txt` | thêm `redis==5.0.1` |

> **⚠️ Lưu ý quan trọng:** trong code dùng tên `'redis'` (service name) chứ KHÔNG dùng `localhost`. Container app gọi `redis://redis:6379`.

## Lệnh thủ công

### Phần A — Khám phá network mặc định

```bash
docker network ls
docker network inspect bridge | head -30
```

### Phần B — Custom network + 2 container

```bash
cd myapp

# 1. Tạo network riêng
docker network create myapp-net

# 2. Chạy Redis trong network này
docker run -d --name redis --network myapp-net redis:alpine

# 3. Build app v5.0
docker build -t myapp:5.0 .

# 4. Dọn container cũ
docker stop myapp-web 2>/dev/null; docker rm myapp-web 2>/dev/null

# 5. Chạy app trong CÙNG network
docker run -d -p 8080:5000 \
  --name myapp-web --network myapp-net \
  myapp:5.0

# 6. Test
curl http://localhost:8080     # Visitor #1
curl http://localhost:8080     # Visitor #2
curl http://localhost:8080     # Visitor #3

# 7. Test DNS giữa container
docker exec myapp-web sh -c 'apt-get install -y iputils-ping 2>/dev/null; ping -c 2 redis 2>&1 | head'
# Hoặc đơn giản:
docker exec myapp-web getent hosts redis
```

## Kết quả mong đợi

- `curl http://localhost:8080` → `Hello! You are visitor #1`, `#2`, `#3`...
- DNS lookup `redis` từ container `myapp-web` ra IP nội bộ của container redis.

## 💡 DNS trong custom network — và liên hệ K8s

- Docker tự cấp DNS resolver bên trong **user-defined network**: container gọi nhau bằng **tên container** (hoặc **tên service** trong Compose).
- Trên default `bridge` network — cơ chế này **KHÔNG hoạt động**; phải dùng IP hoặc `--link` (đã deprecated). Đây là lý do production luôn tạo custom network.
- Khi chuyển sang K8s (xem **Bài 35** trong [`K8s/`](../../K8s/)), cơ chế tương tự nhưng FQDN đầy đủ là:

```
<service>.<namespace>.svc.cluster.local
# ví dụ: redis.myapp-dev.svc.cluster.local
```

Trong cùng namespace có thể gọi gọn `redis` (không cần `.namespace.svc.cluster.local`).

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| `ConnectionError: ... redis: Name or service not known` | Container không cùng network — kiểm tra `--network myapp-net` ở cả 2 |
| `ConnectionRefused` | Redis chưa Up — `docker logs redis` |

## Câu hỏi

- Tại sao `host='redis'`? *(Docker built-in DNS resolve tên container trong cùng user-defined network)*
- 2 container ở 2 network khác nhau có thấy nhau? *(KHÔNG — phải connect thêm: `docker network connect`)*

## Bài kế tiếp

```bash
cp -r ../21-network-redis ../22-multi-stage
cd ../22-multi-stage
```
