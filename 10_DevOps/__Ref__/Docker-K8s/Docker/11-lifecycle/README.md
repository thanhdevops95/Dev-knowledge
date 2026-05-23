# Bài 11 — Vòng đời container (stop/start/restart/pause/kill)

> **Tiên quyết:** container `myapp-web` từ Bài 10 đang chạy. Nếu đã `rm`, làm lại Bài 10 trước.

## Lệnh thủ công (làm tuần tự)

```bash
# 1. STOP — gửi SIGTERM, đợi grace period rồi SIGKILL
docker stop myapp-web
docker ps                  # không thấy
docker ps -a               # thấy với STATUS Exited

# 2. START — chạy lại container đã có
docker start myapp-web
curl http://localhost:8080    # vẫn hoạt động

# 3. RESTART
docker restart myapp-web

# 4. PAUSE — đóng băng process (SIGSTOP)
docker pause myapp-web
curl --max-time 3 http://localhost:8080   # treo — KHÔNG phản hồi (process bị đóng băng)

# 5. UNPAUSE
docker unpause myapp-web
curl http://localhost:8080     # hoạt động trở lại

# 6. KILL — SIGKILL ngay lập tức
docker kill myapp-web
docker ps -a                   # STATUS: Exited (137) — exit code 137 = bị kill
```

## Kết quả mong đợi

| Lệnh | STATUS sau khi chạy |
|------|---------------------|
| `stop` | `Exited (0)` **hoặc** `Exited (137)` ← xem note |
| `start` | `Up X seconds` |
| `pause` | `Up X (Paused)` |
| `unpause` | `Up X seconds` |
| `kill` | `Exited (137)` |

> ⚠️ **Quan sát đáng chú ý — Flask dev server + SIGTERM:**
> `docker stop myapp-web` lý thuyết gửi SIGTERM → app graceful exit (code 0 hoặc 143). **Nhưng** Flask `app.run()` KHÔNG cài signal handler → Docker chờ 10s grace period → buộc phải SIGKILL → exit code **137** (như `kill`).
>
> Đây là bằng chứng cho vấn đề **PID 1 + signal handling** sẽ học chi tiết ở **Bonus Bài 53**. Production app phải dùng WSGI thật (gunicorn) hoặc đăng ký handler:
> ```python
> import signal, sys
> signal.signal(signal.SIGTERM, lambda s,f: sys.exit(0))
> ```

## Câu hỏi

- `stop` vs `kill`? *(stop: SIGTERM → đợi 10s → SIGKILL; kill: SIGKILL ngay → không có chance cleanup)*
- `pause` khác `stop`? *(pause giữ container trong RAM, process đóng băng; stop tắt hẳn process)*
- Dữ liệu sau stop/start có còn? *(còn — filesystem của container không bị xóa khi stop)*

## Bài kế tiếp

```bash
# Nếu container đã exit (sau kill), start lại trước khi sang bài 12
docker start myapp-web

cp -r ../11-lifecycle ../12-exec
cd ../12-exec
```
