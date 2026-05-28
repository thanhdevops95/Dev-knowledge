# Bài 02 — Liệt kê & lọc image

> **Loại bài:** đọc lệnh `docker images` với các cờ khác nhau.
> **Tiên quyết:** đã pull 3 image ở Bài 01.

## Lệnh thủ công

```bash
# 1. Liệt kê tất cả image
docker images

# 2. Chỉ lấy ID
docker images -q

# 3. Bao gồm cả image trung gian (dangling)
docker images -a

# 4. Lọc image có "python"
docker images | grep python

# 5. In dạng bảng tùy chỉnh
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

```

## Kết quả mong đợi

- Lệnh `docker images` ra bảng có cột `REPOSITORY`, `TAG`, `IMAGE ID`, `CREATED`, `SIZE`.
```bash
Output:
    IMAGE                ID             DISK USAGE   CONTENT SIZE   EXTRA
    alpine:latest        5b10f432ef3d       13.6MB         4.29MB        
    hello-world:latest   0e760fdfbc48       22.6kB         10.3kB        
    python:3.11-slim     9a7765b36773        214MB           48MB    
```

- `docker images -q` chỉ in các dòng ID (12 ký tự).
```bash
Output:
    9a7765b36773
    5b10f432ef3d
    0e760fdfbc48
```

- `docker images -a` bao gồm cả image trung gian (dangling)
```bash
Output:
    IMAGE                ID             DISK USAGE   CONTENT SIZE   EXTRA
    alpine:latest        5b10f432ef3d       13.6MB         4.29MB        
    hello-world:latest   0e760fdfbc48       22.6kB         10.3kB        
    python:3.11-slim     9a7765b36773        214MB           48MB    
```

- Lọc `python` ra 1 dòng `python  3.11-slim`.
```bash
Output:
    WARNING: This output is designed for human readability. For machine-readable output, please use --format.
    python:3.11-slim     9a7765b36773        214MB           48MB   
```

- `docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"` ra bảng có 3 cột: Repository, Tag, Size.
```bash
Output:
    REPOSITORY    TAG         SIZE
    python        3.11-slim   214MB
    alpine        latest      13.6MB
    hello-world   latest      22.6kB
```

## Câu hỏi

- `IMAGE ID` có ý nghĩa gì? *(SHA256 của image — định danh duy nhất; 2 image cùng nội dung → cùng ID)*
- Cột `CREATED` là thời gian image được **build** (không phải lúc bạn pull).

## Bài kế tiếp

```bash
cp -r ../02-list-images ../03-run-foreground
cd ../03-run-foreground
```

Bài 03 sẽ thực hành chạy thử container cơ bản (foreground) với các image đã pull.
