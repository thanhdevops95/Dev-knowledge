# Bài 16 — Diff: xem thay đổi filesystem

> **Tiên quyết:** Bài 15 vừa cài curl/vim trong `myapp-web`.

## Lệnh thủ công

```bash
# 1. Xem diff so với image gốc
docker diff myapp-web

# Ký hiệu:
#   A = Added (thêm mới)
#   C = Changed (thay đổi)
#   D = Deleted (xóa)

# 2. Tạo thêm thay đổi
docker exec myapp-web touch /app/newfile.txt
docker exec myapp-web rm /app/test.txt 2>/dev/null || true

# 3. Diff lại
docker diff myapp-web | grep -E '^A |^C |^D '
```

## Kết quả mong đợi

- Thấy rất nhiều dòng `A /var/cache/apt/...` do `apt-get update` ở Bài 15.
- Sau bước 2, có dòng `A /app/newfile.txt` và `D /app/test.txt`.

## Câu hỏi

- Tại sao nhiều file `/var/cache/apt/...` sau `apt install`? *(apt cache index packages — chính lý do production Dockerfile nên `apt-get clean && rm -rf /var/lib/apt/lists/*`)*

## Bài kế tiếp

```bash
cp -r ../16-diff ../17-stats
cd ../17-stats
```
