# 🐳 Docker — Dockerfile Basics — Bài Tập Trắc Nghiệm

---

## 📋 Metadata

- **Parent Lesson:** [../lesson.md](../lesson.md)
- **Total Questions:** 12
- **Passing Score:** 70% (9/12 correct)
- **Estimated Time:** 15 phút

---

## ❓ Câu Hỏi

### Câu 1

**Câu hỏi:** Instruction nào trong Dockerfile chỉ là documentation, không tạo layer?

A. `FROM`  
B. `RUN`  
C. `EXPOSE`  
D. `COPY`

**Đáp án đúng:** C

**Giải thích:** `EXPOSE` chỉ là metadata, không tạo layer và không publish port — chỉ document which ports nên được exposed.

---

### Câu 2

**Câu hỏi:** Lệnh nào để build Docker image từ Dockerfile?

A. `docker create`  
B. `docker build`  
C. `docker make`  
D. `docker image build`

**Đáp án đúng:** B (D cũng đúng: `docker image build`)

---

### Câu 3

**Câu hỏi:** `COPY` và `ADD` khác nhau thế nào?

A. Không có khác biệt  
B. `ADD` có thể unpack compressed files và download từ URLs  
C. `COPY` nhanh hơn  
D. `ADD` được deprecated

**Đáp án đúng:** B

---

### Câu 4

**Câu hỏi:** Exec form của CMD là gì?

A. `CMD python app.py`  
B. `CMD ["python", "app.py"]`  
C. `CMD -c "python app.py"`  
D. `CMD { "exec": "python", "args": ["app.py"] }`

**Đáp án đúng:** B

---

### Câu 5

**Câu hỏi:** Multi-stage build dùng để làm gì?

A. Tăng security  
B. Giảm image size bằng cách loại bỏ build dependencies  
C. Tăng build speed  
D. Tạo multiple images từ 1 Dockerfile

**Đáp án đúng:** B

---

### Câu 6

**Câu hỏi:** `.dockerignore` file dùng để làm gì?

A. Ignore files khi run container  
B. Exclude files từ build context  
C. Ignore logs  
D. Nothing, không có tác dụng

**Đáp án đúng:** B

---

### Câu 7

**Câu hỏi:** Docker layer caching hoạt động thế nào?

A. Mỗi instruction tạo 1 layer, cache hit nếu instruction và context không đổi  
B. Cache toàn bộ image  
C. Không có cache  
D. Cache theo file size

**Đáp án đúng:** A

---

### Câu 8

**Câu hỏi:** Để chạy container với non-root user, dùng instruction nào?

A. `USER`  
B. `RUNUSER`  
C. `SETUSER`  
D. `--user` flag khi `docker run`

**Đáp án đúng:** A (D cũng đúng để override tại runtime)

---

### Câu 9

**Câu hỏi:** Base image nên dùng tag gì trong production?

A. `latest`  
B. `stable`  
C. Specific version tag (ví dụ: `node:18.17.0-alpine`)  
D. Bất kỳ tag nào cũng được

**Đáp án đúng:** C

---

### Câu 10

**Câu hỏi:** Command nào để tag một image?

A. `docker tag`  
B. `docker label`  
C. `docker rename`  
D. `docker tag-image`

**Đáp án đúng:** A

---

### Câu 11

**Câu hỏi:** `ENTRYPOINT` và `CMD` khác nhau thế nào?

A. `ENTRYPOINT` là required, `CMD` là optional  
B. `ENTRYPOINT` không bị override bởi `docker run` arguments  
C. `ENTRYPOINT` chỉ dùng được một lần  
D. Không có khác biệt

**Đáp án đúng:** B (gần đúng — `ENTRYPOINT` thiết lập executable, `CMD` là default args)

---

### Câu 12

**Câu hỏi:** Để clean up trong cùng RUN layer, làm gì?

A. Dùng `--no-install-recommends` với apt-get  
B. `apt-get clean && rm -rf /var/lib/apt/lists/*`  
C. Không cần làm gì  
D. Dùng `docker clean`

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
| 7 | A |
| 8 | A |
| 9 | C |
| 10 | A |
| 11 | B |
| 12 | B |

---

## 🎓 Đánh Giá

- **Pass:** ≥9/12 (75%)
- **Excellent:** 11-12/12

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
