# Bài 10 — Flask Web Server, daemon + port mapping

> **Loại bài:** đại tu app thành Flask, build image `myapp:2.0`, chạy background.
> **Snapshot trước:** copy từ `09-inspect/`, sửa `app.py`, thêm `requirements.txt`, sửa `Dockerfile`.

## File trong thư mục này

```
10-flask-web/
├── README.md
├── KET-QUA.md
└── myapp/
    ├── app.py              ← Flask v2.0 (đổi từ print → web)
    ├── requirements.txt    ← MỚI: flask==3.0.0
    └── Dockerfile          ← thêm RUN pip install, EXPOSE 5000
```

## Lệnh thủ công

```bash
cd myapp

# 1. Build image với tag 2.0
docker build -t myapp:2.0 .

# 2. Chạy background, map port 8080 (host) → 5000 (container)
docker run -d -p 8080:5000 --name myapp-web myapp:2.0

# 3. Xem container đang chạy
docker ps

# 4. Test endpoints
curl http://localhost:8080
curl http://localhost:8080/health

# 5. Xem logs
docker logs myapp-web
```

## Kết quả mong đợi

- `docker ps` thấy `myapp-web` STATUS `Up X seconds`, PORTS `0.0.0.0:8080->5000/tcp`.
- `curl http://localhost:8080` trả: `Hello from MyApp v2.0 - 2026-...`.
- `curl http://localhost:8080/health` trả JSON: `{"status":"ok"}`.

## Tiêu chí hoàn thành

- [ ] `requirements.txt` có `flask==3.0.0`
- [ ] Dockerfile có `RUN pip install --no-cache-dir -r requirements.txt`
- [ ] Dockerfile có `EXPOSE 5000`
- [ ] Container chạy `-d`, map đúng port
- [ ] 2 endpoint HTTP hoạt động

## Câu hỏi

- `-d` làm gì? *(detach — chạy nền, trả về prompt ngay)*
- Cú pháp `-p 8080:5000` ? *(HOST:CONTAINER — port 8080 máy host forward vào port 5000 trong container)*
- `EXPOSE 5000` có tác dụng? *(chỉ documentation; KHÔNG tự động map port — phải dùng `-p` khi run)*

## Bài kế tiếp

```bash
cp -r ../10-flask-web ../11-lifecycle
cd ../11-lifecycle
```

Bài 11 sẽ dùng chính container `myapp-web` này để học `stop/start/restart/pause/kill`.
