# Docker — 24 bài cơ bản + 5 bài Bonus production-grade

> **Series:** docker-practice · [← Mục lục tổng](../README.md) · [Tiếp: Kubernetes →](../K8s/README.md)

## Cách dùng

- **Mỗi bài 1 thư mục** chứa source + `README.md` hướng dẫn lệnh thủ công + (sau khi chạy) `KET-QUA.md` lưu output thực.
- **Tuần tự:** làm xong Bài N → `cp -r N-name N+1-next` → đổi tên thư mục → sửa file theo đề Bài N+1.
- **Không có script `.sh`** — chỉ chép từng lệnh vào terminal.

## Lộ trình 24 bài (cơ bản)

| Bài | Thư mục | Trọng tâm |
|-----|---------|-----------|
| 01 | [`01-pull-image/`](01-pull-image/) | `docker pull`, registry |
| 02 | [`02-list-images/`](02-list-images/) | `docker images` & filters |
| 03 | [`03-run-foreground/`](03-run-foreground/) | `--name`, `--rm`, exit code |
| 04 | [`04-build/`](04-build/) | Dockerfile đầu tiên, app v1.0 |
| 05 | [`05-remove-image/`](05-remove-image/) | `rmi`, `image prune` |
| 06 | [`06-tag-version/`](06-tag-version/) | Versioning v1.1 → v1.2, tag |
| 07 | [`07-retag/`](07-retag/) | `docker tag`, retag |
| 08 | [`08-history/`](08-history/) | Layer & history |
| 09 | [`09-inspect/`](09-inspect/) | `docker inspect` + `--format` |
| 10 | [`10-flask-web/`](10-flask-web/) | **Flask v2.0**, daemon `-d`, port mapping |
| 11 | [`11-lifecycle/`](11-lifecycle/) | stop/start/restart/pause/kill |
| 12 | [`12-exec/`](12-exec/) | `docker exec`, vào container |
| 13 | [`13-logs/`](13-logs/) | `docker logs`, `-f`, `--tail` |
| 14 | [`14-cp/`](14-cp/) | `docker cp` host ↔ container |
| 15 | [`15-commit/`](15-commit/) | `docker commit` → image mới |
| 16 | [`16-diff/`](16-diff/) | `docker diff` |
| 17 | [`17-stats/`](17-stats/) | `stats`, `top`, `inspect` |
| 18 | [`18-env-vars/`](18-env-vars/) | **app v3.0**, `-e`, `--env-file`, `ENV` |
| 19 | [`19-volume/`](19-volume/) | **app v4.0**, bind mount, named volume |
| 20 | [`20-wait/`](20-wait/) | `docker wait`, exit codes |
| 21 | [`21-network-redis/`](21-network-redis/) | **app v5.0**, custom network + Redis |
| 22 | [`22-multi-stage/`](22-multi-stage/) | `Dockerfile.multi`, image slim |
| 23 | [`23-compose/`](23-compose/) | **app v6.0**, `docker-compose.yml` full stack |
| 24 | [`24-push-registry/`](24-push-registry/) | Push lên Docker Hub |

## 🔴 Bonus — Production-grade (Bài 51-55)

> Bộ 24 bài trên đủ cho học viên **biết** Docker. Phần Bonus dưới đây trang bị các chủ đề **bắt buộc trước khi đẩy image ra production**. Đánh dấu 🔴 = không nên skip.

| Bài | Thư mục | Trọng tâm |
|-----|---------|-----------|
| 51 🔴 | [`51-secure-image/`](51-secure-image/) | `.dockerignore` + non-root `USER` + `HEALTHCHECK` → image `myapp:safe` |
| 52 🔴 | [`52-restart-limits/`](52-restart-limits/) | `--restart` policy + `--memory`/`--cpus` + OOMKill demo |
| 53 🔴 | [`53-entrypoint-signal/`](53-entrypoint-signal/) | ENTRYPOINT vs CMD, exec form, PID 1 signal, `tini` |
| 54 🔴 | [`54-image-scan/`](54-image-scan/) | `docker scout` + `trivy` quét CVE, output JSON/SARIF cho CI |
| 55 | [`55-buildx-multiarch/`](55-buildx-multiarch/) | `buildx` build amd64 + arm64 trong 1 lệnh |

## Tiến trình app `myapp`

```
Bài 04 → app v1.0 (print)
Bài 06 → v1.1, v1.2 (timestamp, OS info)
Bài 10 → v2.0 (Flask web server)
Bài 18 → v3.0 (env-aware, /config)
Bài 19 → v4.0 (logging vào /app/logs)
Bài 21 → v5.0 (Redis visitor counter)
Bài 23 → v6.0 (Compose stack: web + redis + postgres)
Bài 24 → v6.0 push lên <your-username>/myapp:6.0
Bài 51 → myapp:safe (non-root + HEALTHCHECK)
Bài 55 → <your-username>/myapp:6.0-multi (amd64 + arm64)
```

## Lưu ý chung

- Thay `<YOUR_DOCKERHUB_USERNAME>` thực sự khi đến Bài 24.
- Mac Apple Silicon: image build mặc định arm64; khi push để dùng cho cloud x86, dùng `docker buildx build --platform linux/amd64` (hoặc Bài 55 để build cả 2 arch).
- Bài 21: code phải dùng `host='redis'`, KHÔNG `localhost`.
- Bài 23: Compose V2 đã bỏ field `version:`. Lệnh là `docker compose` (có space).

→ Bắt đầu: [Bài 01](01-pull-image/)
