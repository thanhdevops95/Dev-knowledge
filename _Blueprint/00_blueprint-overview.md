# 📐 Blueprint Overview — Bản thiết kế chi tiết Repo Tri thức CNTT

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.2.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 15/05/2026

> 🎯 *File này giải thích **Blueprint là gì**, **dùng để làm gì**, **ai đọc**, và **cách áp dụng**. Đọc file này trước khi đi sâu vào bất kỳ file `0X_*.md` nào khác trong thư mục.*

---

## 1️⃣ Blueprint là gì

Blueprint là **bản thiết kế kỹ thuật chi tiết** của Repo Tri thức CNTT. Nó chuyển ý tưởng (vision) thành **đặc tả triển khai** (spec) — đủ rõ để bất kỳ người viết bài nào, sau khi đọc xong, đều có thể bắt tay vào sản xuất nội dung mà không cần hỏi lại.

### So sánh nhanh

| | `_idea-overview.md` | `_Blueprint/` |
|---|---|---|
| **Vai trò** | Tầm nhìn — *làm cái gì, vì sao* | Thiết kế — *làm như thế nào* |
| **Độ trừu tượng** | Cao (chiến lược) | Thấp (cụ thể, có thể thực thi) |
| **Đối tượng đọc** | Người muốn hiểu mục đích kho | Người sắp viết bài / đóng góp |
| **Tần suất sửa** | Ít (chỉ khi đổi định hướng) | Trung bình (khi chuẩn được tinh chỉnh) |
| **Output** | Đoạn văn, sơ đồ tổng | Quy tắc, template, checklist |

---

## 2️⃣ Dùng để làm gì

Blueprint giải quyết **5 câu hỏi cụ thể** mà người viết bài luôn gặp:

| Câu hỏi của người viết | File trong blueprint trả lời |
|---|---|
| *"Chủ đề này nằm ở đâu trong kho?"* | `01_sitemap-detail.md` |
| *"Bài viết của tôi đặt vào folder nào, đặt tên ra sao?"* | `02_folder-structure.md` + `04_naming-convention.md` |
| *"Viết theo cấu trúc gì, văn phong nào?"* | `03_writing-style.md` |
| *"Link tới bài khác / thuật ngữ như thế nào?"* | `05_linking-strategy.md` |
| *"Trước khi publish cần kiểm tra gì?"* | `07_quality-checklist.md` |

Riêng `06_roadmap-design.md` phục vụ một nhu cầu khác: **thiết kế lộ trình học** (roadmap) — vốn không phải bài kiến thức mà là layer điều hướng.

---

## 3️⃣ Đối tượng đọc

| Nhóm | Họ đọc blueprint khi nào |
|---|---|
| 👤 **Chính chủ kho (Mr.Rom)** | Mỗi lần bắt đầu viết bài mới, soát lại convention |
| 🆕 **Người đóng góp mới** | Lần đầu vào kho — đọc để hiểu cách viết bài "đúng chuẩn" |
| 🔄 **Người đóng góp cũ** | Khi quy tắc được cập nhật, hoặc khi gặp tình huống không chắc |
| 🤖 **AI assistant** | Khi được nhờ viết/sửa bài — đọc blueprint để giữ nhất quán |

> 📌 Blueprint **không** phải là tài liệu cho người *học* kiến thức — họ đọc các bài trong các chủ đề L1.

---

## 4️⃣ Cách áp dụng

### Khi viết bài mới — quy trình 5 bước

```mermaid
flowchart LR
    A[1. Tra sitemap<br/>chủ đề ở đâu] --> B[2. Vào folder đúng<br/>theo folder-structure]
    B --> C[3. Copy template<br/>từ templates/]
    C --> D[4. Viết theo<br/>writing-style]
    D --> E[5. Soát qua<br/>quality-checklist]
```

| Bước | Tra file | Kết quả |
|---|---|---|
| 1 | `01_sitemap-detail.md` | Biết chủ đề thuộc L1 nào |
| 2 | `02_folder-structure.md` + `04_naming-convention.md` | Biết đặt vào folder con nào, đặt tên file ra sao |
| 3 | `templates/lesson_template.md` | Có khung sẵn để bắt đầu |
| 4 | `03_writing-style.md` + `05_linking-strategy.md` | Viết đúng văn phong, link chéo đúng cách |
| 5 | `07_quality-checklist.md` | Soát lỗi trước khi publish |

### Khi thiết kế roadmap — đi thẳng

→ `06_roadmap-design.md` có template + ví dụ riêng.

---

## 5️⃣ Trạng thái Blueprint (Living Document)

Blueprint **không đóng băng** — nó tiến hóa cùng kho:

| Sự kiện | Hành động |
|---|---|
| Tìm thấy convention mới hợp lý hơn | Cập nhật file tương ứng + bump version |
| Phát hiện mâu thuẫn giữa các file | Sửa cho thống nhất, ghi changelog |
| Có chủ đề L1 mới phát sinh | Thêm vào `01_sitemap-detail.md` |
| Mẫu template lỗi thời | Cập nhật trong `templates/` |

**Mọi thay đổi quan trọng → ghi vào mục "Changelog" cuối từng file**.

---

## 6️⃣ Quy ước trong các file Blueprint

Để Blueprint tự nhất quán với chính nó, các file `0X_*.md` đều tuân:

### Bố cục chuẩn

```markdown
# <Tiêu đề>

> Metadata header (Author, Version, Created, Updated)
> 🎯 Câu dẫn 1 dòng tóm lược file

## 1️⃣ <Phần chính 1>
## 2️⃣ <Phần chính 2>
...
## 🧪 Ví dụ thực tế (nếu có)
## ⚠️ Lỗi thường gặp (nếu có)
## 📌 Changelog
```

### Ký hiệu emoji nhất quán

→ **Canonical**: [`03_writing-style.md` §5](./03_writing-style.md#5️⃣-emoji--bộ-chuẩn-nhất-quán)

Bộ emoji chuẩn cho section marker (🎯 mục tiêu, 📖 lý thuyết, 💡 pitfall, 🧠 self-check, ⚡ cheatsheet, 📚 glossary, 🔗 liên kết, ...) và inline (✅ ❌ ⚠️ 🟢🟡🔴 🚧 🆕 ...). Đầy đủ bảng + quy tắc dùng trong `03_writing-style.md`.

### Ngôn ngữ

- Tiếng Việt có dấu (UTF-8 NFC).
- Thuật ngữ EN giữ nguyên, *in nghiêng lần đầu*.
- Tên file/folder/code: tiếng Anh, theo convention chung của workspace ([[naming-files]], [[naming-folders]]).

---

## 7️⃣ Quan hệ với hệ thống Skills của Mr.Rom

Blueprint này **kế thừa và mở rộng** các skill toàn cục đã có ở `~/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/00_Skills/Skills-for-me/`:

| Skill toàn cục | Blueprint áp dụng vào |
|---|---|
| `naming/files.md`, `naming/folders.md`, `naming/numbering.md` | `04_naming-convention.md` (chuyên biệt cho nội dung trong kho) |
| `naming/metadata-headers.md` | Header chuẩn của mọi bài học |
| `coding/revision-tracking.md` | Cách đánh dấu nội dung lỗi thời trong bài |
| `language/vietnamese.md` | Toàn bộ chuẩn ngôn ngữ |

> Blueprint **không lặp lại** những quy tắc đã có ở Skills toàn cục — chỉ **trỏ tới** và bổ sung phần riêng cho repo kiến thức này.

---

## 📌 Changelog

- **v0.2.0 (15/05/2026)** — Slim §6 phần emoji table — chỉ giữ tóm tắt + link tới canonical (`03_writing-style.md` §5). Tránh drift.
- **v0.1.0 (15/05/2026)** — Bản đầu tiên. Chốt: định nghĩa Blueprint, phân biệt với Idea, nêu 5 câu hỏi blueprint giải quyết, đối tượng đọc, quy trình 5 bước áp dụng khi viết bài, bố cục chuẩn + ký hiệu emoji nhất quán trong blueprint.
