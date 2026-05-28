# Bài 15 — Commit container thành image

> **Tiên quyết:** `myapp-web` đang chạy.

## Lệnh thủ công

```bash
# 1. Vào container và cài tool mới
docker exec -it myapp-web bash

# === BÊN TRONG CONTAINER ===
apt-get update && apt-get install -y curl vim
which curl   # /usr/bin/curl
exit
# ==========================

# 2. Commit thành image mới
docker commit myapp-web myapp:2.0-with-tools

# 3. Kiểm tra image mới
docker images myapp

# 4. Verify image mới đã có curl
docker run --rm myapp:2.0-with-tools curl --version
```

## Kết quả mong đợi

- `docker images myapp` thấy thêm dòng `myapp:2.0-with-tools` với size lớn hơn (~30MB nhiều hơn).
- `docker run --rm myapp:2.0-with-tools curl --version` in version của curl.

## Lỗi thường gặp

- `apt-get` cần root. Trong image `python:3.11-slim` mặc định là root nên OK; nếu image khác user non-root, dùng `docker exec -u 0 -it myapp-web bash`.

## Câu hỏi

- Commit khác Dockerfile build? *(commit = chụp snapshot container hiện tại; build = tái tạo từ file → reproducible)*
- Tại sao commit KHÔNG nên dùng cho production?
  - Không reproducible (không ai biết bên trong đã làm gì)
  - Không có code history
  - Image phình to do cache apt
  - Khó debug/audit

## Bài kế tiếp

```bash
cp -r ../15-commit ../16-diff
cd ../16-diff
```
