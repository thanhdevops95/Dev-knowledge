# 🐳 Docker — Installation & Setup — Bài Tập Trắc Nghiệm

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)
- **Total Questions:** 8
- **Passing Score:** 70% (6/8 correct)
- **Estimated Time:** 10 phút

---

## 🎯 Mục Tiêu

Kiểm tra kiến thức về Docker installation, architecture, và basic troubleshooting.

---

## ❓ Câu Hỏi

### Câu 1

**Câu hỏi:** Khi chạy `docker run hello-world` lần đầu tiên, điều gì xảy ra?

A. Container chạy và in ra "Hello from Docker!"  
B. Docker pull image `hello-world` từ Docker Hub, sau đó tạo và chạy container  
C. Docker chỉ in ra version của hello-world image  
D. Docker báo lỗi vì image chưa tồn tại

**Đáp án đúng:** B

**Giải thích:** Khi chạy `docker run`, Docker sẽ tự động pull image từ registry nếu image chưa có local. Sau khi pull xong, nó tạo container từ image và chạy container đó.

---

### Câu 2

**Câu hỏi:** Docker Desktop trên macOS sử dụng công nghệ nào để chạy Linux containers?

A. Native macOS kernel  
B. Hypervisor (HyperKit) chạy lightweight VM  
C. WSL2  
D. Chroot jail

**Đáp án đúng:** B

**Giải thích:** macOS không có Linux kernel nên Docker Desktop dùng HyperKit (lightweight hypervisor) để chạy một VM nhỏ, trong đó chạy Docker Engine. Windows dùng WSL2.

---

### Câu 3

**Câu hỏi:** Command nào để verify Docker đã install thành công?

A. `docker check`  
B. `docker version`  
C. `docker --version`  
D. `docker info` và `docker run hello-world`

**Đáp án đúng:** D

**Giải thích:** Cả `docker --version`, `docker version`, và `docker info` đều hiển thị thông tin version, nhưng cách tốt nhất để verify installation là chạy `docker run hello-world` — nó test cả pull, run, và logging.

---

### Câu 4

**Câu hỏi:** Docker Daemon là gì?

A. CLI tool bạn gõ command  
B. Background service quản lý Docker objects (images, containers, networks)  
C. Nơi lưu trữ Docker images  
D. Graphical user interface của Docker Desktop

**Đáp án đúng:** B

**Giải thích:** Docker Daemon (`dockerd`) là background service nghe requests từ Docker Client, và quản lý tất cả Docker objects. Nó chạy như systemd service trên Linux.

---

### Câu 5

**Câu hỏi:** Sau khi cài Docker Desktop trên Mac, bạn nên làm gì nếu gặp lỗi "Cannot connect to the Docker daemon"?

A. Restart máy tính  
B. Mở Docker Desktop app và đợi whale icon ổn định  
C. Chạy `sudo service docker start`  
D. Reinstall Docker

**Đáp án đúng:** B

**Giải thích:** Trên macOS/Windows, Docker Desktop cần được mở và khởi động đầy đủ. Whale icon trên menu bar/system tray phải chuyển từ "starting" sang "running" state trước khi có thể dùng được.

---

### Câu 6

**Câu hỏi:** Trên Linux, để Docker command chạy mà không cần `sudo`, bạn cần làm gì?

A. Chạy `docker enable-root`  
B. Thêm user vào `docker` group: `sudo usermod -aG docker $USER`  
C. Cấp execute permission cho `/usr/bin/docker`  
D. Không thể làm được (luôn cần sudo)

**Đáp án đúng:** B

**Giải thích:** Docker socket `/var/run/docker.sock` thuộc group `docker`. Bằng cách thêm user vào group `docker`, user đó sẽ có permission truy cập Docker socket mà không cần sudo. Cần logout và login lại để áp dụng.

---

### Câu 7

**Câu hỏi:** Docker Desktop Settings → Resources dùng để làm gì?

A. Configure network proxies  
B. Allocate CPU, Memory, và Disk cho Docker  
C. Set up Docker Hub credentials  
D. Enable Kubernetes cluster

**Đáp án đúng:** B

**Giải thích:** Docker Desktop cho phép bạn allocate resources (CPU cores, RAM, disk space) cho Docker engine/VM. Quan trọng vì nếu allocate quá ít, containers có thể out-of-memory.

---

### Câu 8

**Câu hỏi:** Lệnh nào để xem tất cả Docker images đã download?

A. `docker list`  
B. `docker images`  
C. `docker ps`  
D. `docker info`

**Đáp án đúng:** B

**Giải thích:** `docker images` hiển thị danh sách tất cả images local. `docker ps` hiển thị containers đang chạy. `docker ps -a` hiển thị tất cả containers (running + stopped).

---

## 📊 Key

| Câu | Đáp án | Chủ đề |
|-----|--------|--------|
| 1 | B | Docker run workflow |
| 2 | B | Docker Desktop architecture |
| 3 | D | Installation verification |
| 4 | B | Docker components |
| 5 | B | Troubleshooting (Mac/Windows) |
| 6 | B | Linux post-install |
| 7 | B | Docker Desktop settings |
| 8 | B | Docker images command |

---

## 🎓 Đánh Giá Kết Quả

### Tính điểm

- Mỗi câu đúng: 1 điểm (tổng 8 điểm)
- **Pass:** 6 điểm trở lên (70%)
- **Excellent:** 8 điểm (100%)

### Mức độ hiểu biết

| Điểm | Mức độ | Ý nghĩa |
|------|--------|---------|
| 8 | 🔥 Xuất sắc | Bạn hiểu rất tốt về Docker installation và architecture |
| 6-7 | 👍 Tốt | Bạn hiểu tốt, chỉ cần ôn lại vài điểm nhỏ |
| 4-5 | ⚠️ Trung bình | Bạn cần đọc lại bài học và thực hành thêm |
| < 4 | ❌ Yếu | Bạn cần đọc lại toàn bộ bài học từ đầu và làm lại exercises |

---

**Nếu bạn chưa đạt passing score:**
1. Đọc lại [lesson.md](../lesson.md)
2. Làm lại [exercises.md](exercises.md)
3. Thử lại quiz này

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
