# 🐳 Docker — Installation & Setup — Checklist Tự Đánh Giá

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)
- **Purpose:** Đảm bảo bạn đã nắm vững kiến thức installation và setup Docker

---

## 🎯 Mục Tiêu

Dùng checklist này để tự đánh giá xem bạn đã sẵn sàng chuyển sang bài học tiếp theo chưa.

---

## ✅ Danh Sách Kiểm Tra

### Phần 1: Installation

- [ ] Tôi đã cài đặt Docker Desktop (Mac/Windows) HOẶC Docker Engine (Linux)
- [ ] Docker Desktop/Docker Engine đang chạy (whale icon trên taskbar/menu bar)
- [ ] `docker --version` chạy thành công và hiển thị version number
- [ ] `docker info` chạy không lỗi và hiển thị system information
- [ ] `docker run hello-world` chạy thành công và in ra "Hello from Docker!"

### Phần 2: Architecture Understanding

- [ ] Tôi có thể giải thích sự khác biệt giữa Docker Client và Docker Daemon
- [ ] Tôi hiểu Docker Desktop chạy trong VM trên Mac/Windows
- [ ] Tôi hiểu tại sao trên Linux không cần VM
- [ ] Tôi biết Docker sử dụng Linux kernel features (cgroups, namespaces)
- [ ] Tôi phân biệt được Image vs Container

### Phần 3: Docker Commands

- [ ] Tôi biết cách dùng `docker run` để chạy container
- [ ] Tôi biết cách dùng `docker ps` để xem containers đang chạy
- [ ] Tôi biết cách dùng `docker ps -a` để xem tất cả containers
- [ ] Tôi biết cách dùng `docker images` để xem local images
- [ ] Tôi biết cách dùng `docker stop` và `docker rm` để dừng và xóa container

### Phần 4: Docker Desktop UI (Mac/Windows users only)

- [ ] Tôi biết cách mở Docker Desktop application
- [ ] Tôi biết cách vào Settings → Resources để xem CPU, Memory allocation
- [ ] Tôi biết cách xem list containers trong Dashboard
- [ ] Tôi biết cách stop/start container từ UI

### Phần 5: Troubleshooting

- [ ] Tôi biết cách xử lý lỗi "Cannot connect to the Docker daemon"
- [ ] Tôi biết cách xử lý lỗi "Permission denied" trên Linux (thêm user vào docker group)
- [ ] Tôi biết cách reset Docker Desktop nếu gặp vấn đề

---

## 🔍 Tự Đánh Giá

Sau khi hoàn thành checklist:

**Nếu tất cả đều check ✓:**
→ 🎉 **Tuyệt vời!** Bạn đã sẵn sàng chuyển sang bài học tiếp theo: [Images & Containers](../02-Images-Containers/lesson.md)

**Nếu có 1-2 chưa check:**
→ ⚠️ **Cần ôn tập lại** những điểm chưa hiểu. Đọc lại [lesson.md](../lesson.md) và làm lại [exercises.md](exercises.md).

**Nếu có >2 chưa check:**
→ ❌ **Cần học lại bài này từ đầu.** Docker là nền tảng quan trọng — đừng skip! Đọc kỹ lesson, làm tất cả exercises, rồi thử lại.

---

## 📚 Tài Nguyên Ôn Tập

Nếu bạn chưa tự tin về một số điểm:

- **Re-read:** [lesson.md](../lesson.md) — Tập trung vào Sections 2, 3, 5
- **Re-do:** [exercises.md](exercises.md) — Thực hành lại các hands-on exercises
- **Official Docs:** [Docker Get Started](https://docs.docker.com/get-started/)
- **Video:** [Docker Tutorial for Beginners](https://www.youtube.com/watch?v=3c-iBn73dDE) (YouTube, ~1 hour)

---

## 🎯 Mục Tiêu Tiếp Theo

Sau khi hoàn thành bài này, bạn sẽ chuyển sang:

**Lesson 02: Images & Containers**

Nội dung:
- Image là gì? Container là gì?
- Docker commands: `pull`, `run`, `ps`, `stop`, `rm`, `logs`
- Container lifecycle
- Docker Hub

**Thời gian dự kiến:** 1 giờ

---

**Hướng dẫn sử dụng:**
1. Check từng item trong checklist
2. Chỉ tick ✓ khi bạn **HOÀN TOÀN** tự tin (không đoán mò)
3. Sau khi xong, đánh giá theo phần "Tự Đánh Giá" ở trên

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
