# Bài 07 — Đổi tag (Retag)

> **Loại bài:** thao tác `docker tag` và `rmi` trên tag.
> **Tiên quyết:** đã có `myapp:1.2` từ Bài 06.

## Mục tiêu

Hiểu tag là "nhãn dán", không phải bản sao image.

## Lệnh thủ công

```bash
# 1. Tag thêm "stable" và "production" cho image myapp:1.2
docker tag myapp:1.2 myapp:stable
docker tag myapp:1.2 myapp:production

# 2. Liệt kê - thấy cùng IMAGE ID, nhiều tag
docker images myapp

# 3. Xóa chỉ tag production (image vẫn tồn tại vì còn tag khác)
docker rmi myapp:production

# 4. Verify
docker images myapp
```

## Kết quả mong đợi

Sau bước 2:
```
REPOSITORY   TAG          IMAGE ID       ...
myapp        1.2          abc123def456   ...
myapp        latest       abc123def456   ...   ← cùng ID
myapp        production   abc123def456   ...   ← cùng ID
myapp        stable       abc123def456   ...   ← cùng ID
myapp        1.1          789xyz...      ...
```

Sau bước 3: dòng `production` biến mất, các tag khác vẫn còn, **không có image nào bị xóa khỏi disk**.

## Câu hỏi

- Tag bản chất là gì? *(con trỏ tới image ID — không tốn dung lượng)*
- Khi xóa 1 tag, image có bị xóa không? *(không, nếu vẫn còn tag khác trỏ tới)*

## Bài kế tiếp

```bash
cp -r ../07-retag ../08-history
cd ../08-history
```
