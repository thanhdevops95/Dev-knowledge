# 🎨 _QuytacThietke - Quy Tắc & Thiết Kế

---

## 📋 Mô Tả

Thư mục này chứa **tất cả quy tắc, tiêu chuẩn, và templates** cho dự án DevOps-Journey. Đây là **nguồn chân lý duy nhất** (Single Source of Truth) cho việc thiết kế và viết nội dung.

---

## 📁 Cấu Trúc

```
_QuytacThietke/
├── .design/                      # Templates & Specifications
│   ├── MASTER_BLUEPRINT.md       # ⭐ Tài liệu master (ĐỌC TRƯỚC TIÊN)
│   ├── scaffold_course.py        # Script tạo cấu trúc tự động
│   ├── .markdownlint.json        # Config linter
│   └── _Reference/               # 7 file design specifications
│       ├── README_design.md
│       ├── CHEATSHEET_design.md
│       ├── LABS_design.md
│       ├── QUIZ_design.md
│       ├── EXERCISES_design.md
│       ├── PROJECT_design.md
│       └── SOLUTIONS_design.md
│
├── README_Samples/               # Các mẫu README đã viết
│   ├── README.md                 # Mẫu README chính
│   └── _Reference/               # Các phiên bản README khác
│
├── resources/                    # Tài liệu bổ trợ
│   ├── GLOSSARY.md               # 📖 Từ điển thuật ngữ DevOps
│   └── SOFTWARE_LINKS.md         # 🔗 Links tải phần mềm chính thức
│
└── assets/                       # Ảnh, logo dùng chung
```

---

## 📚 Hướng Dẫn Sử Dụng

### 1. Đọc MASTER_BLUEPRINT trước tiên

```bash
# File quan trọng nhất - đọc trước khi làm bất cứ điều gì
open .design/MASTER_BLUEPRINT.md
```

**Nội dung chính:**

- Cấu trúc thư mục chuẩn
- Quy tắc đặt tên
- Lộ trình đào tạo 5 Track
- 7 loại file Markdown chuẩn
- Quy tắc ngôn ngữ
- Quy định hình ảnh
- Progress Tracker

### 2. Xem design specification tương ứng

Khi viết file nào, xem design tương ứng:

| Đang viết | Xem file |
|-----------|----------|
| `README.md` | `.design/_Reference/README_design.md` |
| `CHEATSHEET.md` | `.design/_Reference/CHEATSHEET_design.md` |
| `LABS.md` | `.design/_Reference/LABS_design.md` |
| `QUIZ.md` | `.design/_Reference/QUIZ_design.md` |
| `EXERCISES.md` | `.design/_Reference/EXERCISES_design.md` |
| `PROJECT.md` | `.design/_Reference/PROJECT_design.md` |
| `SOLUTIONS.md` | `.design/_Reference/SOLUTIONS_design.md` |

### 3. Tra cứu thuật ngữ

```bash
# Khi cần giải thích thuật ngữ
open resources/GLOSSARY.md
```

**Quy tắc:** Thuật ngữ chuyên ngành **KHÔNG DỊCH**, chỉ giải thích.

---

## ⭐ Các Quy Tắc Quan Trọng Nhất

### Quy tắc ngôn ngữ

| ❌ SAI | ✅ ĐÚNG |
|--------|---------|
| "Triển khai vỏ đậu lên cụm" | "Deploy Pod lên Cluster" |
| "Đường ống CI/CD" | "CI/CD Pipeline" |
| "Thùng chứa" | "Container" |

### Quy tắc hình ảnh

- **Ưu tiên Mermaid.js** cho diagram
- **Text block** cho screenshot terminal
- **PNG/WebP < 500KB** cho screenshot GUI

### Navigation Footer (Bắt buộc)

Cuối mỗi file phải có:

```markdown
---

[⬅️ Bài trước](../prev/README.md) | [📚 Mục lục](../../README.md) | [Bài tiếp ➡️](../next/README.md)
```

---

## 🔧 Tools & Scripts

### scaffold_course.py

Script Python để tạo cấu trúc module tự động:

```bash
python .design/scaffold_course.py
```

### .markdownlint.json

Config cho markdown linter:

```bash
npx markdownlint "**/*.md"
```

---

*Cập nhật: 2025-12-28*
