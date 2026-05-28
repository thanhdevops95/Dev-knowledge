# Bài 13 — Logs

> **Tiên quyết:** `myapp-web` đang chạy.

## Lệnh thủ công

```bash
# 1. Tạo traffic
curl http://localhost:8080
curl http://localhost:8080/health
curl http://localhost:8080/notexist

# 2. Toàn bộ log
docker logs myapp-web

# 3. Follow realtime (mở terminal khác, gọi curl, xem log update)
docker logs -f myapp-web
# Ctrl+C để thoát follow (không kill container)

# 4. 10 dòng cuối
docker logs --tail 10 myapp-web

# 5. Kèm timestamp
docker logs -t myapp-web

# 6. Trong 5 phút qua
docker logs --since 5m myapp-web
```

## Kết quả mong đợi

- Log thấy `Serving Flask app 'app'` ở đầu.
- Mỗi `curl` tạo 1 dòng `"GET / HTTP/1.1" 200 -` hoặc tương tự.
- Request `/notexist` → status `404`.

## Câu hỏi

- Log đến từ đâu? *(stdout + stderr của process PID 1)*
- App ghi vào file `/var/log/app.log` thì `docker logs` thấy? *(KHÔNG — chỉ thấy stdout/stderr; sẽ học logging file ở Bài 19)*

## Bài kế tiếp

```bash
cp -r ../13-logs ../14-cp
cd ../14-cp
```
