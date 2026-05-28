# Bài 08 — Xem lịch sử image (History)

> **Loại bài:** đọc `docker history`.
> **Tiên quyết:** có `myapp:1.2` và `python:3.11-slim`.

## Lệnh thủ công

```bash
# 1. Lịch sử layer của myapp:1.2
docker history myapp:1.2

# 2. So với base image
docker history python:3.11-slim

# 3. Không cắt nội dung
docker history --no-trunc myapp:1.2
```

## Kết quả mong đợi

Mỗi dòng = 1 layer; cột `SIZE` cho biết layer đó chiếm bao nhiêu byte.
- Các dòng đầu có `<missing>` ID — đó là layer của base image (không thể inspect chi tiết qua history vì chúng được build từ máy khác).
- Layer lớn nhất thường là layer install package hoặc base image.

## Câu hỏi

- Mỗi lệnh trong Dockerfile tạo ra 1 layer? *(đúng với các lệnh thay đổi filesystem: FROM/COPY/RUN/ADD; lệnh metadata như ENV/CMD/EXPOSE cũng tạo 1 layer nhưng size 0)*
- Layer `<missing>` ID nghĩa là gì? *(layer base image — không có manifest local)*

## Bài kế tiếp

```bash
cp -r ../08-history ../09-inspect
cd ../09-inspect
```
