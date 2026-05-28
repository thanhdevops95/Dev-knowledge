# 🛠️ GIAI ĐOẠN 7: CHUẨN BỊ GITLAB

## 📌 MỤC TIÊU
Để thực hành CI/CD, bạn cần một nơi lưu trữ code có tích hợp sẵn CI runner. GitLab là lựa chọn số 1.

---

## 1. TẠO TÀI KHOẢN & REPO
1. Truy cập [gitlab.com](https://gitlab.com) và đăng ký tài khoản (Free).
2. Tạo **New Project** (Blank project).
   - Tên: `todo-devsecops`
   - Visibility: **Public** (để đỡ rắc rối vụ permission Docker login, hoặc Private nhưng phải cấu hình Token). Khuyên dùng Public cho bài học này.

## 2. PUSH CODE LÊN GITLAB
Tại thư mục gốc dự án trên máy bạn:

```bash
# Khởi tạo git nếu chưa
git init

# Thêm remote (thay URL bằng repo của bạn)
git remote add origin https://gitlab.com/USERNAME/todo-devsecops.git

# Commit code
git add .
git commit -m "Initial commit - Stage 6 Complete"

# Push
git push -u origin main
```
*(Nếu branch chính là master thì sửa thành master)*

## 3. CHUẨN BỊ DOCKER HUB
Để lưu Docker Image, ta dùng Docker Hub.
1. Đăng ký tại: [hub.docker.com](https://hub.docker.com/)
2. Tạo Access Token (để CI đăng nhập an toàn hơn mật khẩu):
   - Vào Account Settings -> Security -> New Access Token.
   - Copy token đó.

## 4. CẤU HÌNH BIẾN (VARIABLES) TRÊN GITLAB
Vào Project trên GitLab -> Settings -> CI/CD -> Variables -> Expand -> Add Variable:
1. `DOCKER_USER`: Username Docker Hub của bạn.
2. `DOCKER_PASS`: Access Token (hoặc mật khẩu) Docker Hub.

---

## ✅ CHECKLIST
- Code đã lên GitLab.
- Đã có tài khoản Docker Hub.
- Đã cài đặt Variable `DOCKER_USER` và `DOCKER_PASS`.

Sẵn sàng để Pipeline chạy tự động!
