---
module: "0"
title: "Setup Environment – Quiz"
track: "0"
version: "1.0"
last_updated: "2025-12-27"
total_questions: 5
passing_score: 80
time_limit: "5 minutes"
---

## MODULE 0 – Setup Environment Quiz

### Instructions

- **Số câu hỏi:** 5 câu
- **Thời gian:** 5 phút
- **Điểm pass:** 4/5 (80%)

---

### Questions

#### 1. WSL2 là viết tắt của gì?

A) Windows Server Linux 2
B) Windows Subsystem for Linux 2
C) Web Server Linux 2
D) Windows Super Linux 2

<details>
<summary>Đáp án</summary>
**Đáp án: B** - Windows Subsystem for Linux version 2.
</details>

#### 2. Lệnh nào dùng để kiểm tra phiên bản Docker client và server?

A) `docker info`
B) `docker status`
C) `docker version`
D) `docker -v`

<details>
<summary>Đáp án</summary>
**Đáp án: C** - `docker version` hiển thị chi tiết cả client và server. `docker -v` thường chỉ hiện version rút gọn của client.
</details>

#### 3. Tại sao chúng ta cần config `user.email` trong Git?

A) Để đăng nhập vào GitHub
B) Để nhận email thông báo từ Git
C) Để Git xác định danh tính tác giả của commit
D) Không bắt buộc, Git tự đoán

<details>
<summary>Đáp án</summary>
**Đáp án: C** - Git dùng email để gắn danh tính vào mỗi commit.
</details>

#### 4. File cấu hình global của Git thường nằm ở đâu trên Linux/WSL?

A) `/etc/gitconfig`
B) `~/.gitconfig`
C) `.git/config`
D) `/usr/bin/gitconfig`

<details>
<summary>Đáp án</summary>
**Đáp án: B** - File `.gitconfig` nằm trong thư mục home của user (`~`).
</details>

#### 5. Docker Image khác Docker Container như thế nào?

A) Giống nhau, chỉ là tên gọi khác
B) Image là máy ảo, Container là ứng dụng
C) Image là template tĩnh (read-only), Container là instance đang chạy (run-time)
D) Container dùng để tạo Image

<details>
<summary>Đáp án</summary>
**Đáp án: C** - Image giống như "Class", Container giống như "Object" trong lập trình.
</details>

---

### Answer Key

<details>
<summary>Bảng đáp án nhanh</summary>

| Câu | Đáp án |
|-----|--------|
| 1 | B |
| 2 | C |
| 3 | C |
| 4 | B |
| 5 | C |

</details>

### Navigation Footer ⭐ BẮT BUỘC

---

[⬅️ SOLUTIONS](./SOLUTIONS.md) | [📚 Mục lục](../../README.md) | [PROJECT ➡️](./PROJECT.md)
