# 🐳 Docker — Fundamentals Quiz — Tổng Hợp

---

## 📋 Metadata

- **Parent Lesson:** [../README.md](../README.md)
- **Total Questions:** 25
- **Passing Score:** 70% (18/25 correct)
- **Estimated Time:** 25 phút
- **Covers:** Lessons 01, 02, 03

---

## 🎯 Mục Tiêu

Kiểm tra tổng hợp kiến thức Docker từ cơ bản đến trung cấp:
- Installation & Architecture
- Images & Containers
- Dockerfile & Best Practices

---

## ❓ Câu Hỏi

### Section 1: Installation & Architecture (Câu 1-8)

**Câu 1:** Docker Desktop trên macOS sử dụng công nghệ nào?

A. Native macOS kernel  
B. Hypervisor với lightweight VM  
C. WSL2  
D. Chroot jail

**Câu 2:** Docker Daemon là gì?

A. CLI tool  
B. Background service  
C. Registry  
D. Image builder

**Câu 3:** Command nào để verify Docker installation?

A. `docker --version`  
B. `docker info`  
C. `docker run hello-world`  
D. Tất cả đều đúng

**Câu 4:** Trên Linux, để chạy Docker command mà không cần `sudo`?

A. Chmod +x /usr/bin/docker  
B. Thêm user vào docker group  
C. Cài đặt Docker Desktop  
D. Impossible

**Câu 5:** Docker sử dụng isolation techniques nào của Linux?

A. Virtualization  
B. Cgroups và Namespaces  
C. SELinux only  
D. AppArmor only

**Câu 6:** Docker Desktop Settings → Resources dùng để?

A. Configure network  
B. Allocate CPU, Memory, Disk  
C. Set Docker Hub credentials  
D. Enable Kubernetes

**Câu 7:** Docker Client nói chuyện với Daemon qua?

A. Unix socket  
B. HTTP/HTTPS (REST API)  
C. Both A and B  
D. TCP socket only

**Câu 8:** Lỗi "Cannot connect to the Docker daemon" thường do?

A. Docker chưa start  
B. Permission issues  
C. Network issues  
D. A hoặc B

---

### Section 2: Images & Containers (Câu 9-16)

**Câu 9:** Image là gì?

A. Running instance  
B. Read-only template  
C. Writable layer  
D. Container snapshot

**Câu 10:** Container là?

A. Read-only template  
B. Writable instance của image  
C. Registry  
D. Build artifact

**Câu 11:** Command nào để list running containers?

A. `docker ps`  
B. `docker ps -a`  
C. `docker containers`  
D. `docker list`

**Câu 12:** Port mapping `-p 8080:80` nghĩa là?

A. Container port 8080 → Host port 80  
B. Host port 8080 → Container port 80  
C. Expose port 8080  
D. Expose port 80

**Câu 13:** Command nào để exec shell vào container?

A. `docker exec -it <container> /bin/bash`  
B. `docker shell <container>`  
C. `docker attach <container>`  
D. `docker into <container>`

**Câu 14:** `docker logs` dùng để?

A. Xem container logs  
B. Xem Docker daemon logs  
C. Xem build logs  
D. Xem image history

**Câu 15:** Container lifecycle — container stopped có thể?

A. Start lại với `docker start`  
B. Không thể start lại  
C. Chỉ có thể remove  
D. Phải rebuild từ image

**Câu 16:** Docker Hub là?

A. Official public registry  
B. Documentation site  
C. CLI tool  
D. Virtualization platform

---

### Section 3: Dockerfile & Build (Câu 17-25)

**Câu 17:** Instruction nào KHÔNG tạo layer?

A. `FROM`  
B. `RUN`  
C. `COPY`  
D. `EXPOSE`

**Câu 18:** `COPY` vs `ADD`?

A. Same  
B. `ADD` có thể unpack archives và download URLs  
C. `COPY` nhanh hơn  
D. `ADD` được deprecated

**Câu 19:** Exec form của CMD?

A. `CMD python app.py`  
B. `CMD ["python", "app.py"]`  
C. `CMD -c "python app.py"`  
D. B hoặc C đều được

**Câu 20:** Multi-stage build dùng để?

A. Parallel builds  
B. Reduce image size  
C. Increase security only  
D. B và C

**Câu 21:** `.dockerignore` dùng để?

A. Exclude files từ build context  
B. Exclude files từ container runtime  
C. Ignore Docker errors  
D. Nothing

**Câu 22:** Layer caching hoạt động thế nào?

A. Rebuild mọi lúc  
B. Cache nếu instruction và context không đổi  
C. Cache theo file size  
D. Không có cache

**Câu 23:** Để chạy container với non-root user?

A. `USER` directive trong Dockerfile  
B. `--user` flag khi `docker run`  
C. Both A and B  
D. Không thể

**Câu 24:** Best practice cho base image tag trong production?

A. `latest`  
B. `stable`  
C. Specific version  
D. Bất kỳ

**Câu 25:** Command để tag image?

A. `docker tag`  
B. `docker label`  
C. `docker rename`  
D. `docker image tag`

---

## 📊 Answer Key

| Câu | Đáp án |
|-----|--------|
| 1 | B |
| 2 | B |
| 3 | D |
| 4 | B |
| 5 | B |
| 6 | B |
| 7 | C |
| 8 | D |
| 9 | B |
| 10 | B |
| 11 | A |
| 12 | B |
| 13 | A |
| 14 | A |
| 15 | A |
| 16 | A |
| 17 | D |
| 18 | B |
| 19 | B |
| 20 | D |
| 21 | A |
| 22 | B |
| 23 | C |
| 24 | C |
| 25 | A |

---

## 🎓 Đánh Giá

| Score | Mức độ |
|-------|--------|
| 22-25 | 🔥 Expert |
| 18-21 | 👍 Proficient |
| 14-17 | ⚠️ Intermediate (cần ôn lại) |
| < 14 | ❌ Beginner (học lại từ đầu) |

---

**Next:** Nếu pass → [Mini Project](../_projects/simple-webapp-dockerized.md)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
