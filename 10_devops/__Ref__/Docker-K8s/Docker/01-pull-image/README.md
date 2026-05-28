# Bài 01 — Pull image đầu tiên

> **Loại bài:** thực hành lệnh `docker pull` — chưa có source code.
> **Snapshot kế tiếp:** copy `01-pull-image/` → `02-list-images/`.

## Mục tiêu

Pull 3 image về máy từ Docker Hub, hiểu khái niệm image & registry.

## Lệnh thủ công (gõ từng dòng vào terminal)

```bash
# 1. Image hello-world (để test docker hoạt động)
docker pull hello-world

# 2. Image base cho myapp ở các bài sau — DÙNG ĐÚNG TAG, không pull python:latest
docker pull python:3.11-slim

# 3. Image alpine (làm quen image siêu nhỏ)
docker pull alpine:latest

# 4. Kiểm tra (BẮT BUỘC)
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep -E 'hello-world|python|alpine'
```

## Kết quả mong đợi

- Mỗi `docker pull` kết thúc bằng dòng `Status: Downloaded newer image ...` hoặc `Image is up to date ...`.
- Lệnh verify cuối hiển thị **đủ 3 dòng** image với tag đúng.

Xem output thực tế trong [`KET-QUA.md`](KET-QUA.md).

## Tiêu chí hoàn thành

- [ ] `docker images hello-world` ra 1 dòng
- [ ] `docker images python` thấy tag `3.11-slim`
- [ ] `docker images alpine` thấy tag `latest`

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| `Cannot connect to the Docker daemon` | Mở Docker Desktop, đợi icon chuyển sang đang chạy |
| `denied: requested access` | Image này là public — kiểm tra lại tên (gõ sai `pyhon` thay vì `python`?) |
| Pull rất chậm | Mạng yếu hoặc Docker Hub bị rate-limit; thử lại sau hoặc `docker login` |

## Bài kế tiếp

```bash
# Tạo snapshot cho bài 02
cd /Users/rom/Docker-K8s/Docker
cp -r 01-pull-image 02-list-images
cd 02-list-images
# rồi đọc README.md trong folder 02
```

## Câu hỏi suy ngẫm

- Khi pull, terminal hiển thị nhiều dòng `Pull complete` — đó là gì? *(mỗi layer của image)*
- Tại sao lần pull thứ 2 cùng image lại nhanh hơn? *(đã có cache local, chỉ check digest)*
