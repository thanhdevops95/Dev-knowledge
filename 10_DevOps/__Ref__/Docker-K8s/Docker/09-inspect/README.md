# Bài 09 — Inspect image

> **Loại bài:** đọc metadata image.

## Lệnh thủ công

```bash
# 1. Inspect toàn bộ (JSON, rất dài)
docker inspect myapp:1.2

# 2. Lấy trường cụ thể với --format (Go template)
docker inspect --format='{{.Config.Cmd}}' myapp:1.2
docker inspect --format='{{.Config.WorkingDir}}' myapp:1.2
docker inspect --format='{{.Architecture}}' myapp:1.2
docker inspect --format='{{.Size}}' myapp:1.2

# 3. Lưu ra file để đọc bằng editor
docker inspect myapp:1.2 > myapp-info.json
wc -l myapp-info.json   # đếm dòng
```

## Kết quả mong đợi

- `.Config.Cmd` → `[python app.py]`
- `.Config.WorkingDir` → `/app`
- `.Architecture` → `arm64` hoặc `amd64` (theo máy bạn)
- `.Size` → số byte (vài trăm MB cho python:3.11-slim base)

## Câu hỏi

- Có thể biết image build từ Dockerfile như thế nào qua inspect không? *(không trực tiếp — phải xem `docker history` mới thấy command từng layer)*

## Bài kế tiếp

```bash
cp -r ../09-inspect ../10-flask-web
cd ../10-flask-web
```
