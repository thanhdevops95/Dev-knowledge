# 🐳 Docker — Images & Containers — Checklist Tự Đánh Giá

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)

---

## ✅ Danh Sách Kiểm Tra

### Phần 1: Images

- [ ] Tôi biết cách `docker pull` để tải image từ registry
- [ ] Tôi biết cách `docker images` để list local images
- [ ] Tôi hiểu REPOSITORY, TAG, IMAGE ID, SIZE columns
- [ ] Tôi biết cách `docker rmi` để remove image
- [ ] Tôi phân biệt được `:latest` tag với version tag (ví dụ `:3.18`)

### Phần 2: Containers — Running

- [ ] Tôi biết cách `docker run` để tạo và start container
- [ ] Tôi biết flag `-d` để run trong background (detached mode)
- [ ] Tôi biết flag `-p` để port mapping (`-p host:container`)
- [ ] Tôi biết flag `-it` để interactive terminal
- [ ] Tôi biết cách `docker ps` để xem running containers

### Phần 3: Containers — Managing

- [ ] Tôi biết cách `docker stop` để stop container (graceful, SIGTERM)
- [ ] Tôi biết cách `docker start` để start lại stopped container
- [ ] Tôi biết cách `docker rm` để remove container
- [ ] Tôi biết cách `docker ps -a` để list tất cả containers
- [ ] Tôi biết cách `docker logs` để xem container logs
- [ ] Tôi biết cách `docker logs -f` để follow logs (real-time)
- [ ] Tôi biết cách `docker exec -it` để exec shell vào container
- [ ] Tôi biết cách `docker inspect` để xem JSON metadata của container

### Phần 4: Container Lifecycle & Concepts

- [ ] Tôi phân biệt được Image (read-only) vs Container (writable)
- [ ] Tôi hiểu container là ephemeral (data mất khi container xóa)
- [ ] Tôi hiểu writable layer chỉ tồn tại khi container tồn tại
- [ ] Tôi hiểu container process (PID 1) và tầm quan trọng của signal handling
- [ ] Tôi hiểu tại sao container nên là single-process (one concern per container)

### Phần 5: Docker Registry & Naming

- [ ] Tôi biết Docker Hub là public registry mặc định
- [ ] Tôi hiểu format: `[registry/][namespace/]image[:tag]`
- [ ] Tôi biết `docker pull` tự động tìm image từ Docker Hub nếu không có registry prefix
- [ ] Tôi biết `:latest` tag không phải luôn là mới nhất (có thể stale)

---

## 🔍 Tự Đánh Giá

**Nếu >3 chưa check:** Cần ôn tập lại và làm lại exercises.

**Nếu 1-3 chưa check:** Gần OK, nhưng nên luyện thêm các commands chưa quen.

**Nếu tất cả đều check:** 🎉 Sẵn sàng cho bài tiếp theo!

---

**Next:** [Lesson 03 — Dockerfile Basics](../03-Dockerfile-Basics/lesson.md)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
