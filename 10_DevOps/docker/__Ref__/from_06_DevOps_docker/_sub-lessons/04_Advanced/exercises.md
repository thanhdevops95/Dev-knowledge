# 🐳 Docker — Advanced Topics — Bài Tập Thực Hành

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)
- **Type:** `[Exercise]`
- **Difficulty:** `[Medium-Hard]`
- **Estimated Time:** 2-3 giờ tổng cộng
- **Prerequisites:** [Lesson 03](../03-Dockerfile-Basics/lesson.md)

---

## 🎯 Mục Tiêu

Thực hành advanced Docker topics: multi-stage builds, Docker Compose với healthcheck, networking, volumes, security scanning.

---

## 📝 Bài Tập

### Bài 1: Multi-Stage Build — So Sánh Image Size

**Task:** Viết Dockerfile đơn stage và multi-stage cho Node.js app, đo lường improvement.

**Yêu cầu:**
1. Single-stage Dockerfile:
   ```dockerfile
   FROM node:20-alpine
   WORKDIR /app
   COPY . .
   RUN npm ci
   EXPOSE 3000
   CMD ["node", "server.js"]
   ```
2. Multi-stage Dockerfile (như trong lesson)
3. Build cả 2 với tags khác nhau
4. So sánh size: `docker images | grep node`
5. Ghi lại: Single: ___ MB, Multi: ___ MB, Savings: ___%

**Câu hỏi:** Tại sao multi-stage nhỏ hơn? Giải thích layers.

---

### Bài 2: Docker Compose với Healthcheck

**Task:** Tạo `docker-compose.yml` cho app + PostgreSQL + Redis với healthchecks.

**Yêu cầu:**
- App service: healthcheck `/health` mỗi 30s
- PostgreSQL: healthcheck với `pg_isready`
- Redis: healthcheck với `redis-cli ping`
- App `depends_on` chờ DB healthy
- Resource limits: CPU 0.5, Memory 512M
- Logging: json-file, max-size 10m, max-file 3

**Commands:**
```bash
docker compose up -d
docker compose ps  # Check health status
docker compose logs -f app
```

---

### Bài 3: Networking — Containers Communicate by Name

**Task:** Tạo custom network và 2 containers có kết nối qua container name.

**Steps:**
```bash
docker network create myapp-net
docker run -d --name postgres --network myapp-net -e POSTGRES_PASSWORD=secret postgres:15-alpine
docker run -d --name app --network myapp-net -e DATABASE_URL=postgres://postgres:secret@postgres:5432/mydb nginx:alpine
docker exec app ping -c 3 postgres  # Should work!
docker exec app nc -zv postgres 5432  # Check port open
```

**Ghi lại:** Ping thành công? ____ Port 5432 accessible? ____

---

### Bài 4: Volumes — Backup & Restore PostgreSQL

**Task:** Backup volume của PostgreSQL, xóa container, restore.

**Steps:**
1. Create volume: `docker volume create pgbackup-demo`
2. Run PostgreSQL với volume:
   ```bash
   docker run -d --name pg-demo \
     -v pgbackup-demo:/var/lib/postgresql/data \
     -e POSTGRES_PASSWORD=demo123 \
     postgres:15-alpine
   ```
3. Tạo database và table, insert some data (vào psql)
4. Backup volume:
   ```bash
   docker run --rm -v pgbackup-demo:/source:ro -v $(pwd):/backup alpine \
     tar czf /backup/pgbackup-demo.tar.gz -C /source .
   ```
5. Stop & remove container: `docker stop pg-demo && docker rm pg-demo`
6. Restore:
   ```bash
   docker run --rm -v pgbackup-demo:/target -v $(pwd):/backup alpine \
     tar xzf /backup/pgbackup-demo.tar.gz -C /target
   ```
7. Run PostgreSQL lại với cùng volume, verify data còn không?

**Kết quả:** Data restored successfully? ✅/❌

---

### Bài 5: Security Scan với Trivy

**Task:** Scan Docker image để tìm vulnerabilities.

**Steps:**
1. Install Trivy: https://aquasecurity.github.io/trivy/
2. Scan nginx:latest:
   ```bash
   trivy image nginx:latest
   ```
3. Scan image của bạn (nếu có)
4. Ghi lại:
   - Total vulnerabilities: ___
   - Critical: ___, High: ___, Medium: ___
5. Làm gì để fix? ( Ví dụ: update base image, use specific version)

---

### Bài 6 (Challenge): Build Multi-Arch Image

**Task:** Build image cho cả amd64 và arm64 (nếu có Mac M1/M2 hoặc hỗ trợ).

**Steps:**
```bash
docker buildx create --use --name mymultiarch
docker buildx inspect --bootstrap
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  -t yourusername/myapp:latest .
docker manifest inspect yourusername/myapp:latest
```

**Lưu ý:** Cần registry (Docker Hub, GHCR) để push. Nếu không, có thể build local với `--load` nhưng chỉ được 1 arch tại thời điểm build.

---

## 💡 Hints

### Hint 1: Multi-stage Build Order

Typical pattern:
1. `deps` — Install production dependencies only
2. `builder` — Full deps + build step (if needed)
3. `runtime` — Copy from deps/builder, non-root user, minimal

### Hint 2: Docker Compose Healthcheck

Healthcheck phải return 0 (success) hoặc non-zero (failure). Dùng `curl -f` (fail on 4xx/5xx) hoặc `pg_isready`.

### Hint 3: Networking

Containers trong cùng network có thể giao tiếp qua **tên container** (hoặc **service name** trong docker-compose). Không cần `-p` expose port ra host.

---

## ✅ Success Criteria

**Pass:**
- ✅ Hoàn thành ít nhất 4/6 bài tập
- ✅ Multi-stage image size giảm ≥30% so với single-stage
- ✅ Docker Compose có healthcheck và resource limits
- ✅ Containers communicate qua network name
- ✅ Volume backup/restore thành công
- ✅ Scan image với Trivy

**Excellent:**
- ⭐ Hoàn thành tất cả 6 bài
- ⭐ Multi-stage image size giảm ≥50%
- ⭐ Docker Compose có logging rotation, restart policy, networks
- ⭐ Build multi-arch image thành công
- ⭐ Không có vulnerabilities (hoặc rất ít) sau scan

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
