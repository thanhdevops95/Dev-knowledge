# Bài 23 — Docker Compose: orchestrate multi-container

> **Loại bài:** dùng 1 file YAML chạy toàn stack `web + redis + postgres`.
> **Snapshot trước:** copy từ `22-multi-stage/`.
> **Tag image:** `myapp:6.0`.

## File mới

`myapp/docker-compose.yml` — đặt **trong thư mục `myapp/`**.

## Lệnh thủ công

```bash
cd myapp

# 1. Dọn container thủ công của các bài trước (nếu còn)
docker stop myapp-web redis 2>/dev/null
docker rm myapp-web redis 2>/dev/null

# 2. Khởi động toàn stack
docker compose up -d

# 3. Xem trạng thái
docker compose ps

# 4. Test endpoints
curl http://localhost:8080
curl http://localhost:8080
curl http://localhost:8080

# 5. Theo dõi log web realtime
docker compose logs -f web
# Ctrl+C thoát

# 6. Scale service web lên 3 instance
docker compose up -d --scale web=3
docker compose ps     # thấy 3 myapp-web-* container

# Lưu ý: chỉ 1 host port 8080 → nếu scale, port phải ephemeral
# Compose v2 sẽ báo lỗi "port already in use" với scale + fixed port
# Để demo scale, bỏ "ports" hoặc dùng nginx reverse proxy

# 7. Dừng & xóa volume
docker compose down -v
```

## Kết quả mong đợi

- `docker compose ps` thấy 3 service: `web`, `redis`, `db` — STATE `Up`.
- `curl localhost:8080` đếm visitor tăng dần.
- `docker compose down -v` xóa cả container, network và volume.

## ⚠️ Lưu ý quan trọng

1. **`depends_on` tự thân chỉ đợi container START, KHÔNG đợi service READY.** File `docker-compose.yml` ở đây đã kết hợp `healthcheck` + `condition: service_healthy` cho `redis` và `db`, nên service `web` chỉ start khi cả hai phụ thuộc đã sẵn sàng nhận connection.
2. **Compose V2** (Docker Desktop hiện tại) đã **bỏ field `version:`** — không cần khai báo. Lệnh chính thức là `docker compose` (có space). `docker-compose` (legacy V1, có gạch ngang) chỉ còn để backward compatible.
3. Image `myapp:6.0` được build tự động khi có `build: .` trong service `web`.
4. Healthcheck dùng `redis-cli ping` và `pg_isready` — đây là 2 lệnh tích hợp sẵn trong image official, không cần cài thêm.

## Câu hỏi

- `depends_on` đảm bảo gì? *(thứ tự **start**, không phải **ready**)*
- Ưu điểm so với `docker run` từng container? *(1 lệnh, network/volume tự tạo, dễ tear down)*

## Bài kế tiếp

```bash
cp -r ../23-compose ../24-push-registry
cd ../24-push-registry
```
