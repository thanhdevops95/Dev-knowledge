# 🚀 Dev-Knowledge — Kho Kiến Thức Lập Trình Toàn Diện

> **Dành cho:** Người mới bắt đầu → Senior Developer → Tech Lead  
> **Mục tiêu:** Một nguồn tài liệu duy nhất, có hệ thống, bằng tiếng Việt — để ai cũng có thể tự học và tra cứu kiến thức Dev.

---

## 📌 Triết lý của kho này

- **"Learn by Doing"** — Mỗi bài kèm ví dụ thực tế, bài tập và project nhỏ.
- **"Từ WHY → WHAT → HOW"** — Luôn giải thích *tại sao* trước khi đi vào kỹ thuật.
- **"Evergreen First"** — Ưu tiên kiến thức nền tảng bền vững hơn trend ngắn hạn.
- **"Open Source"** — Mọi người đều có thể đóng góp và cải thiện.
- **"Modular Learning"** — Chia nhỏ kiến thức thành các bài học độc lập, dễ tiêu thụ và cập nhật.

---

## 🏗️ Cấu Trúc Tổ Chức

### Hierarchical Structure (Lớp Lớp)

```
Dev-Knowledge/
├── 00-Roadmaps/              # 🗺️ Lộ trình học tổng thể (Frontend, Backend, DevOps...)
├── 01-Fundamentals/          # 🧱 Kiến thức nền tảng bắt buộc
├── 02-Languages/             # 💻 Ngôn ngữ lập trình
├── 03-Frontend/              # 🎨 Phát triển giao diện
├── 04-Backend/               # ⚙️ Server & API
├── 05-Databases/             # 🗄️ Cơ sở dữ liệu
├── 06-DevOps/                # 🔧 DevOps & Infrastructure
├── 07-Cloud/                 # ☁️ Điện toán đám mây
├── 08-Architecture/          # 🏗️ Kiến trúc phần mềm
├── 09-Security/              # 🔐 Bảo mật
├── 10-AI-ML/                 # 🤖 AI & Machine Learning
├── 11-Testing/               # 🧪 Kiểm thử
├── 12-Soft-Skills/           # 🧠 Kỹ năng mềm
├── 13-Data-Engineering/      # 📊 Kỹ thuật dữ liệu
├── 14-Tools/                 # 🛠️ Công cụ & Productivity
├── _templates/               # 📋 Template chuẩn cho bài học
└── _scripts/                 # 🔧 Scripts hỗ trợ

```

### Bài Mẹ → Bài Con (Parent-Child Lessons)

Mỗi chủ đề lớn (ví dụ: Docker, Kubernetes, React) có thể được chia thành:

```
06-DevOps/
├── Docker/                      # 📚 **Bài Mẹ** (Main Lesson Index)
│   ├── README.md               # Giới thiệu tổng quan, mục tiêu
│   ├── index.md                # Danh sách tất cả bài con + mô tả
│   ├── lesson.md               # Nội dung chính (lịch sử, khái niệm, tại sao)
│   ├── _sub-lessons/           # 📁 Thư mục bài con
│   │   ├── 01-Installation-Setup/
│   │   │   ├── lesson.md      # Nội dung bài học chi tiết
│   │   │   ├── exercises.md   # Bài tập thực hành
│   │   │   ├── quiz.md        # Câu hỏi trắc nghiệm
│   │   │   └── checklist.md   # Checklist tự đánh giá
│   │   ├── 02-Images-Containers/
│   │   ├── 03-Dockerfile-Basics/
│   │   ├── 04-Volumes-Networks/
│   │   └── 05-Best-Practices/
│   ├── _quizzes/               # Bài tập tổng hợp của bài mẹ
│   ├── _projects/              # Projects lớn tổng hợp
│   └── _resources/             # Tài nguyên bổ sung
```

**Ưu điểm:**
- ✅ Dễ maintain: sửa 1 bài con không ảnh hưởng bài khác
- ✅ Dễ navigate: học theo trình tự hoặc nhảy vào bài cụ thể
- ✅ Dễ expand: thêm bài con mới mà không làm file quá dài
- ✅ Modular: mỗi bài con độc lập, có thể reuse

---

## 🎯 Bắt đầu từ đâu?

### Nếu bạn là người **hoàn toàn mới**
1. Đọc [Lộ trình tổng quan](./00-Roadmaps/00-overview.md)
2. Bắt đầu với [Git cơ bản](./01-Fundamentals/git/01-git-basics.md) (nếu có)
3. Chọn ngôn ngữ → [Python](./02-Languages/python/) hoặc [JavaScript](./02-Languages/javascript/)

### Nếu bạn muốn học **Frontend**
→ Xem [Lộ trình Frontend](./00-Roadmaps/frontend-roadmap.md)  
→ Tìm chủ đề cụ thể trong `03-Frontend/` (ví dụ: `03-Frontend/react/`)

### Nếu bạn muốn học **Backend**
→ Xem [Lộ trình Backend](./00-Roadmaps/backend-roadmap.md)  
→ Tìm chủ đề cụ thể trong `04-Backend/`

### Nếu bạn muốn học **DevOps/Cloud**
→ Xem [Lộ trình DevOps](./00-Roadmaps/devops-roadmap.md)  
→ Tìm chủ đề trong `06-DevOps/` hoặc `07-Cloud/`

### Nếu bạn tìm kiếm **chủ đề cụ thể** (ví dụ: MS-SQL, Docker, OAuth)
1. Vào category tương ứng (ví dụ: `05-Databases/` cho MS-SQL)
2. Tìm thư mục bài học (ví dụ: `05-Databases/mssql/`)
3. Đọc `README.md` hoặc `index.md` của bài đó để xem danh sách bài con
4. Học từng bài con theo thứ tự

---

## 📊 Cấp độ học

Mỗi bài tài liệu có gắn cấp độ:

| Badge | Cấp độ | Mô tả |
|---|---|---|
| 🟢 `[BEGINNER]` | Người mới | Không cần kiến thức trước |
| 🟡 `[INTERMEDIATE]` | Trung cấp | Cần nền tảng cơ bản |
| 🔴 `[ADVANCED]` | Nâng cao | Yêu cầu kinh nghiệm thực tế |
| ⭐ `[MUST-KNOW]` | Bắt buộc | Kiến thức không thể thiếu |

---

## 📈 Tiến độ hiện tại

| # | Phần | Tổng | ✅ | 🚧 | ❌ |
|---|---|---|---|---|---|
| 00 | Roadmaps | 13 | 7 | 0 | 6 |
| 01 | CS Fundamentals | 23 | 1 | 8 | 14 |
| 02 | Version Control | 4 | 1 | 2 | 1 |
| 03 | Terminal & OS | 9 | 2 | 3 | 4 |
| 04 | Networking | 12 | 2 | 3 | 7 |
| 05 | Languages | 33 | 5 | 9 | 19 |
| 06 | Frontend | 46 | 5 | 10 | 31 |
| 07 | Backend | 29 | 5 | 6 | 18 |
| 08 | Databases | 29 | 4 | 5 | 20 |
| 09 | DevOps | 36 | 5 | 5 | 26 |
| 10 | Cloud | 18 | 1 | 0 | 17 |
| 11 | Architecture | 16 | 2 | 5 | 9 |
| 12 | Security | 16 | 2 | 1 | 13 |
| 13 | Testing & QA | 16 | 1 | 0 | 15 |
| 14 | AI/ML | 19 | 2 | 2 | 15 |
| 15 | Data Engineering | 12 | 0 | 0 | 12 |
| 16 | Mobile | 12 | 0 | 5 | 7 |
| 17 | Game Dev | 8 | 0 | 0 | 8 |
| 18 | Blockchain | 5 | 0 | 0 | 5 |
| 19 | Embedded/IoT | 7 | 0 | 0 | 7 |
| 20 | Tools | 13 | 2 | 0 | 11 |
| 21 | Soft Skills | 10 | 1 | 3 | 6 |
| **TỔNG** | | **396** | **48** | **67** | **281** |

---

## 📝 Cấu Trúc Bài Học Chuẩn

### Bài Mẹ (Main Lesson)
```
[topic]/
├── README.md         # Giới thiệu, mục tiêu, tại sao cần học
├── index.md          # Danh sách tất cả bài con với mô tả ngắn
├── lesson.md         # Nội dung lý thuyết tổng hợp (history, concepts)
├── _sub-lessons/     # Thư mục chứa tất cả bài con
├── _quizzes/         # Bài tập tổng hợp
├── _projects/        # Projects lớn
└── _resources/       # Tài nguyên bổ sung
```

### Bài Con (Sub-Lesson)
```
01-[topic]/
├── lesson.md         # Nội dung bài học chi tiết
├── exercises.md      # Bài tập thực hành
├── quiz.md           # Câu hỏi trắc nghiệm
├── checklist.md      # Checklist tự đánh giá
└── resources.md      # Link tài nguyên (optional)
```

### Template chuẩn: Xem `_templates/lesson-template.md` và `_templates/parent-lesson-template.md`

---

## ✍️ Đóng góp

Xem hướng dẫn đóng góp tại [CONTRIBUTING.md](./CONTRIBUTING.md) và sử dụng các [template chuẩn](./_templates/) khi tạo bài mới.

---

## 📅 Cập nhật lần cuối

`2026-04-30` — Cập nhật cấu trúc modular "bài mẹ → bài con". Thêm hướng dẫn navigation chi tiết.

