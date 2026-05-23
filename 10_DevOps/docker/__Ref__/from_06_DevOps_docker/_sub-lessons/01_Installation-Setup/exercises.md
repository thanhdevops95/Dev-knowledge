# 🐳 Docker — Installation & Setup — Bài Tập Thực Hành

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)
- **Type:** `[Exercise]`
- **Difficulty:** `[Easy]`
- **Estimated Time:** 30 phút
- **Prerequisites:** None (sau khi đã cài Docker)

---

## 🎯 Mục Tiêu

Luyện tập các thao tác cài đặt và verify Docker installation. Đảm bảo bạn đã sẵn sàng chuyển sang bài học tiếp theo.

---

## 📝 Bài Tập

### Bài 1: Verify Docker Installation

**Mục tiêu:** Xác nhận Docker đã cài đặt và chạy đúng

**Tasks:**
1. Mở terminal (macOS/Linux) hoặc PowerShell/CMD (Windows)
2. Chạy lệnh: `docker --version`
3. Ghi ra **toàn bộ output** vào đây:
   ```
   [Output của bạn]
   ```
4. Chạy lệnh: `docker version` (chú ý: có cả Client và Server sections)
5. Screenshot hoặc ghi lại:
   - Client version: ________
   - Server version: ________
   - API version: ________

**Success Criteria:**
- ✅ Output hiển thị version number (ví dụ: Docker version 24.0.5)
- ✅ Không có error message

---

### Bài 2: Run hello-world Container

**Mục tiêu:** Chạy first container và hiểu output

**Tasks:**
1. Chạy: `docker run hello-world`
2. Đọc output thật kỹ
3. Trả lời câu hỏi:
   - **Q1:** Container `hello-world` làm gì khi chạy?
     ```
     [Trả lời]
     ```
   - **Q2:** Docker đã làm gì khi bạn chạy lệnh này? (Pull image? Run container? Both?)
     ```
     [Trả lời]
     ```
   - **Q3:** Sau khi container chạy xong, nó còn tồn tại không? Kiểm tra bằng `docker ps -a`
     ```
     [Trả lời]
     ```

**Success Criteria:**
- ✅ Thấy message "Hello from Docker!"
- ✅ Hiểu được flow: Pull (nếu chưa có) → Create container → Run → Exit

---

### Bài 3: Explore Docker Desktop UI (Optional)

**Mục tiêu:** Làm quen với Docker Desktop interface (chỉ áp dụng nếu dùng Desktop)

**Tasks:**
1. Mở Docker Desktop app (nếu chưa chạy)
2. Click vào Settings (gear icon)
3. Đi đến **Resources** tab
4. Screenshot hoặc ghi lại:
   - CPUs allocated: ___
   - Memory allocated: ___ GB
   - Disk image size: ___ GB
5. Thử click vào **Containers / Apps** tab
6. Ghi ra: Bạn thấy bao nhiêu container đang chạy? _____

**Success Criteria:**
- ✅ Biết cách mở Settings
- ✅ Biết cách xem resources allocation
- ✅ Biết cách xem list containers

---

### Bài 4: Docker Info Command

**Mục tiêu:** Dùng `docker info` để xem thông tin system

**Tasks:**
1. Chạy: `docker info`
2. Output rất dài. Tìm và ghi ra:
   - `Operating System:` _______________
   - `Kernel Version:` _______________
   - `Number of CPUs:` _______________
   - `Total Memory:` _______________
3. Câu hỏi: Tại sao `docker info` lại quan trọng trong troubleshooting?
   ```
   [Trả lời]
   ```

**Success Criteria:**
- ✅ Biết cách đọc output của `docker info`
- ✅ Hiểu ý nghĩa của các thông tin cơ bản

---

### Bài 5: Test Docker Networking

**Mục tiêu:** Hiểu Docker networking cơ bản

**Tasks:**
1. Chạy container NGINX với port mapping:
   ```bash
   docker run -d -p 8080:80 --name test-nginx nginx:latest
   ```
2. Mở browser và truy cập: `http://localhost:8080`
3. Bạn thấy gì? __________________
4. Stop container:
   ```bash
   docker stop test-nginx
   docker rm test-nginx
   ```
5. Verify container đã bị xóa: `docker ps -a` (không thấy `test-nginx`)

**Success Criteria:**
- ✅ Container NGINX chạy và port 8080 accessible
- ✅ Biết cách stop và remove container

---

## 💡 Gợi Ý & Hints

### Hint cho Bài 2

Nếu `docker run hello-world` bị lỗi "Unable to find image":
- Docker tự động sẽ pull image nếu chưa có
- Kiểm tra internet connection
- Nếu network chậm, có thể pull trước: `docker pull hello-world`

### Hint cho Bài 5

- `-d` flag: Run container in background (detached mode)
- `-p 8080:80`: Port mapping — Host port 8080 → Container port 80
- `--name test-nginx`: Đặt tên container để dễ thao tác sau
- `nginx:latest`: Image name với tag

---

## ✅ Đánh Giá & Checklist

### Self-Evaluation

Checklist hoàn thành:

- [ ] Bài 1: Docker version command hoạt động
- [ ] Bài 2: hello-world container chạy thành công
- [ ] Bài 2: Tôi hiểu output của hello-world
- [ ] Bài 3: (Optional) Docker Desktop UI được explore
- [ ] Bài 4: docker info output được phân tích
- [ ] Bài 5: Nginx container chạy với port mapping
- [ ] Bài 5: Container được stop và remove đúng cách

### Success Criteria

**Pass:**
- ✅ Hoàn thành ít nhất 5/7 tasks
- ✅ Hiểu được Docker Client-Server model
- ✅ Biết cách chạy container cơ bản

**Excellent:**
- ⭐ Hoàn thành tất cả tasks
- ⭐ Hiểu sâu về Docker architecture
- ⭐ Biết cách troubleshoot basic issues

---

## 🔗 Liên Kết

- ← [Quay lại bài học](../lesson.md)
- → [Bài tiếp theo: Images & Containers](../../02-Images-Containers/lesson.md)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
