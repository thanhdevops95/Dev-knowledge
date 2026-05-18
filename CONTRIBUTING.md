# 🤝 Contributing — Repo Tri Thức CNTT

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 16/05/2026\
> **Cập nhật:** 16/05/2026

> Cảm ơn bạn đã quan tâm đóng góp cho **Repo Tri Thức CNTT**! File này hướng dẫn cách contribute để giữ nhất quán với chuẩn của kho.

---

## 1️⃣ Quy trình đóng góp

```mermaid
flowchart LR
    A[1. Fork / clone] --> B[2. Đọc _Blueprint/]
    B --> C[3. Copy template]
    C --> D[4. Viết theo writing-style]
    D --> E[5. Soát quality checklist]
    E --> F[6. Cập nhật MASTER-CATALOG]
    F --> G[7. Mở PR]
```

| Bước | Chi tiết |
|---|---|
| 1 | Fork repo về tài khoản, clone về local |
| 2 | Đọc `_Blueprint/` để hiểu cấu trúc + chuẩn viết (đặc biệt `00_blueprint-overview.md`) |
| 3 | Vào `_Blueprint/templates/` copy template phù hợp loại bài |
| 4 | Viết theo `_Blueprint/03_writing-style.md` (khung 8 phần, WHY→WHAT→HOW) |
| 5 | Soát qua `_Blueprint/07_quality-checklist.md` — tick mọi mục |
| 6 | Cập nhật `MASTER-CATALOG.md` với entry bài mới (status: ✅/🚧) |
| 7 | Mở PR theo template (ngay trong repo) |

---

## 2️⃣ Cấu trúc PR

PR title format: `<type>: <description>`. Type: `feat` / `fix` / `docs` / `refactor` / `chore`.

Ví dụ:
- `feat: add Pod lesson basic`
- `fix: typo in deployment.md`
- `docs: update naming convention`

PR body nên có:

```markdown
## Tóm tắt
<1-3 câu mô tả PR làm gì>

## File thay đổi
- <list file mới/sửa>

## Quality checklist
- [ ] Đã soát theo `_Blueprint/07_quality-checklist.md`
- [ ] Code mẫu đã test chạy
- [ ] Link nội bộ + external đã test
- [ ] Cập nhật MASTER-CATALOG.md
- [ ] Bump version file (nếu sửa file đã có)
```

---

## 3️⃣ Nội dung cần tránh (anti-patterns)

| ❌ Anti-pattern | 💡 Lý do |
|---|---|
| Bài thiếu câu dẫn — section nhảy ngang | Người đọc vấp khi đọc, mất flow |
| Code mẫu chưa test | Người đọc gặp lỗi, mất niềm tin vào kho |
| Heading tiếng Anh trong bài VN | Vi phạm ngôn ngữ chính của kho |
| Ước tính thời gian thiếu căn cứ ("học X trong 1 ngày") | Tạo expectation sai |
| Copy-paste từ nguồn khác không thêm value | Vi phạm Evergreen + DRY |
| Outdated content (vd: API version cũ) | Người đọc làm theo sẽ lỗi |
| Hardcode credential thật (password, API key) | Bảo mật |
| Hardcode đường dẫn tuyệt đối trên máy author | Người khác không chạy được |
| File rỗng không có placeholder | Git track nhưng vô dụng |
| Tag MUST-KNOW lạm dụng | Phá ý nghĩa của tag — chỉ ~20-30% bài là MUST-KNOW |
| Tạo loại nội dung mới ngoài 7 lõi mà không cập nhật Blueprint | Drift cấu trúc |

---

## 4️⃣ Badges level trong metadata

Mỗi bài lesson có Level trong metadata:

| Badge | Áp dụng cho |
|---|---|
| `Basic` | Beginner zero-base có thể hiểu |
| `Intermediate` | Đã biết cơ bản, học nâng cao 1 chút |
| `Advanced` | Chuyên sâu, cần nền vững |
| Tag `[MUST-KNOW]` | Bài bắt buộc trong roadmap tương ứng (vd: Pod cho DevOps roadmap) |

Chi tiết: `_Blueprint/03_writing-style.md` §2.1.

---

## 5️⃣ Văn phong

| Nguyên tắc | Tham chiếu |
|---|---|
| Tiếng Việt có dấu, EN cho thuật ngữ | `_Blueprint/03_writing-style.md` §3.1 |
| Xưng hô: tác giả = mình/Mr.Rom, đọc = bạn | `_Blueprint/03_writing-style.md` §3.1 |
| Câu dẫn liền mạch | `_Blueprint/03_writing-style.md` §3.3 |
| Cấm sáo rỗng | `_Blueprint/03_writing-style.md` §3.4 |
| Khung 8 phần bài | `_Blueprint/03_writing-style.md` §1 |
| WHY → WHAT → HOW | `_Blueprint/03_writing-style.md` §2.3 |

---

## 6️⃣ Đặt tên

Tuân theo `_Blueprint/04_naming-convention.md`. Tóm tắt:

- File: kebab-case, tiếng Anh, đánh số `NN_` nếu trong series
- Folder L1: `NN_Name/` (sentence case)
- Folder L2 trở xuống: `name/` (lowercase)
- Meta: prefix `_` (vd `_glossary.md`, `_notes/`)

---

## 7️⃣ Liên kết

Tuân theo `_Blueprint/05_linking-strategy.md`. Tóm tắt:

- Internal: dùng relative path
- Link text mô tả đích — không "click here"
- Navigation footer cuối bài
- Cross-L2: dùng pattern 3-cách (đi từ stage trước / clone / build mới)
- Thuật ngữ EN: thêm vào glossary 3 cấp

---

## 8️⃣ Tham khảo `_Ref/` — Reference workflow

> ⚠️ **`_Ref/` ở folder `../_Ref/` chứa content cũ**. KHÔNG migrate / copy nguyên. Đó chỉ là **source of inspiration**.

Quy trình đúng khi muốn tham khảo:

1. **Viết draft đầu** theo Blueprint + ý tưởng riêng. **KHÔNG mở `_Ref/` ở bước này.**
2. Sau khi có draft → mở `../_Ref/_FILE-CATALOG.md` tìm file liên quan
3. Skim 1-2 file ~5 phút mỗi
4. **Cherry-pick** ý hay: ẩn dụ, ví dụ, diagram, pitfall, cheatsheet shortcut, thuật ngữ
5. Bỏ phần rác/lỗi thời — không "tiếc"
6. Time-box tham khảo: **15 phút/bài tối đa**

Chi tiết workflow → [`_Blueprint/07_quality-checklist.md`](_Blueprint/07_quality-checklist.md) §15.

---

## 9️⃣ Liên hệ

- Bug / suggestion: open Issue trong repo
- PR review: ping `@<owner>` trong PR
- Câu hỏi lớn: discussion ở Issues hoặc kênh team

---

## 📌 Changelog

- **v1.0.0 (16/05/2026)** — Bản đầu tiên. Quy trình 7 bước + 11 anti-patterns + Reference workflow (cherry-pick từ `_Ref/`).
