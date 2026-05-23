# 🐳 Docker — Advanced Topics — Checklist Tự Đánh Giá

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)

---

## ✅ Danh Sách Kiểm Tra

### Multi-Stage Builds

- [ ] Tôi viết được multi-stage Dockerfile với ít nhất 3 stages (deps, builder, runtime)
- [ ] Tôi hiểu cách copy artifacts giữa stages (`COPY --from=builder`)
- [ ] Tôi biết tạo non-root user trong Dockerfile
- [ ] Tôi hiểu tại sao multi-stage giảm image size
- [ ] Tôi biết multi-stage cho Node.js, Python, ít nhất 1 ngôn ngữ

### Layer Caching & BuildKit

- [ ] Tôi hiểu Docker layer caching hoạt động thế nào
- [ ] Tôi biết order Dockerfile để maximize cache hits (dependencies trước, code sau)
- [ ] Tôi biết dùng `.dockerignore` để giảm build context
- [ ] Tôi enable BuildKit và biết cache mounts
- [ ] Tôi dùng `--mount=type=cache` trong Dockerfile cho package cache

### Docker Compose Advanced

- [ ] Tôi viết được docker-compose.yml với healthcheck cho mỗi service
- [ ] Tôi dùng `depends_on` với `condition: service_healthy`
- [ ] Tôi configure resource limits (CPU, memory) trong `deploy.resources`
- [ ] Tôi setup logging rotation (max-size, max-file)
- [ ] Tôi dùng YAML anchors (`&anchor`, `*alias`) cho DRY
- [ ] Tôi biết override với `docker-compose -f base.yml -f override.yml`

### Networking

- [ ] Tôi tạo custom network với `docker network create`
- [ ] Tôi hiểu containers có thể communicate qua tên trong cùng network
- [ ] Tôi biết network types: bridge, host, overlay
- [ ] Tôi inspect network với `docker network inspect`
- [ ] Tôi connect/disconnect container vào network

### Volumes & Storage

- [ ] Tôi biết 3 types: bind mount, named volume, tmpfs
- [ ] Tôi create và dùng named volume
- [ ] Tôi backup volume với `tar` trong alpine container
- [ ] Tôi restore volume từ backup
- [ ] Tôi prune unused volumes

### Security

- [ ] Tôi dùng specific image tags (không `latest`)
- [ ] Tôi run container với non-root user (`USER` directive)
- [ ] Tôi scan images với Trivy/`docker scout`
- [ ] Tôi biết `--read-only`, `--cap-drop`, `--security-opt`
- [ ] Tôi không store secrets trong image (dùng env tại runtime)
- [ ] Tôi dùng `HEALTHCHECK` directive

### Debugging & Production

- [ ] Tôi debug container với `docker exec`, `docker logs`, `docker inspect`
- [ ] Tôi xem real-time stats với `docker stats`
- [ ] Tôi copy files giữa host-container với `docker cp`
- [ ] Tôi debug distroless/scratch images với side-car container
- [ ] Tôi dùng `dumb-init` cho proper signal handling
- [ ] Tôi build multi-arch với `docker buildx`

---

## 🔍 Tự Đánh Giá

**Nếu >5 chưa check:** Cần làm lại exercises và đọc kỹ lesson.

**Nếu 3-5 chưa check:** Gần OK, nhưng nên luyện thêm các phần chưa quen.

**Nếu tất cả đều check:** 🎉 Bạn đã master Docker advanced topics!

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
