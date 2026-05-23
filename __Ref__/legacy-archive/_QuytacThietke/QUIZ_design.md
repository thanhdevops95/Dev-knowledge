# QUIZ.md Design Specification

## 1. Purpose

- **Mục đích:** Cung cấp câu hỏi trắc nghiệm (10‑20 câu) để học viên ôn lại kiến thức và kiểm tra mức độ hiểu biết sau mỗi module.
- **Mục tiêu:** Đánh giá nhanh kiến thức lý thuyết, củng cố các khái niệm quan trọng.

---

## 2. File Header (Metadata)

```yaml
---
module: "X.Y"
title: "<Tên Module> – Quiz"
track: "<Số Track>"
version: "1.0"
last_updated: "YYYY-MM-DD"
total_questions: 15
passing_score: 70
time_limit: "15 minutes"
---
```

---

## 3. Required Sections (theo thứ tự bắt buộc)

### 3.1. Header

```markdown
## MODULE X.Y – <Tên Module> Quiz
```

### 3.2. Instructions (Hướng dẫn)

- Số lượng câu hỏi
- Thời gian làm bài
- Điểm pass
- Cách tính điểm

### 3.3. Questions (Câu hỏi)

Mỗi câu hỏi bao gồm:

- **Số thứ tự**
- **Nội dung câu hỏi**
- **4 lựa chọn** (A, B, C, D)
- **Đáp án** (ẩn bằng `<details>` tag)
- **Giải thích** (tại sao đáp án đó đúng)

### 3.4. Answer Key (Bảng đáp án)

- Bảng tổng hợp đáp án nhanh
- Ẩn bằng `<details>` tag

### 3.5. Scoring Guide (Hướng dẫn chấm điểm)

- Công thức tính điểm
- Điểm tối đa
- Điểm pass

### 3.6. References (Tham khảo)

- Link tới phần lý thuyết liên quan
- Tài liệu bổ sung

### 3.7. Navigation Footer ⭐ BẮT BUỘC

Cuối mỗi file phải có điều hướng:

```markdown
---

[⬅️ SOLUTIONS](./SOLUTIONS.md) | [📚 Mục lục](../../README.md) | [PROJECT ➡️](./PROJECT.md)
```

---

## 4. Question Types

| Loại | Mô tả | Ví dụ |
|------|-------|-------|
| **Knowledge** | Kiểm tra định nghĩa, khái niệm | "Docker image là gì?" |
| **Comprehension** | Kiểm tra hiểu biết | "Sự khác biệt giữa CMD và ENTRYPOINT?" |
| **Application** | Kiểm tra áp dụng | "Lệnh nào để xem logs của container?" |
| **Analysis** | Kiểm tra phân tích | "Lỗi nào xảy ra khi...?" |

---

## 5. Formatting Rules

| Thành phần | Quy tắc |
|------------|---------|
| Câu hỏi | Đánh số: 1., 2., 3... |
| Lựa chọn | A), B), C), D) |
| Đáp án | Ẩn trong `<details>` tag |
| Code trong câu hỏi | Dùng inline code `` `code` `` |

---

## 6. Style Guide

- **Câu hỏi rõ ràng:** Không mơ hồ, chỉ có 1 đáp án đúng
- **Lựa chọn cân bằng:** Độ dài tương đương, không có gợi ý
- **Giải thích ngắn gọn:** Giải thích tại sao đáp án đúng
- **Đa dạng:** Kết hợp nhiều loại câu hỏi

---

## 7. Review Checklist

- [ ] Đủ số lượng câu hỏi (10-20)
- [ ] Mỗi câu chỉ có 1 đáp án đúng
- [ ] Các lựa chọn không có gợi ý rõ ràng
- [ ] Có giải thích cho mỗi đáp án
- [ ] Đáp án được ẩn bằng `<details>` tag
- [ ] Bảng Answer Key đầy đủ
- [ ] **Có Navigation Footer cuối file** ⭐
- [ ] `last_updated` là ngày hiện tại

---

## 8. Do's and Don'ts

### ✅ Nên làm

- Câu hỏi phản ánh nội dung đã học
- Sắp xếp theo độ khó tăng dần
- Cung cấp giải thích chi tiết
- Đa dạng loại câu hỏi

### ❌ Không nên làm

- Câu hỏi mơ hồ, nhiều đáp án đúng
- Lựa chọn "All of the above" quá nhiều
- Đáp án quá dễ đoán
- Câu hỏi không liên quan đến module

---

## 9. Example Template (Copy-Paste)

```markdown
---
module: "1.4"
title: "Docker Fundamentals – Quiz"
track: "1"
version: "1.0"
last_updated: "2025-12-27"
total_questions: 15
passing_score: 70
time_limit: "15 minutes"
---

## MODULE 1.4 – Docker Fundamentals Quiz

### Instructions
- **Số lượng câu hỏi:** 15 câu
- **Thời gian:** 15 phút
- **Điểm pass:** 70% (đúng ít nhất 11/15 câu)
- **Cách tính:** Mỗi câu đúng = 1 điểm, không trừ điểm câu sai

---

### Questions

#### 1. Docker container là gì?

A) Một máy ảo hoàn chỉnh với hệ điều hành riêng  
B) Một instance đang chạy của Docker image  
C) Một file text chứa các lệnh build  
D) Một registry lưu trữ images

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** Container là một instance đang chạy của image. Image là template read-only, còn container là môi trường runtime thực tế.
</details>

---

#### 2. Dockerfile instruction nào được sử dụng để chỉ định base image?

A) `BASE`  
B) `IMAGE`  
C) `FROM`  
D) `SOURCE`

<details>
<summary>Xem đáp án</summary>

**Đáp án: C**

**Giải thích:** `FROM` là instruction đầu tiên trong Dockerfile, dùng để chỉ định base image mà image mới sẽ được xây dựng từ đó.
</details>

---

#### 3. Lệnh nào dùng để xem danh sách tất cả containers (bao gồm cả stopped)?

A) `docker ps`  
B) `docker ps -a`  
C) `docker containers`  
D) `docker list --all`

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** `docker ps` chỉ hiển thị containers đang chạy. Thêm flag `-a` (hoặc `--all`) để hiển thị tất cả containers.
</details>

---

#### 4. Sự khác biệt chính giữa `CMD` và `ENTRYPOINT` là gì?

A) `CMD` không thể bị override, `ENTRYPOINT` có thể  
B) `ENTRYPOINT` không thể bị override, `CMD` có thể  
C) `CMD` cho commands, `ENTRYPOINT` cho arguments  
D) Không có sự khác biệt

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** `CMD` cung cấp default command có thể bị override khi chạy `docker run`. `ENTRYPOINT` định nghĩa command chính không thể bị override (trừ khi dùng `--entrypoint` flag).
</details>

---

#### 5. Port mapping `-p 8080:80` có nghĩa là gì?

A) Container port 8080 map tới host port 80  
B) Host port 8080 map tới container port 80  
C) Cả hai ports đều là 8080  
D) Cả hai ports đều là 80

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** Syntax là `-p <host_port>:<container_port>`. Vậy 8080:80 nghĩa là truy cập port 8080 trên host sẽ được forward tới port 80 trong container.
</details>

---

#### 6. Lệnh nào để build Docker image từ Dockerfile?

A) `docker create -t myimage .`  
B) `docker build -t myimage .`  
C) `docker make -t myimage .`  
D) `docker image myimage .`

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** `docker build` là lệnh để build image. Flag `-t` dùng để đặt tên và tag cho image. `.` chỉ định build context (thư mục chứa Dockerfile).
</details>

---

#### 7. Docker volume được sử dụng để làm gì?

A) Tăng tốc độ build image  
B) Persist data và chia sẻ data giữa containers  
C) Caching layers  
D) Compress image size

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** Volumes là cơ chế để persist data bên ngoài container lifecycle và chia sẻ data giữa nhiều containers.
</details>

---

#### 8. Instruction nào dùng để set working directory trong Dockerfile?

A) `DIR`  
B) `CD`  
C) `WORKDIR`  
D) `SETDIR`

<details>
<summary>Xem đáp án</summary>

**Đáp án: C**

**Giải thích:** `WORKDIR` instruction set working directory cho các instructions tiếp theo như `RUN`, `CMD`, `COPY`, `ADD`.
</details>

---

#### 9. Lệnh nào để truy cập shell bên trong container đang chạy?

A) `docker shell container_id`  
B) `docker exec -it container_id /bin/sh`  
C) `docker enter container_id`  
D) `docker ssh container_id`

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** `docker exec` chạy lệnh trong container đang chạy. Flag `-it` (interactive + tty) cho phép tương tác với shell.
</details>

---

#### 10. Multi-stage build giúp gì?

A) Build nhiều images cùng lúc  
B) Giảm kích thước image cuối cùng  
C) Tăng tốc độ runtime  
D) Enable multi-threading

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** Multi-stage build cho phép sử dụng nhiều `FROM` statements. Chỉ copy artifacts cần thiết từ stage trước, giảm đáng kể kích thước image cuối.
</details>

---

#### 11. Docker Compose dùng để làm gì?

A) Build Docker images nhanh hơn  
B) Định nghĩa và chạy multi-container applications  
C) Deploy lên Kubernetes  
D) Scan vulnerabilities

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** Docker Compose là tool để định nghĩa và chạy multi-container applications bằng file YAML, giúp quản lý các services, networks, và volumes dễ dàng.
</details>

---

#### 12. Lệnh nào để xóa tất cả stopped containers?

A) `docker rm -all`  
B) `docker container prune`  
C) `docker clean containers`  
D) `docker delete stopped`

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** `docker container prune` xóa tất cả stopped containers. Tương tự có `docker image prune`, `docker volume prune`, và `docker system prune` cho cleanup toàn bộ.
</details>

---

#### 13. Layer caching trong Docker dựa trên gì?

A) Thời gian build  
B) Nội dung của instruction và các files  
C) Tên của image  
D) Số lượng containers

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** Docker cache mỗi layer dựa trên checksum của instruction và files liên quan. Nếu không có thay đổi, Docker reuse cached layer.
</details>

---

#### 14. `EXPOSE` instruction trong Dockerfile làm gì?

A) Tự động publish port ra host  
B) Document port mà container sẽ listen  
C) Block access tới port  
D) Create firewall rule

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** `EXPOSE` chỉ là documentation, không tự động publish port. Cần dùng `-p` flag khi chạy `docker run` để thực sự map port.
</details>

---

#### 15. Lệnh nào để xem logs của container?

A) `docker log container_id`  
B) `docker logs container_id`  
C) `docker output container_id`  
D) `docker print container_id`

<details>
<summary>Xem đáp án</summary>

**Đáp án: B**

**Giải thích:** `docker logs` (số nhiều) hiển thị logs của container. Thêm `-f` để follow logs realtime.
</details>

---

### Answer Key

<details>
<summary>Xem bảng đáp án</summary>

| Câu | Đáp án | Câu | Đáp án |
|-----|--------|-----|--------|
| 1 | B | 9 | B |
| 2 | C | 10 | B |
| 3 | B | 11 | B |
| 4 | B | 12 | B |
| 5 | B | 13 | B |
| 6 | B | 14 | B |
| 7 | B | 15 | B |
| 8 | C | | |

</details>

---

### Scoring Guide

| Số câu đúng | Điểm | Đánh giá |
|-------------|------|----------|
| 14-15 | 93-100% | Xuất sắc ⭐⭐⭐ |
| 12-13 | 80-87% | Tốt ⭐⭐ |
| 11 | 73% | Pass ⭐ |
| < 11 | < 70% | Cần ôn lại |

---

### References
- [README.md - MODULE 1.4](../Track1_Foundation_StaticWeb/1.4_Docker_Fundamentals/README.md)
- [Docker Official Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [GLOSSARY](../../resources/GLOSSARY.md)

---

[⬅️ SOLUTIONS](./SOLUTIONS.md) | [📚 Mục lục](../../README.md) | [PROJECT ➡️](./PROJECT.md)
```

---

*File này là chuẩn mẫu cho mọi `QUIZ.md` trong khoá học DevOps.*
