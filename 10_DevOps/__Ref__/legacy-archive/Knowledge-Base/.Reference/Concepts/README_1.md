# 📚 Reference - Thư Viện Tài Liệu Tham Khảo

---

## 📋 Mô Tả

Thư mục này chứa toàn bộ tài liệu tham khảo được tổ chức lại từ các nguồn khác nhau, phục vụ cho việc xây dựng dự án **DevOps-Journey**.

---

## 📁 Cấu Trúc Thư Mục

```
Reference/
├── _QuytacThietke/           # 🎨 Quy tắc & Thiết kế
│   ├── .design/              # Templates và specifications (7 file *_design.md)
│   ├── README_Samples/       # Các mẫu README đã viết
│   ├── resources/            # GLOSSARY.md, SOFTWARE_LINKS.md
│   └── assets/               # Ảnh, logo chung
│
├── _NoiDungMau/              # 📖 Nội dung mẫu (Content Samples)
│   ├── Setup_Environment/    # Mẫu setup môi trường
│   ├── Track1-5/             # Mẫu nội dung cho 5 Tracks
│   ├── DevOps-1_TrainingRoadmap/  # Roadmap từ nguồn 1
│   ├── DevOps-2/             # Nội dung từ nguồn 2 (cấu trúc modules)
│   ├── DevOps-3/             # Nội dung từ nguồn 3 (FOUNDATION)
│   └── DevOps-course/        # Nội dung DevOps lifecycle (PLAN→MONITOR)
│
└── _BaiTap/                  # ✏️ Bài tập & Exercises
    ├── DevOps-1_Exercises/   # Exercises từ nguồn 1
    └── Devops-Exercises/     # Bộ exercises lớn (345 items)
```

---

## 📂 Chi Tiết Từng Thư Mục

### 🎨 _QuytacThietke (Quy tắc & Thiết kế)

**Mục đích:** Chứa tất cả tài liệu thiết kế, quy tắc, templates chuẩn.

| Thư mục/File | Mô tả |
|--------------|-------|
| `.design/` | Chứa `MASTER_BLUEPRINT.md` và 7 file `*_design.md` (README, CHEATSHEET, LABS, QUIZ, EXERCISES, PROJECT, SOLUTIONS) |
| `README_Samples/` | Các mẫu README đã được viết sẵn |
| `resources/` | `GLOSSARY.md` (từ điển thuật ngữ), `SOFTWARE_LINKS.md` (links phần mềm) |
| `assets/` | Ảnh, logo dùng chung |

**👉 Sử dụng khi:** Cần tham khảo quy tắc, template, hoặc thiết kế chuẩn.

---

### 📖 _NoiDungMau (Nội dung mẫu)

**Mục đích:** Chứa các nội dung đã được viết từ nhiều nguồn, dùng làm tham khảo khi viết nội dung mới.

| Thư mục | Nguồn | Đặc điểm |
|---------|-------|----------|
| `Setup_Environment/` | Bản gốc | 7 files chuẩn + scripts |
| `Track1-5/` | Bản gốc | Cấu trúc hoàn chỉnh với 7 files/module |
| `DevOps-1_TrainingRoadmap/` | Nguồn 1 | Roadmap 7 Lessons |
| `DevOps-2/` | Nguồn 2 | 15 Modules (LINUX → SRE) + Labs + Scenarios |
| `DevOps-3/` | Nguồn 3 | Foundation với 11 modules |
| `DevOps-course/` | Nguồn khác | Cấu trúc theo DevOps lifecycle |

**👉 Sử dụng khi:** Cần tham khảo cách viết nội dung, cấu trúc bài học.

---

### ✏️ _BaiTap (Bài tập & Exercises)

**Mục đích:** Chứa các bài tập, exercises, solutions từ nhiều nguồn.

| Thư mục | Số lượng | Đặc điểm |
|---------|----------|----------|
| `DevOps-1_Exercises/` | 55 items | Exercises theo từng lesson |
| `Devops-Exercises/` | 345 items | Bộ exercises lớn với nhiều topics |

**👉 Sử dụng khi:** Cần tham khảo bài tập, câu hỏi, scenarios.

---

## 🔍 Cách Sử Dụng

### 1. Khi bắt đầu viết module mới

```bash
# 1. Xem quy tắc thiết kế
open _QuytacThietke/.design/MASTER_BLUEPRINT.md

# 2. Xem template tương ứng
open _QuytacThietke/.design/README_design.md

# 3. Tham khảo nội dung mẫu
open _NoiDungMau/DevOps-2/01_LINUX/README.md
```

### 2. Khi cần tham khảo thuật ngữ

```bash
open _QuytacThietke/resources/GLOSSARY.md
```

### 3. Khi cần tham khảo bài tập

```bash
# Xem danh sách topics
ls _BaiTap/Devops-Exercises/topics/
```

---

## 📊 Thống Kê

| Danh mục | Số thư mục con | Mục đích chính |
|----------|----------------|----------------|
| `_QuytacThietke` | 4 | Templates, Quy tắc |
| `_NoiDungMau` | 10 | Nội dung tham khảo |
| `_BaiTap` | 2 | Bài tập, Exercises |

---

## ⚠️ Lưu Ý

1. **Không chỉnh sửa** các file trong thư mục này - chỉ tham khảo
2. **Copy sang DevOps-Journey** khi cần sử dụng
3. Các file trong `_QuytacThietke/.design/` là **nguồn chân lý duy nhất** cho quy tắc thiết kế

---

*Cập nhật: 2025-12-28*
