# 🐳 Docker — Containerization Platform

---

## 📋 Metadata

- **Category:** DevOps
- **Subcategory:** Containerization
- **Level:** `[BEGINNER]`
- **Total Sub-lessons:** 3 (có thể mở rộng thêm)
- **Estimated Total Time:** 4-5 giờ
- **Last Updated:** 30/04/2026
- **Author:** Mr.Rom

---

## 🎯 Giới Thiệu & Tại Sao Cần Học

### Vấn đề: "It works on my machine!"

Bạn đã bao giờ gặp tình huống này chưa?
- Code chạy tốt trên máy của bạn
- Khi chuyển sang máy khác (teammate, staging, production) → **"It works on my machine!"** 💥
- Các dependency môi trường (phiên bản Node, Python, libraries,...) khác biệt
- Mất hàng giờ để debug tại sao lại lỗi

### Giải pháp: Docker

**Docker** là nền tảng containerization giúp đóng gói ứng dụng và tất cả dependencies của nó vào một **container** — đảm bảo chạy giống hệt nhau trên mọi môi trường.

```
┌─────────────────────────────────────────────┐
│   Your App + Dependencies + OS Libraries   │
│              → Docker Image → Container     │
│              (Portable, Consistent)        │
└─────────────────────────────────────────────┘
```

### Kết quả expected

Sau khi học xong chủ đề này, bạn sẽ có thể:

- ✅ Cài đặt Docker Desktop trên máy tính
- ✅ Hiểu và phân biệt **Image** vs **Container**
- ✅ Tạo Dockerfile để build custom image
- ✅ Chạy, quản lý container (start, stop, logs, exec)
- ✅ Sử dụng Docker Compose cho multi-container apps
- ✅ Áp dụng Docker best practices vào thực tế

---

## 🗺️ Tổng Quan Cấu Trúc Bài Học

Chủ đề Docker được chia thành **3 bài học**, mỗi bài tập trung vào một khía cạnh cụ thể:

| # | Bài Học | Mô Tả Ngắn | Thời Gian | Cấp Độ |
|---|---------|------------|-----------|---------|
| 01 | [Installation & Setup](_sub-lessons/01-Installation-Setup/) | Cài đặt Docker, verify, cấu hình cơ bản | 45 phút | BEGINNER |
| 02 | [Images & Containers](_sub-lessons/02-Images-Containers/) | Hiểu và sử dụng images/containers, Docker commands | 1 giờ | BEGINNER |
| 03 | [Dockerfile Basics](_sub-lessons/03-Dockerfile-Basics/) | Viết Dockerfile, best practices, multi-stage builds | 1.5 giờ | INTERMEDIATE |

**Tổng thời gian ước tính:** ~3-4 giờ

---

## 📚 Bài Học Chi Tiết

### 1. [Installation & Setup](_sub-lessons/01-Installation-Setup/)

**Mục tiêu:** Cài đặt Docker Desktop, hiểu architecture cơ bản, và verify installation

**Prerequisites:** Không cần kiến thức trước

→ [Đọc bài này](_sub-lessons/01-Installation-Setup/lesson.md)

---

### 2. [Images & Containers](_sub-lessons/02-Images-Containers/)

**Mục tiêu:** Hiểu và làm việc với Docker images và containers, sử dụng Docker CLI

**Prerequisites:** [Lesson 01]

→ [Đọc bài này](_sub-lessons/02-Images-Containers/lesson.md)

---

### 3. [Dockerfile Basics](_sub-lessons/03-Dockerfile-Basics/)

**Mục tiêu:** Viết Dockerfile để build custom images, hiểu best practices

**Prerequisites:** [Lesson 02]

→ [Đọc bài này](_sub-lessons/03-Dockerfile-Basics/lesson.md)

---

## 🧪 Bài Tập Tổng Hợp

Sau khi hoàn thành tất cả các bài con:

1. **Quiz tổng hợp Docker:** Xem file [`_quizzes/docker-fundamentals-quiz.md`](_quizzes/docker-fundamentals-quiz.md)
2. **Mini-project:** Xem file [`_projects/simple-webapp-dockerized.md`](_projects/simple-webapp-dockerized.md)

---

## 🔗 Liên Kết Đến Các Chủ Đề Khác

### Prerequisites (Cần học trước)

- Nếu chưa biết **Linux command line**, học [Linux Basics](../fundamentals/linux-basics.md) trước.
- Nếu chưa hiểu **terminal/CLI**, học [Terminal 101](../fundamentals/terminal-basics.md).

### Next Steps (Học sau)

Sau khi thành thạo Docker, bạn có thể học:
- [Kubernetes](../kubernetes/) — Orchestration cho production
- [CI/CD với Docker](../ci-cd/docker-ci-cd.md) — Tự động hóa build và deploy
- [DevOps Core](../devops-core/) — Infrastructure as Code, Monitoring

---

## 📖 Tài Nguyên & Tham Khảo

### Official Documentation

- [Docker Official Docs](https://docs.docker.com/)
- [Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Docker CLI Reference](https://docs.docker.com/engine/reference/commandline/cli/)

### Articles & Tutorials

- [Docker — From Zero to Hero](https://docker-curriculum.com/)
- [Play with Docker](https://labs.play-with-docker.com/) — Interactive labs miễn phí

### Books

- "The Docker Book" by James Turnbull
- "Docker Deep Dive" by Nigel Poulton

---

## 💡 Lưu Ý & Common Pitfalls

### Những lỗi thường gặp

- ❌ **Không nên:** Chạy container với `--privileged` mode trừ khi thực sự cần thiết
- ❌ **Không nên:** Lưu data bên trong container (container die thì data mất)
- ✅ **Nên làm:** Dùng volumes cho persistent data
- ✅ **Nên làm:** Dùng `.dockerignore` file để exclude files không cần thiết
- ✅ **Nên làm:** Không chạy process作为 root trong container (dùng `USER` directive)

### Tips

- 💡 Dùng `docker system prune` để clean unused resources
- 💡 Dùng `docker logs <container>` để xem logs của container
- 💡 Dùng `docker exec -it <container> /bin/bash` để vào shell của container

---

## 🤝 Đóng Góp & Feedback

Nếu bạn thấy thiếu sót, sai sót, hoặc có góp ý cải thiện bài học này:

1. Fork repository
2. Tạo Pull Request với cải tiến
3. Hoặc mở Issue để thảo luận

Xem chi tiết tại [CONTRIBUTING.md](../../CONTRIBUTING.md)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Ngày tạo:** 30/04/2026  
**Cập nhật lần cuối:** 30/04/2026
