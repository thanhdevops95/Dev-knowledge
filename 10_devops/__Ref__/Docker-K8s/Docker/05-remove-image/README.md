# Bài 05 — Xóa image

> **Loại bài:** quản lý dọn dẹp image.
> **Tiên quyết:** đã có `myapp`, `hello-world`, `python:3.11-slim` từ bài trước.
> **Không sửa source** — chỉ thao tác lệnh.

## Lệnh thủ công

```bash
# 1. Xóa hello-world (không còn cần)
docker rmi hello-world

# 2. Thử xóa base image đang được myapp dùng
# Lưu ý: Trên Docker mới (BuildKit), lệnh này sẽ chạy thành công và gỡ tag (Untagged) chứ không lỗi.
# Tuy nhiên các layer thực tế vẫn được giữ lại do myapp đang sử dụng.
docker rmi python:3.11-slim
# Output: Error response from daemon: conflict: unable to remove ...
# → Nếu lỗi (trên Docker cũ): Không sao, đây là bài học: image base không xóa được khi đang có image khác dùng

# 3. Xóa image dangling (image không tag, do build dở)
docker image prune
# Trả lời y khi hỏi

# 4. Verify — myapp vẫn còn, python:3.11-slim đã bị gỡ tag khỏi danh sách
docker images

```

## Kết quả mong đợi

- `docker rmi hello-world` thành công, in `Untagged: hello-world:latest` và `Deleted: sha256:...`.
- `docker rmi python:3.11-slim`:
  - *Trên Docker Desktop mới (BuildKit):* Chạy thành công và gỡ nhãn (báo `Untagged: python:3.11-slim`).
  - *Trên Docker cũ / Legacy:* Báo lỗi `conflict: unable to remove` (đây là kết quả mong đợi trên phiên bản cũ).
- Sau khi xong, `myapp:latest` vẫn hoạt động bình thường (do layer được cached độc lập).

## Tiêu chí hoàn thành

- [ ] `docker images hello-world` → trống
- [ ] `docker images myapp` → vẫn còn
- [ ] `docker images python` → không còn tag `3.11-slim` (nếu dùng Docker mới) hoặc vẫn còn (nếu báo lỗi trên Docker cũ)

## Câu hỏi

- Sự khác nhau giữa `docker rmi` (xóa cụ thể) và `docker image prune` (xóa dangling)?
- Khi nào dùng `-f` (force)? *(khi muốn xóa cưỡng chế, bỏ qua check container đang dùng)*

## Bài kế tiếp

```bash
cp -r ../05-remove-image ../06-tag-version
cd ../06-tag-version
```

Bài 06 sẽ tạo 2 phiên bản app (v1.1, v1.2) và gán tag.
