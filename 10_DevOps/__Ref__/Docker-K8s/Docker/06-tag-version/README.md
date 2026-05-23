# Bài 06 — Tag & Versioning

> **Loại bài:** sửa `app.py` 2 lần, build với tag cụ thể.
> **Snapshot trước:** copy từ `05-remove-image/`.

## Mục tiêu

Hiểu khái niệm tag, quản lý nhiều phiên bản image.

## Tiến trình (làm theo thứ tự)

> ⚠️ **macOS lưu ý:** `cp` thường được alias thành `cp -i` (interactive). Lệnh `cp app_v1_1.py.snapshot app.py` sẽ **hỏi confirm** mà nếu copy-paste cả block, không gõ `y` → file **KHÔNG overwrite** → bạn build sai content mà không có error. Cách tránh: dùng `/bin/cp -f` hoặc `\cp -f` (gạch chéo bỏ alias).

### Bước 1 — Sửa app thành v1.1, build tag 1.1

Sửa `myapp/app.py` thành **nội dung 1.1** (đã chuẩn bị sẵn trong file `myapp/app_v1_1.py.snapshot` để tham khảo). Copy vào `app.py`:

```bash
cd myapp
/bin/cp -f app_v1_1.py.snapshot app.py     # -f bypass interactive prompt
docker build -t myapp:1.1 .
```

### Bước 2 — Sửa app thành v1.2, build tag 1.2

```bash
/bin/cp -f app_v1_2.py.snapshot app.py
docker build -t myapp:1.2 .
```

### Bước 3 — Build không tag (sẽ thành `latest`)

```bash
docker build -t myapp .
```

### Bước 4 — Liệt kê

```bash
docker images myapp
```

## Kết quả mong đợi

```
REPOSITORY   TAG       IMAGE ID       CREATED         SIZE
myapp        latest    xxxxxxxxxxxx   a few seconds   xxxMB
myapp        1.2       xxxxxxxxxxxx   a few seconds   xxxMB
myapp        1.1       xxxxxxxxxxxx   a minute ago    xxxMB
```

- `myapp:1.1` có ID **khác** `myapp:1.2` (nội dung app khác).
- `myapp:1.2` và `myapp:latest`: với **Docker classic builder** → cùng IMAGE ID (vì cùng content). Với **BuildKit** (Docker 23+, mặc định hiện nay) → có thể **khác** do mỗi build sinh manifest metadata riêng. Cả hai đều là kết quả hợp lệ.

## File trong thư mục này

```
06-tag-version/
├── README.md
├── KET-QUA.md
└── myapp/
    ├── app.py                  ← bản đang dùng (sẽ là v1.2 sau khi làm xong)
    ├── app_v1_1.py.snapshot    ← bản v1.1 để khôi phục/tham khảo
    ├── app_v1_2.py.snapshot    ← bản v1.2
    └── Dockerfile
```

## Câu hỏi

- Có bao nhiêu image `myapp` hiện tại? *(3: latest, 1.1, 1.2 — nhưng latest và 1.2 chung 1 ID)*
- Tag `latest` đang trỏ tới version nào? *(v1.2, vì build cuối)*

## Bài kế tiếp

```bash
cp -r ../06-tag-version ../07-retag
cd ../07-retag
```
