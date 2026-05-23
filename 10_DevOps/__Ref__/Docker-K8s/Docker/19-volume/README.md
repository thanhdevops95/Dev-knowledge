# Bài 19 — Volume: lưu dữ liệu bền vững

> **Loại bài:** sửa app ghi log ra file, học Bind Mount + Named Volume.
> **Build tag:** `myapp:4.0`

## File thay đổi

| File | Thay đổi |
|------|----------|
| `myapp/app.py` | thêm `logging` ghi vào `/app/logs/app.log` |

## Lệnh thủ công

### Phần A — Bind Mount (mount thư mục host)

```bash
cd myapp

docker build -t myapp:4.0 .

docker stop myapp-web 2>/dev/null; docker rm myapp-web 2>/dev/null
mkdir -p ./logs

docker run -d -p 8080:5000 \
  -v "$(pwd)/logs":/app/logs \
  --name myapp-web myapp:4.0

curl http://localhost:8080
cat ./logs/app.log   # Log xuất hiện trên host NGAY LẬP TỨC
```

### Phần B — Named Volume

```bash
docker volume create myapp-data
docker volume ls
docker volume inspect myapp-data

docker run -d -p 8081:5000 \
  -v myapp-data:/app/logs \
  --name myapp-web2 myapp:4.0

curl http://localhost:8081
```

### Phần C — Test tính bền vững

```bash
# Xóa container
docker rm -f myapp-web2

# Tạo lại, vẫn dùng volume cũ
docker run -d -p 8081:5000 -v myapp-data:/app/logs --name myapp-web2 myapp:4.0

# Log cũ vẫn còn
docker exec myapp-web2 cat /app/logs/app.log
```

## Kết quả mong đợi

- File `./logs/app.log` trên host có nội dung sau khi curl (bind mount).
- Sau khi xóa rồi tạo lại `myapp-web2`, log cũ vẫn còn (named volume bền vững).

## Câu hỏi

- Bind mount vs Named volume?
  - Bind mount: thư mục host cụ thể → tốt cho dev (edit code thấy ngay)
  - Named volume: Docker quản lý → tốt cho data production
- Volume có bị xóa khi `docker rm container`? *(KHÔNG. Phải `docker volume rm myapp-data` riêng)*

## Bài kế tiếp

```bash
cp -r ../19-volume ../20-wait
cd ../20-wait
```
