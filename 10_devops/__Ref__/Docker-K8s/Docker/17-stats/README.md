# Bài 17 — Stats, Top, Inspect Container

> **Tiên quyết:** `myapp-web` đang chạy.

## Lệnh thủ công

```bash
# 1. Realtime tài nguyên (CPU, MEM, NET, BLOCK)
docker stats myapp-web
# Ctrl+C thoát

# 2. Snapshot 1 lần
docker stats --no-stream myapp-web

# 3. Process bên trong container
docker top myapp-web

# 4. Inspect container (khác inspect image)
docker inspect myapp-web | head -50
# IP — field .NetworkSettings.IPAddress (legacy) thường RỖNG trên Docker mới.
# Dùng range để in IP của mọi network container join:
docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' myapp-web
docker inspect --format='{{.State.Status}}' myapp-web
docker inspect --format='{{.HostConfig.PortBindings}}' myapp-web
```

> 💡 `.NetworkSettings.IPAddress` chỉ có giá trị khi container chạy trên **default bridge**. Trên custom network (kể cả Compose) → IP nằm trong `.NetworkSettings.Networks.<name>.IPAddress`.

## Kết quả mong đợi

- `docker stats` ra bảng realtime, app idle thường CPU < 1%, MEM ~30MB.
- `docker top` thấy `python app.py`.
- `.State.Status` → `running`.
- `.HostConfig.PortBindings` → `map[5000/tcp:[{ 8080}]]`.
- IP qua `range .NetworkSettings.Networks` → ví dụ `172.17.0.2`.

## Bài kế tiếp

```bash
cp -r ../17-stats ../18-env-vars
cd ../18-env-vars
```

Bài 18 sẽ **sửa `app.py` và `Dockerfile`** — thêm ENV, build `myapp:3.0`.
