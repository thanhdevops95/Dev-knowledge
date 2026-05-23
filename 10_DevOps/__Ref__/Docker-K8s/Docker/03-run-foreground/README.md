# Bài 03 — Run container cơ bản (foreground)

> **Loại bài:** thao tác `docker run` với options khác nhau.
> **Snapshot trước:** copy từ `02-list-images/`.

## Mục tiêu

Chạy container từ image có sẵn, hiểu vòng đời container — container thoát khi process chính thoát, học cách đặt tên và tự động dọn dẹp container.

## Lệnh thủ công

```bash
# 1. Run foreground với hello-world (in xong tự thoát)
docker run hello-world

# 2. Run foreground với alpine + truyền lệnh
docker run alpine echo "Hello from Alpine"

# 3. Run với tên cụ thể
docker run --name alpine-test alpine echo "Testing name"

# 4. Chạy lại cùng tên → SẼ LỖI vì container "alpine-test" đã tồn tại (Exited)
docker run --name alpine-test alpine echo "Testing name"
# Error response from daemon: Conflict. The container name "/alpine-test" is already in use...

# 5. Liệt kê container đã dừng để kiểm tra
docker ps -a

# 6. Run với --rm (tự xóa container sau khi chạy xong)
docker run --rm alpine echo "Testing --rm"

# 7. Dọn dẹp container cũ
docker rm alpine-test
```

## Kết quả mong đợi

- `docker ps -a` thấy `alpine-test` ở trạng thái `Exited (0)`.
- Sau khi chạy với `--rm`, `docker ps -a` không hiển thị container đó.
- Sau khi `docker rm alpine-test`, lệnh `docker ps -a` không còn container đó nữa.

## Câu hỏi

- Tại sao container dừng ngay sau khi chạy? *(process chính kết thúc -> container exit)*
- `docker run` vs `docker start`? *(run = tạo + start container mới; start = chạy lại container cũ đã dừng)*

## Bài kế tiếp

```bash
cp -r ../03-run-foreground ../04-build
cd ../04-build
```

Bài 04 sẽ **tạo file mới** viết Dockerfile và build image `myapp` đầu tiên từ code Python.
