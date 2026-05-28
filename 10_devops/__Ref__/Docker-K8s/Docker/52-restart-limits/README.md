# Bài 52 — Restart Policy + Resource Limits 🔴

> **Loại bài:** học flag CLI, không sửa source code.
> **Snapshot trước:** copy từ `51-secure-image/` (dùng image `myapp:safe`).

## Mục tiêu

Container production phải:

1. **Tự khôi phục** khi crash → restart policy.
2. **Không nuốt sạch RAM/CPU** của host → resource limits.
3. **Bị OOMKill rõ ràng** thay vì làm chậm cả node → memory cap.

## File trong thư mục này

```
52-restart-limits/
└── README.md          ← chỉ README, dùng lại image myapp:safe
```

Tái sử dụng image `myapp:safe` từ Bài 51. Nếu chưa có:

```bash
cd ../51-secure-image/myapp && docker build -t myapp:safe . && cd -
```

## So sánh 4 restart policy

| Flag | Restart khi crash? | Restart sau reboot máy? | Restart khi `docker stop`? |
|------|--------------------|--------------------------|----------------------------|
| `--restart=no` (default) | ❌ | ❌ | ❌ |
| `--restart=on-failure[:N]` | ✅ (exit ≠ 0, tối đa N lần) | ✅ | ❌ |
| `--restart=always` | ✅ | ✅ | ✅ (tự dậy lại!) |
| `--restart=unless-stopped` | ✅ | ✅ | ❌ (tôn trọng stop thủ công) |

## Lệnh thủ công

### Phần A — Restart policy

```bash
# 1. always: luôn restart, kể cả sau reboot máy
docker run -d --restart=always --name myapp-always myapp:safe

# 2. unless-stopped: như always nhưng KHÔNG restart nếu bị stop thủ công
docker run -d --restart=unless-stopped --name myapp-unless myapp:safe

# 3. on-failure: chỉ restart khi exit code != 0, tối đa 5 lần
docker run -d --restart=on-failure:5 --name myapp-onfail myapp:safe

# 4. Test: kill process bên trong container, xem có tự dậy không
# LƯU Ý: pkill KHÔNG có trong python:3.11-slim → dùng kill -9 1 (PID 1 = entrypoint)
docker exec myapp-always kill -9 1
docker ps                # Restarting → Up sau vài giây

# 5. Kiểm tra restart count
docker inspect --format='{{.RestartCount}}' myapp-always
```

> 💡 Image slim/alpine không cài `pkill`, `procps`, `htop` mặc định. Hoặc cài thêm (`apt-get install -y procps`) hoặc dùng `kill -<signal> <pid>` — PID 1 luôn là process chính của container.

### Phần B — Resource limits

```bash
# 6. Giới hạn 128MB RAM, 0.5 CPU, tối đa 100 process
docker run -d --name myapp-limited \
  --memory=128m \
  --memory-swap=128m \
  --cpus=0.5 \
  --pids-limit=100 \
  --restart=on-failure:3 \
  myapp:safe

# 7. Quan sát real-time usage
docker stats myapp-limited
# Ctrl+C thoát

# 8. Stress test → trigger OOMKill
docker exec myapp-limited python -c "x=[0]*100000000"
# Container sẽ exit với OOMKilled = true

docker inspect --format='{{.State.OOMKilled}}' myapp-limited     # true
docker inspect --format='{{.State.ExitCode}}'  myapp-limited     # 137 (= 128 + 9)
```

### Phần C — Dọn dẹp

```bash
docker stop myapp-always myapp-unless myapp-onfail myapp-limited 2>/dev/null
docker rm   myapp-always myapp-unless myapp-onfail myapp-limited 2>/dev/null
```

## Kết quả mong đợi

- Sau khi `pkill python`, container `myapp-always` chuyển `Restarting` → `Up` trong vài giây.
- `docker stats` cho thấy `myapp-limited` không vượt quá 128MB / 50% 1-CPU.
- Stress test → `OOMKilled = true`, exit code `137`.

## Tiêu chí hoàn thành

- [ ] Hiểu khác biệt giữa 4 restart policy
- [ ] Đã chạy stress test và quan sát `OOMKilled = true`
- [ ] Đối chiếu được bảng map sang K8s (xem phần dưới)
- [ ] Đã trả lời câu hỏi suy ngẫm

## So sánh với K8s tương ứng

| Docker flag | K8s field |
|-------------|-----------|
| `--memory=128m` | `resources.limits.memory: 128Mi` |
| `--cpus=0.5` | `resources.limits.cpu: "500m"` |
| `--restart=always` | `restartPolicy: Always` (default Deployment) |
| `--restart=on-failure` | `restartPolicy: OnFailure` (Job) |
| `--restart=no` | `restartPolicy: Never` (Job) |

## Lỗi thường gặp

| Lỗi | Cách xử lý |
|------|------------|
| `--memory-swap` < `--memory` | Phải `>=` memory, hoặc đặt cùng giá trị để disable swap |
| `--cpus` không hiệu lực | Yêu cầu cgroup v2 trên Linux; macOS/Windows OK qua VM |
| Container không restart sau reboot máy | Docker daemon chưa auto-start (Linux: `systemctl enable docker`) |

## Câu hỏi

- Vì sao `--restart=always` nguy hiểm trong dev (nhưng tốt cho prod)? *(restart loop khi config sai, vô tình giấu lỗi)*
- K8s tách `requests` và `limits` — Docker chỉ có `--memory` (= limit). Khi nào cần phân biệt?

## Bài kế tiếp

```bash
cp -r ../52-restart-limits ../53-entrypoint-signal
cd ../53-entrypoint-signal
```

Bài 53 sẽ tạo source mới (`signal_app.py`) + 4 Dockerfile demo.
