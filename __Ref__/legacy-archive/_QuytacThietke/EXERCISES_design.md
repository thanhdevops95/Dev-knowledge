# EXERCISES.md Design Specification

## 1. Purpose

- **Mục đích:** Cung cấp bài tập tình huống, thách thức để học viên tự suy luận và áp dụng kiến thức đã học.
- **Mục tiêu:** Củng cố lý thuyết, phát triển kỹ năng giải quyết vấn đề thực tế.
- **Lưu ý:** KHÔNG đưa đáp án trong file này (đáp án nằm trong SOLUTIONS.md).

---

## 2. File Header (Metadata)

```yaml
---
module: "X.Y"
title: "<Tên Module> – Exercises"
track: "<Số Track>"
version: "1.0"
last_updated: "YYYY-MM-DD"
difficulty: "Beginner | Intermediate | Advanced"
estimated_time: "30-60 minutes"
---
```

---

## 3. Required Sections (theo thứ tự bắt buộc)

### 3.1. Header

```markdown
## MODULE X.Y – <Tên Module> Exercises
```

### 3.2. Overview (Tổng quan)

- Số lượng bài tập
- Thời gian ước tính
- Mức độ khó
- Yêu cầu hoàn thành tối thiểu

### 3.3. Prerequisites (Yêu cầu trước khi làm)

- Checklist các kiến thức/công cụ cần có

### 3.4. Exercises (Các bài tập)

Mỗi bài tập bao gồm:

- **Exercise ID & Title**
- **Difficulty Level** (⭐ Easy, ⭐⭐ Medium, ⭐⭐⭐ Hard)
- **Scenario** (Tình huống thực tế)
- **Requirements** (Yêu cầu cụ thể)
- **Constraints** (Ràng buộc)
- **Hints** (Gợi ý - không tiết lộ đáp án)
- **Expected Deliverables** (Sản phẩm cần nộp)

### 3.5. Evaluation Criteria (Tiêu chí đánh giá)

- Bảng điểm cho từng tiêu chí
- Điểm tối đa và điểm tối thiểu để pass

### 3.6. Submission Guidelines (Hướng dẫn nộp bài)

- Format file cần nộp
- Cách đặt tên file
- Nơi nộp bài

### 3.7. Navigation Footer ⭐ BẮT BUỘC

Cuối mỗi file phải có điều hướng:

```markdown
---

[⬅️ LABS](./LABS.md) | [📚 Mục lục](../../README.md) | [SOLUTIONS ➡️](./SOLUTIONS.md)
```

---

## 4. Formatting Rules

| Thành phần | Quy tắc |
|------------|---------|
| Tiêu đề | `##` cho chính, `###` cho mục con |
| Bài tập | Đánh số: Exercise 1, Exercise 2... |
| Mức độ khó | Dùng emoji: ⭐, ⭐⭐, ⭐⭐⭐ |
| Code | Block với ngôn ngữ phù hợp |
| Hints | Dùng `<details>` tag để ẩn |

---

## 5. Style Guide

- **Tình huống thực tế:** Gắn với công việc DevOps hàng ngày
- **Rõ ràng:** Yêu cầu không mơ hồ, có thể kiểm tra được
- **Thử thách:** Không quá dễ, không quá khó
- **Gợi ý:** Đủ để hướng dẫn, không tiết lộ đáp án

---

## 6. Review Checklist

- [ ] Mỗi bài tập có đầy đủ: Scenario, Requirements, Constraints, Hints
- [ ] Mức độ khó rõ ràng và phù hợp với module
- [ ] Yêu cầu cụ thể, có thể kiểm tra được
- [ ] Hints không tiết lộ đáp án
- [ ] Tiêu chí đánh giá công bằng và chi tiết
- [ ] **Có Navigation Footer cuối file** ⭐
- [ ] `last_updated` là ngày hiện tại

---

## 7. Do's and Don'ts

### ✅ Nên làm

- Đặt tình huống thực tế, gần gũi với công việc
- Cung cấp ràng buộc rõ ràng
- Cho gợi ý từng bước (không phải đáp án)
- Đa dạng mức độ khó

### ❌ Không nên làm

- Đặt yêu cầu mơ hồ, không kiểm tra được
- Đưa đáp án trong đề bài
- Bỏ qua tiêu chí đánh giá
- Thiếu thông tin về môi trường/công cụ cần thiết

---

## 8. Example Template (Copy-Paste)

```markdown
---
module: "1.4"
title: "Docker Fundamentals – Exercises"
track: "1"
version: "1.0"
last_updated: "2025-12-27"
difficulty: "Beginner to Intermediate"
estimated_time: "60-90 minutes"
---

## MODULE 1.4 – Docker Fundamentals Exercises

### Overview
- **Số lượng bài tập:** 3 bài
- **Thời gian ước tính:** 60-90 phút
- **Mức độ khó:** Từ Beginner đến Intermediate
- **Yêu cầu:** Hoàn thành ít nhất 2/3 bài tập

---

### Prerequisites
- [ ] Đã hoàn thành phần lý thuyết MODULE 1.4
- [ ] Docker Desktop đã cài đặt và chạy được
- [ ] Có tài khoản Docker Hub
- [ ] Terminal/Command Line hoạt động

---

### Exercise 1: Build Your First Docker Image ⭐

#### Scenario
Bạn là DevOps Engineer mới vào công ty ABC. Team lead giao cho bạn task đầu tiên: đóng gói một ứng dụng Node.js đơn giản thành Docker image.

#### Requirements
1. Tạo một thư mục mới tên `my-first-docker`
2. Tạo file `app.js` với nội dung in ra "Hello from Docker!"
3. Viết `Dockerfile` để:
   - Sử dụng base image `node:18-alpine`
   - Copy file `app.js` vào container
   - Chạy ứng dụng khi container start
4. Build image với tên `hello-docker:v1`
5. Chạy container và verify output

#### Constraints
- Phải sử dụng `node:18-alpine` làm base image
- Image size không quá 200MB
- Container phải tự động exit sau khi in output

#### Hints
<details>
<summary>Hint 1: Cấu trúc Dockerfile</summary>
Dockerfile cần có: FROM, WORKDIR, COPY, CMD
</details>

<details>
<summary>Hint 2: Chạy Node script</summary>
Sử dụng `CMD ["node", "app.js"]` để chạy script
</details>

#### Expected Deliverables
- [ ] File `Dockerfile`
- [ ] File `app.js`
- [ ] Screenshot output của `docker images` showing `hello-docker:v1`
- [ ] Screenshot output khi chạy container

---

### Exercise 2: Multi-container with Port Mapping ⭐⭐

#### Scenario
Công ty cần deploy một web server NGINX để serve static files. Bạn cần chạy NGINX container và map port để có thể truy cập từ browser.

#### Requirements
1. Tạo thư mục `nginx-exercise`
2. Tạo file `index.html` với nội dung tùy chọn
3. Chạy NGINX container với:
   - Port mapping: host 8080 → container 80
   - Mount thư mục chứa `index.html` vào `/usr/share/nginx/html`
   - Chạy ở chế độ detached
4. Verify bằng cách truy cập `http://localhost:8080`
5. Xem logs của container
6. Stop và remove container

#### Constraints
- Phải sử dụng official `nginx:alpine` image
- Container phải chạy ở background (detached mode)
- Phải sử dụng volume mount (không copy file vào image)

#### Hints
<details>
<summary>Hint 1: Volume mount syntax</summary>
`docker run -v /host/path:/container/path ...`
</details>

<details>
<summary>Hint 2: Xem logs</summary>
`docker logs <container_id>` hoặc `docker logs -f <container_id>` để follow
</details>

#### Expected Deliverables
- [ ] File `index.html`
- [ ] Lệnh `docker run` đầy đủ đã sử dụng
- [ ] Screenshot browser hiển thị trang web
- [ ] Screenshot output của `docker logs`

---

### Exercise 3: Docker Compose Multi-service ⭐⭐⭐

#### Scenario
Bạn được giao task setup môi trường development cho một ứng dụng web gồm:
- Frontend: NGINX serving static files
- Backend API: Node.js application
- Database: PostgreSQL

Tất cả phải được định nghĩa trong docker-compose.yml.

#### Requirements
1. Tạo thư mục `fullstack-app`
2. Tạo `docker-compose.yml` với 3 services:
   - `frontend`: NGINX, port 80:80
   - `backend`: Node.js app, port 3000:3000
   - `db`: PostgreSQL, port 5432:5432
3. Cấu hình:
   - Backend phụ thuộc vào database
   - Frontend phụ thuộc vào backend
   - Database sử dụng volume để persist data
   - Tất cả services trong cùng một network
4. Sử dụng `docker-compose up -d` để start
5. Verify tất cả services đang chạy

#### Constraints
- Backend phải có healthcheck
- Database credentials phải dùng environment variables
- Volume phải được khai báo trong `volumes` section

#### Hints
<details>
<summary>Hint 1: depends_on</summary>
Sử dụng `depends_on` để định nghĩa thứ tự start
</details>

<details>
<summary>Hint 2: Environment variables</summary>
Database cần: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
</details>

<details>
<summary>Hint 3: Healthcheck</summary>
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

</details>

#### Expected Deliverables

- [ ] File `docker-compose.yml`
- [ ] Screenshot `docker-compose ps` showing all services running
- [ ] Screenshot network và volume created

---

### Evaluation Criteria

| Tiêu chí | Điểm tối đa | Mô tả |
|----------|-------------|-------|
| Đúng yêu cầu | 40 | Hoàn thành đầy đủ requirements |
| Cấu trúc đúng | 20 | Dockerfile/Compose đúng cú pháp và best practices |
| Tối ưu | 20 | Image size nhỏ, không lệnh thừa |
| Giải thích | 10 | Comment/ghi chú rõ ràng |
| Clean up | 10 | Dọn dẹp resources sau khi xong |
| **Tổng** | **100** | |

**Điểm pass:** ≥ 60/100

---

### Submission Guidelines

1. Tạo folder với tên: `<TenHocVien>_Module1.4_Exercises`
2. Trong folder chứa:
   - Tất cả files (Dockerfile, docker-compose.yml, scripts...)
   - Screenshots
   - File `NOTES.md` ghi chú các bước đã làm
3. Nén thành file `.zip`
4. Nộp qua [link nộp bài]

---

[⬅️ LABS](./LABS.md) | [📚 Mục lục](../../README.md) | [SOLUTIONS ➡️](./SOLUTIONS.md)

```

---

*File này là chuẩn mẫu cho mọi `EXERCISES.md` trong khoá học DevOps.*
