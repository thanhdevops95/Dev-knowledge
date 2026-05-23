# Bài 20 — Wait: chờ container kết thúc

> **Loại bài:** học `docker wait` và exit code.
> **File mới:** `myapp/exit_test.py`, `myapp/Dockerfile.exit`.

## Lệnh thủ công

```bash
cd myapp

# 1. Build image riêng cho exit test
docker build -t exit-test -f Dockerfile.exit .

# 2. Chạy background, gọi wait
docker run -d --name waiter exit-test
docker wait waiter           # block 2 giây rồi in exit code
echo "Exit code: $?"

# 3. Dọn dẹp
docker rm waiter
```

## Bài tập mở rộng — exit code 1

Sửa `exit_test.py` đổi `sys.exit(0)` thành `sys.exit(1)`, rebuild, chạy lại:

```bash
docker build -t exit-test -f Dockerfile.exit .
docker run -d --name waiter2 exit-test
docker wait waiter2          # in 1
echo "Exit: $?"               # in 1
docker rm waiter2
```

## Kết quả mong đợi

- `docker wait waiter` đứng ~2 giây (script `sleep(2)`), rồi in `0`.
- `echo $?` in `0`.
- Bài tập: in `1` thay vì `0`.

## Câu hỏi

- `docker wait` block đến khi nào? *(đến khi container exit)*
- Exit code trong CI/CD? *(0 = OK; ≠ 0 = fail → pipeline dừng)*

## Bài kế tiếp

```bash
cp -r ../20-wait ../21-network-redis
cd ../21-network-redis
```

Bài 21 — đại nâng cấp: thêm Redis, app `myapp:5.0`.
