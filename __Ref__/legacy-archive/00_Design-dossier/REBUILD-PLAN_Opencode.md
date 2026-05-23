# 📋 Kế Hoạch Làm Lại Dev-Knowledge

## 1. PHÂN TÍCH HIỆN TRẠNG

### 1.1 Vấn đề chính

| Vấn đề | Chi tiết |
|--------|----------|
| **Trùng lặp cấu trúc** | 05-Databases vs 08-Databases, 07-Backend vs 04-Backend, 03-Terminal-OS vs 03-Terminal-OS |
| **Nội dung trùng lặp** | `01-sql-basics.md` có 2 bản gần giống nhau (05 vs 08) |
| **Thứ tự folder lộn xộn** | Số đầu folder không theo thứ tự (00, 01, 03, 05, 07, 08...) |
| **.Old chưa xử lý** | Chứa DevOps training cũ - cần review và merge |
| **Format không nhất quán** | Có file tiếng Việt, có file tiếng Anh, có file dùng emoji, có không |

### 1.2 Cấu trúc hiện tại (lộn xộn)

```
Dev-Knowledge/
├── 00-Roadmaps/
├── 01-CS-Fundamentals/
├── 01-Fundamentals/          ← TRÙNG với 01-CS-Fundamentals
├── 02-Languages/
├── 02-Version-Control/
├── 03-Frontend/              ← TRÙNG với 06-Frontend
├── 03-Terminal-OS/           ← Có ở cả 03 và 07
├── 04-Backend/               ← TRÙNG với 07-Backend
├── 04-Networking/
├── 05-Databases/             ← TRÙNG với 08-Databases
├── 05-Languages/            ← TRÙNG với 02-Languages
├── 06-DevOps/
├── 06-Frontend/             ← TRÙNG với 03-Frontend
├── 07-Backend/
├── 07-Cloud/
├── 08-Architecture/
├── 08-Databases/            ← TRÙNG với 05-Databases
├── 09-DevOps/                ← TRÙNG với 06-DevOps
├── 09-Security/
├── 10-AI-ML/
├── 10-Cloud/
├── 11-Architecture/         ← TRÙNG với 08-Architecture
├── 11-Testing/              ← TRÙNG với 13-Testing
├── 12-Security/             ← TRÙNG với 09-Security
├── 12-Soft-Skills/
├── 13-Data-Engineering/
├── 13-Testing/              ← TRÙNG với 11-Testing
├── 14-AI-ML/                 ← TRÙNG với 10-AI-ML
├── 14-Tools/
├── 15-Data-Engineering/     ← TRÙNG với 13-Data-Engineering
├── 16-Mobile/
├── 17-GameDev/
├── 18-Blockchain/
├── 19-Embedded-IoT/
├── 21-Soft-Skills/          ← TRÙNG với 12-Soft-Skills
```

### 1.3 Nguồn từ .Old (DevOps Training)

- **Knowledge-Base**: Cheatsheets, Concepts, Best-Practices (rất nhiều file trùng lặp)
- **DevOps-1_TrainingRoadmap**: Exercises, Lessons có cấu trúc rõ ràng
- **File trùng**: Nhiều file tên giống nhau (_1, _2, ...)

---

## 2. YÊU CẦU THIẾT KẾ MỚI

### 2.1 Nguyên tắc

1. **Mỗi chủ đề có DUY NHẤT 1 folder** - không trùng lặp
2. **Số thứ tự có ý nghĩa** - theo learning path hợp lý
3. **Tên folder nhất quán** - tiếng Anh, lowercase, kebab-case
4. **Nội dung chuẩn hóa** - header, format, ngôn ngữ
5. **Dữ liệu từ .Old được review và merge** - không xóa ngay

### 2.2 Cấu trúc đề xuất (Learning Path)

```
Dev-Knowledge/
├── 01-Foundations/           # CS Fundamentals, Terminal, OS
├── 02-Version-Control/      # Git
├── 03-Programming/          # Languages
├── 04-Networking/           # Network
├── 05-Frontend/             # Frontend
├── 06-Backend/               # Backend, Frameworks, APIs
├── 07-Databases/            # SQL, NoSQL
├── 08-DevOps/                # Docker, K8s, CI/CD
├── 09-Cloud/                 # AWS, GCP, Azure
├── 10-Architecture/          # Patterns, Design
├── 11-Testing/               # Unit, Integration, E2E
├── 12-Security/              # Security
├── 13-AI-ML/                 # AI/ML
├── 14-Tools/                 # IDEs, Utils
├── 15-Soft-Skills/           # Communication, etc.
├── 16-Mobile/                # Mobile dev
├── 17-GameDev/               # Game dev
├── 18-Blockchain/            # Blockchain
├── 19-Data-Engineering/     # Data pipelines
├── 20-Embedded-IoT/         # Embedded systems

# Special
├── 00-Roadmaps/              # Learning roadmaps
├── _Templates/               # Templates
├── _Refs/                    # References
```

---

## 3. DANH MỤC CÔNG VIỆC (WORKFLOW)

### Phase 1: Audit & Mapping (Ngày 1-2)

- [ ] 1.1. Liệt kê tất cả các folder hiện tại + số file trong mỗi folder
- [ ] 1.2. Xác định các folder trùng lặp (map 1:1, 1:n)
- [ ] 1.3. Đánh giá chất lượng nội dung mỗi folder (A/B/C)
- [ ] 1.4. Review .Old - extract nội dung hay cần giữ lại
- [ ] 1.5. Tạo bảng mapping: Folder cũ → Folder mới

### Phase 2: Thiết kế cấu trúc (Ngày 2-3)

- [ ] 2.1. Tạo folder mới theo cấu trúc đề xuất
- [ ] 2.2. Định nghĩa template chuẩn cho mỗi bài viết
- [ ] 2.3. Viết hướng dẫn CONTRIBUTING.md mới
- [ ] 2.4. Tạo README.md cho mỗi section

### Phase 3: Migration (Ngày 3-7)

- [ ] 3.1. Di chuyển nội dung từ folder trùng vào folder mới
- [ ] 3.2. Merge nội dung trùng (giữ bản đầy đủ nhất)
- [ ] 3.3. Review và làm giàu nội dung từ .Old
- [ ] 3.4. Chuẩn hóa format (header, ngôn ngữ, emoji)
- [ ] 3.5. Cập nhật internal links

### Phase 4: Cleanup (Ngày 7-8)

- [ ] 4.1. Xóa các folder trùng lặp cũ
- [ ] 4.2. Dọn dẹp .Old (move vào archive hoặc xóa)
- [ ] 4.3. Cập nhật SUMMARY.md, MASTER-CATALOG.md
- [ ] 4.4. Tạo index/toc cho mỗi section

### Phase 5: Review cuối (Ngày 8-10)

- [ ] 5.1. Đọc lại tất cả các bài - đảm bảo chất lượng
- [ ] 5.2. Fix broken links, images
- [ ] 5.3. Check độ nhất quán của format
- [ ] 5.4. Viết tài liệu hướng dẫn maintain

---

## 4. TEMPLATE CHUẨN CHO BÀI VIẾT

```markdown
# 📝 [Tên bài - Title Case]

> `[LEVEL]` ⭐ `[TAGS]` — Mô tả ngắn 1 dòng

---

## Mục lục
1. [Giới thiệu](#1-giới-thiệu)
2. [Nội dung chính](#2-nội-dung-chính)
3. [Ví dụ](#3-ví-dụ)
4. [Bài tập](#4-bài-tập)
5. [Tài nguyên](#5-tài-nguyên)

---

## 1. Giới thiệu
...

## 2. Nội dung chính
### 2.1 Sub-section
...

## 3. Ví dụ
...

## 4. Bài tập
- [ ] Task 1
- [ ] Task 2

## 5. Tài nguyên
- [Link 1](url)
```

**Quy tắc:**
- Ngôn ngữ: Tiếng Việt (ưu tiên) hoặc English nhất quán
- Emoji: Dùng đều cho header sections
- Code blocks: Luôn có language specified
- Level tags: `[BEGINNER]`, `[INTERMEDIATE]`, `[ADVANCED]`
- Must-know tag: ⭐ `[MUST-KNOW]`

---

## 5. PRIORITIZE NỘI DUNG

### Nội dung ưu tiên giữ lại (từ Dev-Knowledge hiện tại)
- ✅ 07-Backend/api-design/* - Format đẹp, đầy đủ
- ✅ 08-Databases/* - Chất lượng tốt
- ✅ 13-Testing/* - Đầy đủ

### Nội dung cần review (từ .Old)
- ✅ Cheatsheets (docker-commands, kubernetes-commands, git-commands...)
- ✅ Best-Practices (design-patterns, performance-optimization)
- ⚠️ Training lessons - Cần merge vào đúng section

### Nội dung trùng lặp cần merge
- 01-Fundamentals vs 01-CS-Fundamentals → Merge vào 01-Foundations
- 05-Databases vs 08-Databases → Merge vào 07-Databases
- 07-Backend vs 04-Backend → Merge vào 06-Backend

---

## 6. PHÂN CÔNG (GỢI Ý)

Nếu làm một mình, ưu tiên:

| Tuần | Nội dung |
|------|----------|
| Tuần 1 | Phase 1 + Phase 2 (Audit + Design) |
| Tuần 2 | Phase 3 (Migration - Backend + Databases) |
| Tuần 3 | Phase 3 (Migration - còn lại) |
| Tuần 4 | Phase 4 + Phase 5 (Cleanup + Review) |

---

## 7. CÔNG CỤ HỖ TRỢ

- **Search**: `grep` để tìm nội dung trùng
- **Move**: Script tự động di chuyển nếu cần
- **Links**: Check internal links với regex

---

## 8. KẾT QUẢ MONG ĐỢI

1. ✅ Cấu trúc folder nhất quán, không trùng lặp
2. ✅ Mỗi bài viết theo template chuẩn
3. ✅ Nội dung từ .Old được review và merge
4. ✅ Tài liệu hướng dẫn maintain rõ ràng
5. ✅ Index/TOC đầy đủ cho navigation

---

**Lưu ý**: Đây là kế hoạch tổng quan. Chi tiết từng bước sẽ được điều chỉnh trong quá trình thực hiện.