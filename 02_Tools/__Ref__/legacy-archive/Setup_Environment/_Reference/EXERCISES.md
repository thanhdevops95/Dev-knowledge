---
module: "0"
title: "Setup Environment – Exercises"
track: "0"
version: "1.0"
last_updated: "2025-12-27"
difficulty: "Beginner"
estimated_time: "30 minutes"
---

## MODULE 0 – Setup Environment Exercises

### Overview

- **Số lượng bài tập:** 2 bài
- **Thời gian ước tính:** 30 phút
- **Mức độ khó:** Beginner
- **Yêu cầu:** Hoàn thành cả 2 bài để đảm bảo môi trường không lỗi

### Prerequisites

- Đã hoàn thành LABS (Cài đặt WSL, Docker, Git)

---

### Exercises

#### Exercise 1: Docker Permission Challenge (Linux/WSL)

**Scenario (Tình huống):**
Bạn đang làm việc trên môi trường Linux thuần (hoặc WSL không dùng Docker Desktop mà cài Engine trực tiếp). Khi chạy lệnh `docker ps`, bạn nhận được lỗi:
`Got permission denied while trying to connect to the Docker daemon socket`

**Requirements (Yêu cầu):**

1. Tìm cách cấu hình để running user hiện tại có thể chạy lệnh docker mà **KHÔNG** cần gõ `sudo` trước mỗi lệnh.
2. Verify bằng lệnh `docker run hello-world`.

**Constraints (Ràng buộc):**

- Không được dùng `sudo docker ...` làm giải pháp lâu dài.

**Hints:**
<details>
<summary>Xem gợi ý</summary>
Liên quan đến `docker group`.
</details>

#### Exercise 2: Git Identity Crisis

**Scenario:**
Bạn vừa setup máy mới và commit code lần đầu tiên lên GitHub công ty. Tuy nhiên, trên giao diện GitHub, commit của bạn không hiện avatar của bạn mà hiện hình "ghost" (người dùng vô danh) hoặc avatar mặc định. Đồng nghiệp phàn nàn không biết ai là người commit.

**Requirements:**

1. Xác định nguyên nhân tại sao GitHub không nhận diện được user.
2. Sửa cấu hình Git để các commit sau này hiện đúng avatar và link tới profile của bạn.

**Hints:**
<details>
<summary>Xem gợi ý</summary>
Kiểm tra `user.email` trong git config và so sánh với email đăng ký GitHub.
</details>

---

### Evaluation Criteria

| Tiêu chí | Điểm tối đa | Mô tả |
|----------|-------------|-------|
| Docker chạy không sudo | 50 | User nằm trong group docker |
| Git config đúng | 50 | `git log` hiện đúng tên và email |
| **Tổng** | **100** | |

**Điểm pass:** 100/100 (Vì đây là cấu hình cơ bản bắt buộc)

---

### Submission Guidelines

1. Chụp ảnh màn hình terminal khi chạy `docker run hello-world` (không sudo).
2. Chụp ảnh màn hình `git config --list` (che các thông tin nhạy cảm khác nếu có).
3. Lưu vào folder `Setup_Exercise_Evidence` và nén zip.

---

### Navigation Footer ⭐ BẮT BUỘC

---

[⬅️ LABS](./LABS.md) | [📚 Mục lục](../../README.md) | [SOLUTIONS ➡️](./SOLUTIONS.md)
