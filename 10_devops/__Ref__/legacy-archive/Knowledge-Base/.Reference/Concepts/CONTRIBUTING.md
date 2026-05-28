# 🤝 Hướng dẫn Đóng góp

Cảm ơn bạn đã quan tâm đến việc đóng góp cho **DevOps Mastery**!

---

## 📋 Nguyên tắc đóng góp

### 1. Format

- Phóng cách: trực tiếp, gãy gọn, không văn hoa
- Mỗi module có 3 files: README, LABS, SCENARIOS
- Sử dụng emoji theo quy định

### 3. Code

- Code phải có comment giải thích
- Tuân thủ best practices
- Test trước khi submit

---

## 🔄 Quy trình đóng góp

### Bước 1: Fork repository

```bash
# Fork repo trên GitHub, sau đó clone
git clone https://github.com/YOUR_USERNAME/DevOps-Mastery.git
cd DevOps-Mastery
```

### Bước 2: Tạo branch mới

```bash
git checkout -b feature/your-feature-name
```

### Bước 3: Thực hiện thay đổi

- Sửa/thêm nội dung
- Test kỹ lưỡng
- Commit với message rõ ràng

```bash
git add .
git commit -m "feat: Add detailed explanation for Docker networking"
```

### Bước 4: Push và tạo Pull Request

```bash
git push origin feature/your-feature-name
```

Sau đó tạo Pull Request trên GitHub.

---

## 📝 Commit Message Convention

```
<type>: <description>

[optional body]
```

**Types:**

- `feat`: Thêm tính năng mới
- `fix`: Sửa lỗi
- `docs`: Cập nhật tài liệu
- `style`: Format, không ảnh hưởng logic
- `refactor`: Tái cấu trúc code
- `test`: Thêm tests

**Ví dụ:**

```
docs: Add Kubernetes troubleshooting section
feat: Add Lab 3 for Docker Compose
fix: Correct typo in Module 02 README
```

---

## ✅ Checklist trước khi submit PR

- [ ] Code có comment
- [ ] Không có lỗi chính tả
- [ ] Links hoạt động
- [ ] Đã test (nếu có code)

---

## 💬 Cần hỗ trợ?

- Mở [Issue](https://github.com/thanhlehoang0107/DevOps-Mastery/issues) để hỏi
- Tham gia [Discussions](https://github.com/thanhlehoang0107/DevOps-Mastery/discussions)

---

**Cảm ơn bạn đã đóng góp! 🙏**
