# 🤝 Hướng dẫn đóng góp

## Cấu trúc thư mục

```
Dev-Knowledge/
├── 00-Roadmaps/            # Lộ trình học theo vai trò
├── 01-Fundamentals/        # Kiến thức nền tảng (CS, DSA, Git, Networking, Terminal)
├── 02-Languages/           # Ngôn ngữ lập trình (Python, JS, TS, Go, Java, C#, Rust…)
├── 03-Frontend/            # Phát triển giao diện (HTML, CSS, React, Vue, Next.js…)
├── 04-Backend/             # Phát triển server & API (REST, GraphQL, gRPC, Frameworks…)
├── 05-Databases/           # Cơ sở dữ liệu (SQL, NoSQL, ORM, Data Modeling)
├── 06-DevOps/              # DevOps & Infrastructure (Docker, K8s, CI/CD, IaC, Cloud)
├── 07-Cloud/               # Điện toán đám mây (AWS, Azure, GCP, Cloudflare)
├── 08-Architecture/        # Kiến trúc phần mềm (Design Patterns, System Design, DDD)
├── 09-Security/            # Bảo mật (OWASP, Auth, Encryption, DevSecOps)
├── 10-AI-ML/               # AI & Machine Learning (ML, Deep Learning, LLM, MLOps)
├── 11-Tools/               # Công cụ & Productivity (Editors, API clients, Monitoring)
├── 12-Soft-Skills/         # Kỹ năng mềm & Tư duy (Code review, Interviews, Career)
├── 13-Data-Engineering/    # Kỹ thuật dữ liệu (ETL, Airflow, Spark, Kafka, dbt)
├── 14-Testing/             # Kiểm thử (Unit, Integration, E2E, TDD, BDD)
├── 15-Mobile/              # Phát triển di động (React Native, Flutter, iOS, Android)
├── 16-GameDev/             # Phát triển game (Unity, Unreal, Godot, Three.js)
├── 17-Blockchain/          # Blockchain & Web3 (Solidity, DeFi, Web3.js)
├── 18-Embedded-IoT/        # Embedded & IoT (MCU, RTOS, MQTT, AWS IoT)
├── 19-Algorithms/          # Thuật toán nâng cao (DP, Graph, String, Number theory)
└── _templates/             # Mẫu tài liệu chuẩn
```

---

## Quy tắc viết bài

### 1. Dùng template

Mọi bài mới phải bắt đầu từ `_templates/article-template.md`.

### 2. Đặt tên file

```
01-tên-chủ-đề.md     ← Số thứ tự + tên kebab-case tiếng Anh
02-chủ-đề-tiếp.md
```

### 3. Cấu trúc bài viết bắt buộc

Mỗi bài phải có đủ:
- **Tại sao** cần học (WHY) — giải thích vấn đề được giải quyết
- **Khái niệm cốt lõi** (WHAT) — định nghĩa, mô hình tư duy
- **Code ví dụ thực tế** (HOW) — chạy được, có comment
- **Các lỗi thường gặp** (Gotchas) — ❌ sai → ✅ đúng
- **Bài tập thực hành** — ít nhất 3 bài tăng dần độ khó
- **Tài nguyên thêm** — link chất lượng (docs chính thức, sách, khóa học)

### 4. Code examples

- Dùng **ví dụ thực tế**, không dùng `foo/bar/baz`
- Luôn có **comment tiếng Anh** giải thích dòng quan trọng
- Phân biệt ❌ sai và ✅ đúng khi cần
- Ví dụ phải **chạy được** và đúng cú pháp

### 5. Ngôn ngữ

- **Tiêu đề section** và **giải thích**: **Tiếng Việt**
- **Code, tên biến, comments trong code**: **Tiếng Anh**
- **Technical terms**: Dùng tiếng Anh + giải thích tiếng Việt lần đầu xuất hiện
  → Ví dụ: *Event Loop (vòng lặp xử lý sự kiện)*

### 6. Cấp độ — Gắn ở đầu mỗi bài

```markdown
> `[BEGINNER]` — Không cần kiến thức trước
> `[INTERMEDIATE]` — Cần biết nền tảng
> `[ADVANCED]` — Yêu cầu kinh nghiệm
> `[MUST-KNOW]` ⭐ — Kiến thức không thể thiếu
```

Có thể kết hợp: `` `[BEGINNER → INTERMEDIATE]` ⭐ `[MUST-KNOW]` ``

### 7. Trạng thái trong MASTER-CATALOG.md

Sau khi viết bài, cập nhật trạng thái trong `MASTER-CATALOG.md`:
- `✅` — Bài đầy đủ (có đủ template, code, bài tập, tài nguyên)
- `🚧` — Có skeleton (cần mở rộng thêm)
- `❌` — Chưa có (cần tạo mới)

---

## Quy trình thêm bài mới

1. Mở `MASTER-CATALOG.md` → tìm bài muốn viết (trạng thái ❌ hoặc 🚧)
2. Tạo file theo đúng thư mục và tên quy định
3. Copy từ `_templates/article-template.md`
4. Viết nội dung theo quy tắc trên
5. Cập nhật trạng thái trong `MASTER-CATALOG.md` → `✅`

---

## Nội dung cần tránh

- ❌ Thời gian ước tính (mỗi người học khác nhau)
- ❌ Thông tin outdated/deprecated (kiểm tra version/ngày viết)
- ❌ Copy-paste từ tài liệu gốc mà không thêm giá trị
- ❌ Bài viết quá dài mà không có cấu trúc rõ ràng
- ❌ Code không có comment, khó hiểu
- ❌ Tiêu đề section bằng tiếng Anh (phải là tiếng Việt)
- ❌ Thiếu phần Bài tập hoặc Tài nguyên thêm

---

## Cảm ơn mọi đóng góp! 🙏
