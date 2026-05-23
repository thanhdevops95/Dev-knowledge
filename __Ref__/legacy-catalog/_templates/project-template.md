# [Tên Project] — Project Tổng Hợp

---

## 📋 Metadata

- **Parent Lesson:** (Link đến bài mẹ)
- **Type:** `[Mini-Project/Full-Project/Capstone]`
- **Difficulty:** `[Easy/Medium/Hard]`
- **Estimated Time:** (X giờ hoặc X ngày)
- **Prerequisites:** (Các bài học cần hoàn thành trước)

---

## 🎯 Mục Tiêu Project

[Giải thích mục tiêu tổng thể của project. Sau khi hoàn thành, học viên sẽ có được gì?]

### Kết quả Deliverables

Học viên sẽ xây dựng được:
- [ ] Deliverable 1 (ví dụ: Một Docker image hoạt động)
- [ ] Deliverable 2 (ví dụ: CI/CD pipeline)
- [ ] Deliverable 3 (ví dụ: Documentation)
- [ ] Deliverable 4 (ví dụ: Test coverage > 80%)

---

## 📝 Mô Tả Chi Tiết

### Background

[Đưa ra context thực tế: tại sao project này quan trọng? Vấn đề nào nó giải quyết?]

### Requirements

#### Functional Requirements (Yêu cầu chức năng)

1. **Yêu cầu 1:** [Mô tả]
2. **Yêu cầu 2:** [Mô tả]
3. **Yêu cầu 3:** [Mô tả]

#### Technical Requirements (Yêu cầu kỹ thuật)

1. **Công nghệ bắt buộc:**
   - [ ] Dùng [Docker/K8s/Terraform/...]
   - [ ] Viết bằng [ngôn ngữ X]
   
2. **Best Practices:**
   - [ ] Code phải có unit tests
   - [ ] CI/CD pipeline phải có các stage: build, test, deploy
   - [ ] Security scanning
   
3. **Performance/Quality:**
   - [ ] Response time < X ms
   - [ ] Test coverage > X%
   - [ ] Không có critical vulnerabilities

---

## 🗂️ Cấu Trúc Project Đề Xuất

```
project-name/
├── README.md              # Project overview
├── src/                   # Source code
│   ├── ...
├── tests/                 # Test files
│   ├── ...
├── docker-compose.yml     # Docker compose (nếu cần)
├── Dockerfile             # Docker image definition
├── .github/
│   └── workflows/        # CI/CD pipelines
├── docs/                  # Documentation
│   └── architecture.md
├── Makefile               # Helper commands
└── requirements.txt       # Dependencies
```

---

## 🚀 Các Bước Thực Hiện

### Phase 1: Setup & Planning (X giờ)

1. **Đọc kỹ requirements**
2. **Thiết kế architecture** (vẽ diagram nếu cần)
3. **Setup development environment**
4. **Tạo project structure** cơ bản

### Phase 2: Implementation (X giờ)

1. **Viết core functionality**
2. **Viết tests** (TDD approach nếu có thể)
3. **Refactor code** cho clean và maintainable

### Phase 3: DevOps Setup (X giờ)

1. **Containerize** ứng dụng với Docker
2. **Setup CI/CD** pipeline (GitHub Actions, GitLab CI,...)
3. **Deploy** lên môi trường test

### Phase 4: Testing & Optimization (X giờ)

1. **Run end-to-end testing**
2. **Performance testing**
3. **Security scanning**
4. **Optimize** dựa trên kết quả

### Phase 5: Documentation (X giờ)

1. **Viết README** đầy đủ
2. **Document architecture decisions**
3. **Viết deployment guide**

---

## 💡 Gợi Ý & Hints

### Khởi đầu

[Nếu cần, đưa ra skeleton code hoặc starter template]

### Lỗi thường gặp

- ❌ **Lỗi 1:** [Mô tả] → **Cách fix:** [Giải pháp]
- ❌ **Lỗi 2:** [Mô tả] → **Cách fix:** [Giải pháp]

### Tips

- 💡 **Tip 1:** [Gợi ý]
- 💡 **Tip 2:** [Gợi ý]

---

## ✅ Rubric Đánh Giá

| Tiêu chí | Weight | Pass (✓) | Excellent (⭐) |
|----------|--------|----------|---------------|
| **Functionality** | 30% | Hoàn thành 70% yêu cầu | Hoàn thành 100% yêu cầu |
| **Code Quality** | 20% | Code chạy được,Clean code principles | Code clean, có comments, SOLID principles |
| **Testing** | 20% | Có unit tests cơ bản | Coverage >80%, có integration tests |
| **DevOps** | 20% | Docker hoạt động | Full CI/CD, multi-stage builds, security scanning |
| **Documentation** | 10% | README cơ bản | Full docs: architecture, deployment, troubleshooting |

**Tổng điểm:** /100  
**Pass:** 70 điểm trở lên  
**Excellent:** 90 điểm trở lên

---

## 🔗 Tài Nguyên

### Starter Templates (nếu có)

- [GitHub Template Repository](url)

### Reference Implementations

- [Example project 1](url)
- [Example project 2](url)

### Documentation

- [Official Guide](url)
- [Best Practices](url)

---

## 🎓 Sau Project Này

Sau khi hoàn thành project này, bạn có thể:

- [ ] Thêm vào portfolio của mình
- [ ] Làm base cho các project phức tạp hơn
- [ ] Giảng dạy/ chia sẻ cho người khác
- [ ] Contribute back to community

---

## 📢 Feedback & Showcase

Nếu bạn hoàn thành project này:

1. **Share your work!** Mở issue hoặc discussion để chia sẻ link repo của bạn
2. **Give feedback:** Báo cáo những phần khó, đề xuất cải thiện
3. **Contribute:** Nếu bạn thấy cách giải pháp hay, hãy làm PR để thêm vào `_examples/`

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Ngày tạo:** DD/MM/YYYY  
**Cập nhật:** DD/MM/YYYY
