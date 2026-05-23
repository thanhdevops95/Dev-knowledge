# Bài 12 — Exec vào container

> **Tiên quyết:** `myapp-web` đang chạy.

## Lệnh thủ công

```bash
# Nếu container đã dừng:
docker start myapp-web

# 1. Mở shell tương tác (bash) trong container
docker exec -it myapp-web /bin/bash
# Lưu ý: image alpine không có bash, dùng sh
# docker exec -it myapp-web sh
```

**Bên trong container, chạy các lệnh sau:**

```bash
pwd                    # /app
ls -la                 # thấy app.py
cat app.py             # xem source
ps aux                 # process gì đang chạy
env                    # biến môi trường
whoami                 # root
cat /etc/os-release    # debian (slim)
which python           # /usr/local/bin/python
exit                   # thoát shell, container vẫn chạy
```

**Lệnh nhanh không cần vào shell:**

```bash
docker exec myapp-web ls /app
docker exec myapp-web python --version
docker exec myapp-web pip list
```

## Kết quả mong đợi

- `pwd` → `/app` (đúng `WORKDIR`).
- `ps aux` thấy `python app.py` PID 1 (process chính của container).
- `whoami` → `root` (mặc định image python:3.11-slim).
- Sau `exit`, `docker ps` vẫn thấy `myapp-web` Up.

## Lỗi thường gặp

- `exec failed: ... "bash": executable file not found` → image dùng (như `alpine`) không có bash; thử `sh`.

## Câu hỏi

- Filesystem container khác máy host? *(hoàn toàn riêng — chỉ thấy file trong layer image + ghi đè runtime)*
- Khi exit shell, container có dừng? *(không — chỉ tắt session exec, process chính vẫn chạy)*

## Bài kế tiếp

```bash
cp -r ../12-exec ../13-logs
cd ../13-logs
```
