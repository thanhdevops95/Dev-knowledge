# 📚 Hệ Thống Dev-Knowledge — Hướng Dẫn Sử Dụng

---

## 🎯 Tổng Quan

`Dev-Knowledge/` là một **Knowledge Base có hệ thống** với cấu trúc modular, bao gồm:

1. **Lộ trình học** (Roadmaps) — Học theo track có định hướng
2. **Bài học chủ đề** (Category-based) — Tìm kiếm theo chủ đề cụ thể
3. **Bài Mẹ → Bài Con** — Cấu trúc hierarchical, dễ maintain và expand
4. **Tài nguyên tổng hợp** — Official docs, articles, tools

---

## 🗺️ Cấu Trúc Thư Mục

```
Dev-Knowledge/
├── 00-Roadmaps/              # Lộ trình học tổng thể
├── 01-Fundamentals/          # CS Basics, Git, Linux, Networking
├── 02-Languages/             # Python, JavaScript, Go, Rust,...
├── 03-Frontend/              # HTML, CSS, React, Vue,...
├── 04-Backend/               # REST, GraphQL, Frameworks
├── 05-Databases/             # SQL, NoSQL, ORM
├── 06-DevOps/                # Docker, K8s, CI/CD, IaC
├── 07-Cloud/                 # AWS, Azure, GCP
├── 08-Architecture/          # Design Patterns, System Design
├── 09-Security/              # OWASP, Auth, Encryption
├── 10-AI-ML/                 # ML, Deep Learning, LLM
├── 11-Testing/               # Unit, Integration, E2E
├── 12-Soft-Skills/           # Code review, Interviews
├── 13-Data-Engineering/      # ETL, Airflow, Kafka, Spark
├── 14-Tools/                 # VSCode, Git, CLI tools
├── _templates/               # Templates chuẩn cho bài học
├── _scripts/                 # Helper scripts
├── README.md                 # Index chính
├── MASTER-CATALOG.md         # Danh sách tất cả chủ đề (396+)
└── CONTRIBUTING.md           # Hướng dẫn đóng góp
```

---

## 🎯 Làm Thế Nào Để Học?

### Cách 1: Học Theo Lộ Trình (Roadmap) — **RECOMMENDED cho người mới**

**Bước 1:** Vào [`00-Roadmaps/`](./00-Roadmaps/)

**Bước 2:** Chọn lộ trình phù hợp:
- [`frontend-roadmap.md`](./00-Roadmaps/frontend-roadmap.md) — Frontend Developer
- [`backend-roadmap.md`](./00-Roadmaps/backend-roadmap.md) — Backend Developer
- [`devops-roadmap.md`](./00-Roadmaps/devops-roadmap.md) — DevOps Engineer
- [`fullstack-roadmap.md`](./00-Roadmaps/fullstack-roadmap.md) — Fullstack
- [`data-engineer-roadmap.md`](./00-Roadmaps/data-engineer-roadmap.md) — Data Engineer
- [`ai-ml-roadmap.md`](./00-Roadmaps/ai-ml-roadmap.md) — AI/ML Engineer

**Bước 3:** Theo dõi thứ tự bài học trong roadmap. Mỗi bài sẽ link đến bài học chi tiết trong các category tương ứng.

**Ví dụ:** Lộ trình DevOps → Bài 1: Git Basics → `01-Fundamentals/git/01-git-basics.md` → Bài 2: Docker → `06-DevOps/docker/` → ...

---

### Cách 2: Học Theo Chủ Đề Cụ Thể — Cho người muốn tra cứu nhanh

**Bước 1:** Xem [`MASTER-CATALOG.md`](./MASTER-CATALOG.md) — Bảng danh sách tất cả 396+ chủ đề

**Bước 2:** Tìm chủ đề bạn muốn (ví dụ: Docker, React, PostgreSQL)

**Bước 3:** Vào category tương ứng:
- Docker → `06-DevOps/docker/`
- React → `03-Frontend/react/`
- PostgreSQL → `05-Databases/postgresql/`

**Bước 4:** Trong thư mục chủ đề, đọc `README.md` hoặc `index.md` để xem danh sách bài con.

---

## 📚 Cấu Trúc Bài Học Chuẩn

### Bài Mẹ (Parent Lesson)

Mỗi chủ đề lớn (ví dụ: Docker, Kubernetes, React) có cấu trúc:

```
[topic]/
├── README.md               # Giới thiệu, mục tiêu, overview
├── index.md                # Danh sách tất cả bài con + mô tả
├── lesson.md               # Nội dung lý thuyết tổng hợp
├── _sub-lessons/           # Thư mục chứa bài con
│   ├── 01-<topic>/
│   │   ├── lesson.md      # Nội dung chi tiết
│   │   ├── exercises.md   # Bài tập
│   │   ├── quiz.md        # Trắc nghiệm
│   │   └── checklist.md   # Tự đánh giá
│   └── 02-<topic>/
├── _quizzes/               # Quiz tổng hợp
├── _projects/              # Projects lớn
└── _resources/             # Tài nguyên bổ sung
```

---

### Bài Con (Sub-Lesson)

Mỗi bài con (`_sub-lessons/01-xxx/lesson.md`) có cấu trúc:

```markdown
# [Tiêu đề bài]

## Metadata
- Level, Prerequisites, Time estimate

## Mục Tiêu
- Checklist những gì học viên có thể làm sau bài

## Nội Dung
- Lý thuyết, khái niệm
- Định nghĩa chính thức (official)
- Giải thích đơn giản
- Ẩn dụ/so sánh

## Hands-On
- Code examples
- Commands
- Expected output

## Bài Tập
- Self-check questions
- Mini exercises

## Liên Kết
- Navigation (quay lại bài mẹ, sang bài tiếp)
- Further reading (docs, articles)

## Checklist
- Tự đánh giá những điểm đã nắm
```

---

## 🧭 Làm Thế Nào Để Tìm Kiếm?

### Search by Technology

| Từ khóa | Vào category |
|---------|--------------|
| Docker | `06-DevOps/docker/` |
| Kubernetes | `06-DevOps/kubernetes/` (nếu có) |
| AWS | `07-Cloud/aws/` |
| React | `03-Frontend/react/` |
| Python | `02-Languages/python/` |
| PostgreSQL | `05-Databases/postgresql/` |
| Git | `01-Fundamentals/git/` |

### Search by Skill Level

Mỗi bài có tags:
- `[BEGINNER]` — Không cần kiến thức trước
- `[INTERMEDIATE]` — Cần nền tảng cơ bản
- `[ADVANCED]` — Cần kinh nghiệm thực tế
- `[MUST-KNOW]` — Bắt buộc phải biết

**Người mới:** Bắt đầu với `[BEGINNER]` và `[MUST-KNOW]` trước.

---

## ✅ Quy Trình Học Tối Ưu

```
1. Chọn lộ trình (Roadmap) → Xác định bài học cần học
2. Đọc bài mẹ (README.md + lesson.md) → Hiểu overview
3. Đọc từng bài con theo thứ tự
   ├─ lesson.md (nội dung)
   ├─ exercises.md (thực hành)
   ├─ quiz.md (kiểm tra)
   └─ checklist.md (tự đánh giá)
4. Làm quiz tổng hợp (_quizzes/)
5. Làm project thực tế (_projects/)
6. Nếu chưa hiểu → xem _resources/ để đọc thêm
7. Pass checklist → chuyển sang bài tiếp
```

---

## 📝 Cấu Trúc Template

Tất cả templates ở [`_templates/`](../_templates/):

| Template | Mục đích |
|----------|----------|
| `parent-lesson-template.md` | Tạo bài mẹ mới |
| `sub-lesson-template.md` | Tạo bài con mới |
| `quiz-template.md` | Tạo quiz |
| `checklist-template.md` | Tạo checklist |
| `exercises-template.md` | Tạo bài tập |
| `project-template.md` | Tạo project |

**Khi đóng góp bài mới:** Copy template phù hợp, rename, và fill nội dung.

---

## 🤝 Đóng Góp

Xem [CONTRIBUTING.md](./CONTRIBUTING.md) để biết:
- Cách đóng góp bài mới
- Format chuẩn
- Quy trình PR
- Code of conduct

---

## 📊 Tiến Độ Hiện Tại

Xem bảng tiến độ trong [README.md](./README.md) — hiển thị số bài đã hoàn thành trên tổng số 396+ chủ đề.

---

## 🔄 Update Log

- `2026-04-30`: Thêm cấu trúc modular "bài mẹ → bài con"
- `2026-04-30`: Tạo ví dụ mẫu Docker đầy đủ (3 bài con + resources)
- `2026-02-20`: Mở rộng lên 396 chủ đề

---

**Lưu ý:** Đây là project đang trong quá trình xây dựng. Nhiều bài học vẫn là "TODO". Bạn có thể đóng góp để hoàn thiện!

---

**Happy Learning! 🚀**

---

**Tác giả:** Mr.Rom  
**Phiên bản:** v1.0.0  
**Cập nhật:** 30/04/2026
