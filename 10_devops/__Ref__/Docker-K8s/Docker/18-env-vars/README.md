# Bài 18 — Environment Variables

> **Loại bài:** sửa app, build `myapp:3.0`.
> **Snapshot trước:** copy từ `17-stats/`.

## File thay đổi so với bài trước

| File | Thay đổi |
|------|----------|
| `myapp/app.py` | thêm `os.getenv()` cho APP_NAME, APP_ENV, APP_VERSION; thêm route `/config` |
| `myapp/Dockerfile` | thêm 3 dòng `ENV` |
| `myapp/app.env` | **MỚI** — file env mẫu |

## Lệnh thủ công

```bash
cd myapp

# 1. Build version mới
docker build -t myapp:3.0 .

# 2. Dọn container cũ rồi chạy với -e (inline env)
docker stop myapp-web 2>/dev/null; docker rm myapp-web 2>/dev/null
docker run -d -p 8080:5000 \
  -e APP_NAME="Production App" \
  -e APP_ENV="production" \
  --name myapp-web myapp:3.0

# 3. Test
curl http://localhost:8080
curl http://localhost:8080/config

# 4. Chạy lại bằng --env-file
docker stop myapp-web && docker rm myapp-web
docker run -d -p 8080:5000 --env-file app.env --name myapp-web myapp:3.0
curl http://localhost:8080/config
```

## Kết quả mong đợi

- `/config` ở bước 3 trả: `{"name":"Production App","env":"production","version":"3.0"}`.
- `/config` ở bước 4 trả: `{"name":"Staging App","env":"staging","version":"3.0-rc1"}`.

## Câu hỏi

- Thứ tự ưu tiên ENV: `-e` runtime > `--env-file` > `ENV` trong Dockerfile.
- Không hardcode password vào Dockerfile — image có thể bị đẩy lên registry public.

## Bài kế tiếp

```bash
cp -r ../18-env-vars ../19-volume
cd ../19-volume
```
