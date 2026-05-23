# 🐳 Docker — Advanced Topics — Bài Tập Trắc Nghiệm

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)
- **Total Questions:** 15
- **Passing Score:** 70% (11/15 correct)
- **Estimated Time:** 20 phút

---

## ❓ Câu Hỏi

### Câu 1

**Multi-stage build dùng để làm gì?**

A. Tăng build speed  
B. Giảm image size bằng cách loại bỏ build dependencies  
C. Tăng security  
D. B và C

**Câu 2**

**Đâu là đúng về layer caching?**

A. Docker cache theo file size  
B. Mỗi instruction tạo 1 layer, cache hit nếu instruction và context không đổi  
C. Cache chỉ hoạt động với `RUN` instructions  
D. Không có cache trong Docker

**Câu 3**

**Docker Compose `depends_on` với `condition: service_healthy` nghĩa là gì?**

A. Chờ container start  
B. Chờ healthcheck pass  
C. Không chờ gì cả  
D. Chờ volume sẵn sàng

**Câu 4**

**Khi nào nên dùng `COPY` thay vì `ADD`?**

A. Luôn dùng `COPY`  
B. Chỉ dùng `ADD` khi cần unpack tarball hoặc download URLs  
C. `ADD` nhanh hơn  
D. `COPY` được deprecated

**Câu 5**

**Command nào để build multi-arch image?**

A. `docker build --platform`  
B. `docker buildx build --platform`  
C. `docker multi-build`  
D. `docker build --arch`

**Câu 6**

**`.dockerignore` dùng để?**

A. Exclude files từ container runtime  
B. Exclude files từ build context  
C. Ignore logs  
D. Nothing

**Câu 7**

**Security best practice nào sau đây là SAI?**

A. Run as non-root user  
B. Dùng `:latest` tag trong production  
C. Scan images cho vulnerabilities  
D. Dùng `--read-only` filesystem nếu có thể

**Câu 8**

**Làm thế nào để backup một Docker volume?**

A. `docker volume backup`  
B. `docker run --rm -v volume:/source -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /source .`  
C. `docker cp`  
D. Không thể backup volume

**Câu 9**

**BuildKit cache mount dùng để làm gì?**

A. Cache Docker layers  
B. Persist package manager cache giữa các builds  
C. Cache container logs  
D. Cache image pushes

**Câu 10**

**Docker network type nào chia sẻ host network stack?**

A. `bridge`  
B. `host`  
C. `overlay`  
D. `macvlan`

**Câu 11**

**Lệnh nào để exec vào container với interactive terminal?**

A. `docker exec container sh`  
B. `docker exec -it container /bin/bash`  
C. `docker shell container`  
D. A và B đều đúng

**Câu 12**

**`docker stats` dùng để?**

A. Xem container logs  
B. Xem real-time CPU/RAM usage  
C. Xem network stats  
D. Xem disk usage

**Câu 13**

**Làm thế nào để scan image với Trivy?**

A. `trivy scan image`  
B. `trivy image <image>`  
C. `docker scan`  
D. `security scan`

**Câu 14**

**`dumb-init` dùng để làm gì trong Dockerfile?**

A. Khởi tạo environment  
B. Proper signal handling cho PID 1  
C. Tạo user  
D. Cleanup tmp files

**Câu 15**

**Port mapping `-p 8080:80` nghĩa là?**

A. Container port 8080 → Host port 80  
B. Host port 8080 → Container port 80  
C. Expose port 8080  
D. Expose port 80

---

## 📊 Answer Key

| Câu | Đáp án |
|-----|--------|
| 1 | D |
| 2 | B |
| 3 | B |
| 4 | B |
| 5 | B |
| 6 | B |
| 7 | B |
| 8 | B |
| 9 | B |
| 10 | B |
| 11 | D |
| 12 | B |
| 13 | B |
| 14 | B |
| 15 | B |

---

## 🎓 Đánh Giá

- **Pass:** ≥11/15 (73%)
- **Excellent:** 14-15/15
- **Cần ôn lại:** 9-10/15
- **Học lại từ đầu:** <9

---

**Next:** Nếu pass → [Projects](../_projects/) hoặc [Resources](../_resources/)

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
