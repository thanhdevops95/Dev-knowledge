# 📚 Docker — Danh Sách Bài Học

---

## Tổng quan

Đây là **bài mẹ** cho chủ đề Docker. Dưới đây là danh sách tất cả các bài con bạn cần học để thành thạo Docker từ cơ bản đến nâng cao.

---

## 📝 Danh Sách Bài Học

### 🟢 [Lesson 01: Installation & Setup](_sub-lessons/01-Installation-Setup/)

**Thời gian:** 45 phút  
**Cấp độ:** BEGINNER  
**Mục tiêu:** Cài đặt Docker Desktop, verify installation, và hiểu architecture cơ bản

**Nội dung chính:**
- Docker Desktop vs Docker Engine
- Architecture: Client-Server, Docker Daemon
- Verify installation với `docker --version` và `docker run hello-world`
- Cấu hình cơ bản (resources, networking)

**Prerequisites:** Không cần gì

→ [Bắt đầu học](_sub-lessons/01-Installation-Setup/lesson.md)

---

### 🟢 [Lesson 02: Images & Containers](_sub-lessons/02-Images-Containers/)

**Thời gian:** 1 giờ  
**Cấp độ:** BEGINNER  
**Mục tiêu:** Hiểu và làm việc với Docker images và containers

**Nội dung chính:**
- Image là gì? Container là gì? Sự khác biệt?
- Docker commands: `pull`, `run`, `ps`, `stop`, `rm`, `images`
- Container lifecycle
- Docker Hub và public images

**Prerequisites:** [Lesson 01]

→ [Đọc bài này](_sub-lessons/02-Images-Containers/lesson.md)

---

### 🟡 [Lesson 03: Dockerfile Basics](_sub-lessons/03-Dockerfile-Basics/)

**Thời gian:** 1.5 giờ  
**Cấp độ:** INTERMEDIATE  
**Mục tiêu:** Viết Dockerfile để build custom images

**Nội dung chính:**
- Dockerfile syntax và directives (`FROM`, `RUN`, `COPY`, `CMD`, `ENTRYPOINT`, `EXPOSE`, `ENV`)
- Build image với `docker build`
- Best practices: layer caching, .dockerignore, multi-stage builds
- Optimizing image size

**Prerequisites:** [Lesson 02]

→ [Đọc bài này](_sub-lessons/03-Dockerfile-Basics/lesson.md)

---

### 🔴 [Lesson 04: Advanced Topics](_sub-lessons/04-Advanced/)

**Thời gian:** 2-3 giờ  
**Cấp độ:** ADVANCED  
**Mục tiêu:** Master Docker advanced topics cho production

**Nội dung chính:**
- Multi-stage builds chi tiết (Node.js, Go, Python)
- Layer caching optimization với BuildKit
- Docker Compose advanced (healthcheck, resource limits, logging, YAML anchors)
- Networking deep dive (custom networks, DNS, iptables)
- Volumes & storage (backup/restore, tmpfs)
- Security best practices (capabilities, read-only, scanning)
- Multi-architecture builds (amd64, arm64)
- Debugging containers (distroless, side-car pattern)
- Production Dockerfile templates

**Prerequisites:** [Lesson 03]

→ [Đọc bài này](_sub-lessons/04-Advanced/lesson.md)

---

## 🧪 Tài Nguyên Bổ Sung

### Quiz Tổng Hợp

Sau khi hoàn thành tất cả bài học, hãy làm [Docker Fundamentals Quiz](_quizzes/docker-fundamentals-quiz.md) để kiểm tra kiến thức.

### Projects Thực Hành

1. **[Mini Project] Dockerize một Node.js/Python app** — Xem [`_projects/simple-webapp-dockerized.md`](_projects/simple-webapp-dockerized.md)

2. **[Advanced] Multi-container app với Docker Compose** — Sẽ được thêm sau

---

## 🔄 Lộ Trình Đề Xuất

**Để học Docker hiệu quả nhất, hãy làm theo thứ tự:**

```
Lesson 01 → Lesson 02 → Lesson 03 → Lesson 04 → Quiz → Mini Project
```

**Thời gian ước tính tổng cộng:** 6-7 giờ

---

## 📊 Tiến Độ Học

Sử dụng checklist này để theo dõi tiến độ của bạn:

- [ ] Hoàn thành Lesson 01
- [ ] Hoàn thành Lesson 02
- [ ] Hoàn thành Lesson 03
- [ ] Hoàn thành Lesson 04 (Advanced)
- [ ] Hoàn thành Quiz với score > 80%
- [ ] Hoàn thành Mini Project

---

## ❓ Cần Trợ Giúp?

- **Bị kẹt ở bài nào?** → Vào file bài học đó và tìm phần "Common Pitfalls" hoặc "Hints"
- **Cần giải thích thêm?** → Đọc官方 documentation trong phần "Further Reading" của mỗi bài
- **Bug/không hiểu gì?** → Mở issue trong repository để hỏi cộng đồng

---

## 🔗 Liên Kết Nhanh

- [Official Docker Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Cheatsheet](https://dockerlabs.collabnix.com/docker/cheatsheet/)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
