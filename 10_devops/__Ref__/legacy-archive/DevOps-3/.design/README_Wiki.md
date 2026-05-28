# 📁 .design/ Folder - Meta Documentation

> **Thư mục này chứa tài liệu thiết kế, planning, và tracking cho toàn bộ dự án**

---

## 📖 TÀI LIỆU TRONG FOLDER NÀY

### 1. [BLUEPRINT.md](BLUEPRINT.md) - Master Design Document

**Mục đích:** Tài liệu thết kế tổng thể của dự án

**Nội dung:**

- Vision & Principles (Tầm nhìn và nguyên tắc)
- Project Structure (Cấu trúc dự án)
- Content Philosophy (Triết lý nội dung)
- Module Templates (Mẫu cho mỗi module)
- Naming Conventions (Quy ước đặt tên)
- Quality Standards (Tiêu chuẩn chất lượng)
- Implementation Phases (Các giai đoạn thực hiện)
- Design Decisions Log (Nhật ký quyết định thiết kế)

**Khi nào xem:**

- Trước khi bắt đầu module mới
- Khi cần reference cho format/style
- Khi muốn hiểu "why" behind decisions

---

### 2. [PROGRESS.md](PROGRESS.md) - Progress Tracker

**Mục đích:** Theo dõi tiến độ thực hiện

**Nội dung:**

- ✅ Completed (Đã hoàn thành)
- 🚧 In Progress (Đang làm)
- 📋 TODO lists chi tiết cho mỗi module
- 📅 Timeline estimates
- 📊 Metrics (pages, labs, exercises created)
- 🎯 Next steps (Bước tiếp theo ngay lập tức)

**Khi nào xem:**

- Mỗi ngày trước khi bắt đầu làm việc
- Sau khi hoàn thành một milestone
- Khi cần update stakeholders về tiến độ

**⚠️ Lưu ý:** Cập nhật file này sau mỗi session làm việc!

---

### 3. [CHANGELOG.md](CHANGELOG.md) - Change Log

**Mục đích:** Ghi lại tất cả thay đổi theo version

**Format:** Based on [Keep a Changelog](https://keepachangelog.com/)

**Nội dung:**

- Version history
- Added (Thêm mới)
- Changed (Thay đổi)
- Fixed (Sửa lỗi)
- Removed (Xóa bỏ)
- Design decisions with rationale

**Khi nào xem:**

- Khi cần biết "what changed" giữa các versions
- Khi integrate changes từ contributors
- Khi prepare release notes

**⚠️ Lưu ý:** Mỗi khi release version mới, update CHANGELOG!

---

### 4. README.md (File này)

**Mục đích:** Navigation cho thư mục .design/

---

## 🎯 WORKFLOW SỬ DỤNG CÁC TÀI LIỆU

### Khi bắt đầu ngày làm việc

```
1. Mở PROGRESS.md
   └─> Check "Next Steps"
   └─> Xem TODO list

2. Mở BLUEPRINT.md (nếu cần)
   └─> Review templates
   └─> Check quality standards

3. Làm việc...

4. Cuối ngày:
   └─> Update PROGRESS.md
   └─> Mark completed items
   └─> Update metrics
   └─> Plan tomorrow's "Next Steps"
```

### Khi hoàn thành một module

```
1. Update PROGRESS.md
   └─> Move module từ TODO → Completed
   └─> Update overall progress %
   └─> Update metrics

2. Update CHANGELOG.md
   └─> Add entry cho module mới
   └─> List all files created
   └─> Note any design decisions

3. (Optional) Update BLUEPRINT.md
   └─> Nếu có design decisions mới
   └─> Nếu discovered new patterns
```

### Khi release version mới

```
1. Review CHANGELOG.md
   └─> Move [Unreleased] → [Version Number]
   └─> Add release date

2. Update PROGRESS.md
   └─> Snapshot current state

3. Tag release trong Git
   └─> git tag -a v0.2.0 -m "Module 01 Complete"
   └─> git push origin v0.2.0

4. Announce release
   └─> Discord, Discussions, etc.
```

---

## 📏 DESIGN PRINCIPLES RECAP

Khi làm việc, nhớ 5 principles từ BLUEPRINT:

1. **"Không sợ dài"** - Chi tiết > Ngắn gọn
2. **"Hiểu WHY trước HOW"** - Context > Commands
3. **"Thực hành thực chiến"** - Hands-on > Theory only
4. **"Fix logic flow"** - Teach before use
5. **"Accessibility"** - Multi-OS, Vietnamese, Analogies

---

## 🔄 VERSION HISTORY

| Version | Date | Milestone |
|---------|------|-----------|
| 0.1.0 | 2025-01-24 | Module 00 Complete |
| 0.2.0 | TBD | Module 01 Complete |
| ... | ... | ... |
| 1.0.0 | TBD | Foundation Track Complete 🎉 |
| 2.0.0 | TBD | Advanced Track Complete 🚀 |

---

## 📂 FOLDER STRUCTURE

```
.design/
├── README.md           # This file (Navigation)
├── BLUEPRINT.md        # Master design (~500 lines)
├── PROGRESS.md         # Current progress (~600 lines)
├── CHANGELOG.md        # Version history (~300 lines)
└── TEMPLATES/          # (Future) Content templates
    ├── MODULE_README_TEMPLATE.md
    ├── LABS_TEMPLATE.md
    └── SCENARIOS_TEMPLATE.md
```

---

## 🤔 FAQ về .design/ folder

### Q: Tại sao cần folder này?

**A:** Để tổ chức meta-information, track progress, và maintain consistency xuyên suốt project lớn như thế này.

### Q: Học viên có cần đọc folder này không?

**A:** KHÔNG. Thư mục này dành cho contributors và maintainers. Học viên chỉ cần các module trong FOUNDATION/ và ADVANCED/.

### Q: Có nên commit folder này vào Git không?

**A:** CÓ! Đây là phần của project documentation. Giúp contributors hiểu project structure và decisions.

### Q: File nào quan trọng nhất?

**A:** **PROGRESS.md** - Vì nó được update thường xuyên nhất và cho biết "we are now."

---

## 📞 CONTACT

Nếu có câu hỏi về design decisions hoặc cần clarification:

- Open Discussion trong repository
- Tag maintainer: @thanhlehoang0107
- Check existing design decisions trong BLUEPRINT.md Section 9

---

<div align="center">

**This folder keeps the project organized and on-track** 🎯

**Last Updated:** 2025-01-24

</div>
