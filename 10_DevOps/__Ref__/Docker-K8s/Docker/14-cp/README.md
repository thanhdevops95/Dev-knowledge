# Bài 14 — Copy file giữa host và container

> **Tiên quyết:** `myapp-web` đang chạy.

## Lệnh thủ công

```bash
# 1. Copy file từ container ra host
docker cp myapp-web:/app/app.py ./app-backup.py
ls -la app-backup.py
cat app-backup.py | head -5

# 2. Tạo file ở host, copy vào container
echo "test data" > test.txt
docker cp test.txt myapp-web:/app/test.txt
docker exec myapp-web ls /app

# 3. Copy cả thư mục
mkdir -p static
echo "<h1>Test</h1>" > static/index.html
docker cp static myapp-web:/app/static
docker exec myapp-web ls /app/static
```

## Kết quả mong đợi

- `app-backup.py` tồn tại trên host, nội dung giống `app.py` của container.
- Sau bước 2, `docker exec myapp-web ls /app` thấy thêm `test.txt`.
- Sau bước 3, `docker exec myapp-web cat /app/static/index.html` ra `<h1>Test</h1>`.

## Câu hỏi

- File copy vào container có còn khi `docker rm` container? *(KHÔNG — filesystem container bị xóa cùng. Phải dùng volume — Bài 19)*
- Container stopped có copy được không? *(có — `docker cp` hoạt động cả với container đã dừng)*

## Bài kế tiếp

```bash
cp -r ../14-cp ../15-commit
cd ../15-commit
```
