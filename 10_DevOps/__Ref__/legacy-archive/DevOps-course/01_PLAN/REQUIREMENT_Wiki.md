# 📋 MODULE 01: PLAN - YÊU CẦU & TIÊU CHÍ NGHIỆM THU

## 🎯 Mục tiêu Module

Sau khi hoàn thành module này, bạn sẽ:

1. ✅ Hiểu **tại sao** cần DevOps và khi nào nên áp dụng
2. ✅ Nắm vững **tư duy Agile** và áp dụng vào quy trình phát triển
3. ✅ Biết cách thiết kế **Architecture Diagram** cho ứng dụng
4. ✅ Viết được **Requirements Document** rõ ràng, đầy đủ
5. ✅ Thực hành **collaboration** với Git cơ bản (commit, push, pull)
6. ✅ Giải quyết được 5 tình huống phổ biến khi lập kế hoạch dự án

---

## 📖 Danh sách thuật ngữ (Terminology)

Trong module này, bạn sẽ gặp các từ viết tắt sau:

| Từ viết tắt | Tiếng Anh đầy đủ | Nghĩa tiếng Việt |
|-------------|------------------|------------------|
| **DevOps** | Development + Operations | Phát triển + Vận hành |
| **Agile** | Agile Software Development | Phát triển phần mềm linh hoạt |
| **Sprint** | Sprint (Scrum term) | Chu kỳ phát triển ngắn (1-4 tuần) |
| **MVP** | Minimum Viable Product | Sản phẩm khả thi tối thiểu |
| **User Story** | User Story | Câu chuyện người dùng (mô tả tính năng) |
| **DoD** | Definition of Done | Định nghĩa "Hoàn thành" |
| **SLA** | Service Level Agreement | Thỏa thuận mức độ dịch vụ |
| **RTO** | Recovery Time Objective | Thời gian phục hồi mục tiêu |
| **RPO** | Recovery Point Objective | Điểm phục hồi mục tiêu |
| **MTTR** | Mean Time To Recovery | Thời gian trung bình để phục hồi |
| **SDLC** | Software Development Life Cycle | Chu trình phát triển phần mềm |
| **VCS** | Version Control System | Hệ thống quản lý phiên bản |

---

## ✅ Checklist bài tập (LABS)

Hoàn thành tất cả các tasks sau trong `LABS.md`:

### Phần 1: Thiết lập môi trường

- [ ] **LAB 1.1**: Cài đặt Git và cấu hình user
- [ ] **LAB 1.2**: Tạo repository trên GitHub
- [ ] **LAB 1.3**: Clone repository về local
- [ ] **LAB 1.4**: Thực hiện commit đầu tiên

### Phần 2: Viết tài liệu dự án

- [ ] **LAB 2.1**: Viết User Stories cho The Counter App
- [ ] **LAB 2.2**: Tạo Architecture Diagram (dùng draw.io hoặc Mermaid)
- [ ] **LAB 2.3**: Viết Requirements Document (README.md)
- [ ] **LAB 2.4**: Tạo file CHANGELOG.md để theo dõi thay đổi

### Phần 3: Lập kế hoạch Sprint

- [ ] **LAB 3.1**: Chia nhỏ dự án thành tasks (dùng GitHub Issues)
- [ ] **LAB 3.2**: Ước lượng thời gian cho từng task
- [ ] **LAB 3.3**: Tạo Project Board trên GitHub
- [ ] **LAB 3.4**: Di chuyển issues qua các cột (Todo → In Progress → Done)

### Phần 4: Collaboration cơ bản

- [ ] **LAB 4.1**: Tạo branch mới từ main
- [ ] **LAB 4.2**: Commit thay đổi vào branch
- [ ] **LAB 4.3**: Tạo Pull Request
- [ ] **LAB 4.4**: Review và merge PR

---

## 🚨 Checklist tình huống (SCENARIOS)

Giải quyết thành công 5 scenarios sau trong `SCENARIOS.md`:

- [ ] **Scenario 1**: Bus Factor Problem - Dev duy nhất nghỉ việc
- [ ] **Scenario 2**: Vague Requirements - Yêu cầu mơ hồ gây ra bug
- [ ] **Scenario 3**: Scope Creep - Khách hàng liên tục thay đổi yêu cầu
- [ ] **Scenario 4**: Merge Conflict Hell - 3 người sửa cùng 1 file
- [ ] **Scenario 5**: No Documentation - Dự án cũ không có tài liệu

---

## 💯 Tiêu chí nghiệm thu (Acceptance Criteria)

Bạn được coi là **hoàn thành Module 01** khi:

### Kiến thức lý thuyết

- ✅ Giải thích được DevOps bằng lời của mình (có ẩn dụ)
- ✅ Phân biệt được Agile vs Waterfall
- ✅ Vẽ được Architecture Diagram cho ứng dụng 2-tier (Web + DB)

### Kỹ năng thực hành

- ✅ Thực hiện được Git workflow cơ bản: clone → branch → commit → push → PR → merge
- ✅ Tạo được GitHub repository với README, LICENSE, .gitignore
- ✅ Viết được User Story theo format: "As a [role], I want [feature], so that [benefit]"
- ✅ Sử dụng được GitHub Issues và Project Board

### Mindset

- ✅ Hiểu tầm quan trọng của **Documentation**
- ✅ Biết đặt câu hỏi đúng lúc để tránh vague requirements
- ✅ Có thói quen commit code thường xuyên (không để 1000 dòng code rồi mới commit)

---

## 📦 Deliverables (Sản phẩm đầu ra)

Khi hoàn thành module này, repository của bạn phải có:

```
your-repo/
├── README.md                    # Tài liệu dự án
├── CHANGELOG.md                 # Lịch sử thay đổi
├── .gitignore                   # Ignore files
├── LICENSE                      # Giấy phép mã nguồn
├── docs/
│   ├── architecture.md          # Kiến trúc hệ thống
│   └── user-stories.md          # User stories
├── source-code/
│   └── (Source code của The Counter App)
└── .github/
    └── (GitHub Issues + Projects đã setup)
```

---

## ⏱️ Thời lượng ước tính

- **Học lý thuyết (README.md)**: 1.5 - 2 giờ
- **Làm LAB (LABS.md)**: 2 - 3 giờ
- **Giải SCENARIOS (SCENARIOS.md)**: 1 - 1.5 giờ

**Tổng**: 4-6 giờ

---

## ⏭️ Next Steps

Khi hoàn thành đầy đủ checklist, hãy chuyển sang:

👉 **Module 02: BUILD - Git & Docker**

---

## 💡 Tips

1. **Đừng vội code** - 80% dự án thất bại vì lập kế hoạch kém, không phải code kém
2. **Viết tài liệu ngay từ đầu** - "Future you" sẽ cảm ơn "Current you"
3. **Commit nhỏ, commit thường** - Commit message rõ ràng giúp debug nhanh hơn
4. **Hỏi nhiều** - Câu hỏi "ngớ ngẩn" bây giờ tốt hơn bug production sau này

---

**Sẵn sàng bắt đầu? Đọc tiếp tại `README.md`! 🚀**
