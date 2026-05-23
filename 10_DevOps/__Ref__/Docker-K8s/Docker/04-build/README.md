# Bài 04 — Tạo app Python + Dockerfile cơ bản

> **Loại bài:** tạo source code đầu tiên.
> **Snapshot trước:** copy từ `03-run-foreground/`.

## Mục tiêu

Viết Dockerfile đầu tiên, build image từ source code Python.

## File trong thư mục này

```
04-build/
├── README.md         ← bạn đang đọc
├── KET-QUA.md        ← output thực tế (cập nhật sau khi chạy)
└── myapp/
    ├── app.py        ← v1.0 — chỉ print 2 dòng
    └── Dockerfile    ← FROM → CMD, 4 dòng
```

## Lệnh thủ công

```bash
cd myapp

# Build image (context = thư mục hiện tại)
docker build -t myapp .

# Verify image tồn tại
docker images myapp

# Chạy thử (container in 2 dòng rồi tự thoát)
docker run myapp
```

## Kết quả mong đợi

Output `docker run myapp`:
```
Hello from MyApp - Version 1.0
Running inside Docker container
```

`docker build` kết thúc bằng `Successfully tagged myapp:latest`.

## Tiêu chí hoàn thành

- [ ] Build không lỗi
- [ ] `docker images myapp` thấy tag `latest`
- [ ] `docker run myapp` in đúng 2 dòng và thoát (exit 0)

## Câu hỏi

- Mỗi dòng trong Dockerfile có ý nghĩa gì?
  - `FROM` chọn base image
  - `WORKDIR` set thư mục làm việc bên trong container
  - `COPY` copy file từ host vào image
  - `CMD` lệnh mặc định khi container start
- `WORKDIR` khác `cd` thế nào? *(WORKDIR tồn tại xuyên qua các layer; `cd` chỉ áp dụng trong 1 `RUN`)*
- Tại sao không cần install Python? *(image `python:3.11-slim` đã có sẵn)*

## Bài kế tiếp

```bash
cp -r ../04-build ../05-remove-image
cd ../05-remove-image
```

Bài 05 sẽ thao tác xóa image (không sửa source).
