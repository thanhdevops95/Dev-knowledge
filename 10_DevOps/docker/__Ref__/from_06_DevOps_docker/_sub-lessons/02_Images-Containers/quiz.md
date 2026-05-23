# 🐳 Docker — Images & Containers — Bài Tập Trắc Nghiệm

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)
- **Total Questions:** 10
- **Passing Score:** 70% (7/10 correct)
- **Estimated Time:** 12 phút

---

## ❓ Câu Hỏi

### Câu 1

**Câu hỏi:** Command nào để list tất cả Docker images local?

A. `docker list`  
B. `docker ps`  
C. `docker images`  
D. `docker image ls`

**Đáp án đúng:** C (D cũng đúng, `docker image ls` là command mới)

---

### Câu 2

**Câu hỏi:** Command nào để chạy container trong background?

A. `docker run alpine`  
B. `docker run -d alpine`  
C. `docker start alpine`  
D. `docker create alpine`

**Đáp án đúng:** B

---

### Câu 3

**Câu hỏi:** Container với `-p 8080:80` nghĩa là gì?

A. Host port 80 maps đến container port 8080  
B. Host port 8080 maps đến container port 80  
C. Expose container port 8080 ra host port 80  
D. Không có ý nghĩa gì

**Đáp án đúng:** B

---

### Câu 4

**Câu hỏi:** Lệnh nào để exec vào container đang chạy?

A. `docker into <container>`  
B. `docker exec -it <container> /bin/bash`  
C. `docker attach <container>`  
D. `docker shell <container>`

**Đáp án đúng:** B

---

### Câu 5

**Câu hỏi:** `docker ps` hiển thị gì?

A. Tất cả containers (running + stopped)  
B. Chỉ containers đang chạy  
C. Tất cả Docker images  
D. Docker system info

**Đáp án đúng:** B

---

### Câu 6

**Câu hỏi:** Docker image là read-only. Container là?

A. Read-only too  
B. Read-write (có writable layer)  
C. Append-only  
D. Tùy thuộc vào image

**Đáp án đúng:** B

---

### Câu 7

**Câu hỏi:** Lệnh nào để xem logs của container?

A. `docker log <container>`  
B. `docker logs <container>`  
C. `docker cat <container>`  
D. `docker inspect <container>`

**Đáp án đúng:** B

---

### Câu 8

**Câu hỏi:** Khi container exit, writable layer có giữ lại không?

A. Có, writable layer vẫn tồn tại  
B. Không, mất hết  
C. Chỉ giữ lại nếu dùng `docker commit`  
D. Chỉ giữ lại nếu dùng volume

**Đáp án đúng:** A (nhưng nếu `docker rm` container thì writable layer bị xóa theo)

---

### Câu 9

**Câu hỏi:** Docker Hub là?

A. Docker's official public registry  
B. Docker's official documentation site  
C. Docker's CLI tool  
D. Docker's virtualization engine

**Đáp án đúng:** A

---

### Câu 10

**Câu hỏi:** Command nào để stop tất cả running containers?

A. `docker stop --all`  
B. `docker stop $(docker ps -q)`  
C. `docker killall`  
D. `docker stop all`

**Đáp án đúng:** B

---

## 📊 Key

| Câu | Đáp án |
|-----|--------|
| 1 | C |
| 2 | B |
| 3 | B |
| 4 | B |
| 5 | B |
| 6 | B |
| 7 | B |
| 8 | A |
| 9 | A |
| 10 | B |

---

## 🎓 Đánh Giá

- **Pass:** ≥7/10 (70%)
- **Excellent:** 10/10

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
