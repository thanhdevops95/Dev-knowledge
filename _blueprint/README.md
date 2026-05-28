# 📘 Blueprint — Bản thiết kế chi tiết Repo Tri thức CNTT

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 26/05/2026

Đây là **bản thiết kế chi tiết** (blueprint) để hiện thực hóa ý tưởng đã phác thảo trong [`../_idea-overview.md`](../_idea-overview.md).

Mọi quyết định về *cách kho được xây dựng* (cấu trúc, tên file, chuẩn viết, link chéo, template...) đều nằm trong thư mục này. Khi viết bài mới, đầu tiên tra blueprint, sau đó mới viết nội dung.

---

## 1️⃣ Blueprint là gì

Blueprint là **bản thiết kế kỹ thuật chi tiết** của Repo Tri thức CNTT. Nó chuyển ý tưởng (vision) thành **đặc tả triển khai** (spec) — đủ rõ để bất kỳ người viết bài nào, sau khi đọc xong, đều có thể bắt tay vào sản xuất nội dung mà không cần hỏi lại.

### So sánh nhanh

| Đặc điểm | `_idea-overview.md` | `_blueprint/` |
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
| *"Chủ đề này nằm ở đâu trong kho?"* | [`01_sitemap-detail.md`](./01_sitemap-detail.md) |
| *"Bài viết của tôi đặt vào folder nào, đặt tên ra sao?"* | [`02_folder-structure.md`](./02_folder-structure.md) *(Đã gộp Quy ước đặt tên)* |
| *"Viết theo cấu trúc gì, văn phong nào, Alert ra sao?"* | [`03_writing-style.md`](./03_writing-style.md) |
| *"Link tới bài khác / thuật ngữ như thế nào?"* | [`05_linking-strategy.md`](./05_linking-strategy.md) |
| *"Trước khi publish cần kiểm tra gì?"* | [`07_quality-checklist.md`](./07_quality-checklist.md) |

Riêng [`06_roadmap-design.md`](./06_roadmap-design.md) phục vụ một nhu cầu khác: **thiết kế lộ trình học** (roadmap) — vốn không phải bài kiến thức mà là layer điều hướng.

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

## 4️⃣ Cách áp dụng khi viết bài mới — Quy trình 5 bước

```mermaid
flowchart LR
    A[1. Tra sitemap<br/>chủ đề ở đâu] --> B[2. Vào folder đúng<br/>theo folder-structure]
    B --> C[3. Copy template<br/>từ templates/]
    C --> D[4. Viết theo<br/>writing-style]
    D --> E[5. Soát qua<br/>quality-checklist]
```

| Bước | Tra file | Kết quả |
|---|---|---|
| 1 | [`01_sitemap-detail.md`](./01_sitemap-detail.md) | Biết chủ đề thuộc L1 nào |
| 2 | [`02_folder-structure.md`](./02_folder-structure.md) | Biết đặt vào folder con nào, đặt tên file ra sao nhờ quy tắc tích hợp |
| 3 | [`templates/lesson_template.md`](./templates/lesson_template.md) | Có khung sẵn để bắt đầu |
| 4 | [`03_writing-style.md`](./03_writing-style.md) + [`05_linking-strategy.md`](./05_linking-strategy.md) | Viết đúng văn phong, chèn Alert Box hợp lý, link chéo đúng cách |
| 5 | [`07_quality-checklist.md`](./07_quality-checklist.md) | Soát lỗi trước khi publish |

---

## 5️⃣ Danh mục file Spec chi tiết

| File | Vai trò | Trạng thái |
|---|---|---|
| [`README.md`](./README.md) | File bạn đang đọc — cổng tổng quan của Blueprint | v1.0.0 (Gộp Overview) |
| [`_CONCEPT-MAP.md`](./_CONCEPT-MAP.md) | **SSOT register** — concept nào ở file nào (tra trước khi sửa) | v0.5.0 |
| [`01_sitemap-detail.md`](./01_sitemap-detail.md) | Sitemap mở rộng L1 → L2 → L3 của toàn bộ kho | v0.4.0 |
| [`02_folder-structure.md`](./02_folder-structure.md) | Cấu trúc folder/file chuẩn + Quy ước đặt tên + hub setup | v1.0.0 (Gộp Naming) |
| [`03_writing-style.md`](./03_writing-style.md) | Chuẩn viết: WHY→WHAT→HOW, ẩn dụ, emoji, **Quy chuẩn Alert Boxes** | v0.6.0 (Thêm Alert Box) |
| [`05_linking-strategy.md`](./05_linking-strategy.md) | Link chéo, glossary, cross-L2 pattern | v0.1.0 |
| [`06_roadmap-design.md`](./06_roadmap-design.md) | Cách thiết kế roadmap, template, ví dụ | v0.1.0 |
| [`07_quality-checklist.md`](./07_quality-checklist.md) | Checklist kiểm tra trước khi publish bài | v0.3.0 |

### 📁 Thư mục con hỗ trợ

| Thư mục | Nội dung |
|---|---|
| [`templates/`](./templates/) | Các template thật để copy-paste khi viết bài (`lesson_template.md`, `topic-readme_template.md`, `roadmap_template.md`, `overview_template.md`, `_cheatsheet.md`) |
| [`examples/`](./examples/) | 1 chủ đề mẫu viết hoàn chỉnh để tham chiếu |

---

## 6️⃣ Quy ước chung trong các file Blueprint

Để Blueprint tự nhất quán với chính nó, các file `0X_*.md` đều tuân:

### Bố cục chuẩn

```markdown
# <Tiêu đề>

> Metadata header (Author, Version, Created, Updated)
> 🎯 Câu dẫn 1 dòng tóm lược file

## 1️⃣ <Phần chính 1>
## 2️⃣ <Phần chính 2>
...
## ⚠️ Lỗi thường gặp (nếu có)
## 📌 Changelog
```

### Ký hiệu emoji nhất quán

→ **Canonical**: [`03_writing-style.md` §5](./03_writing-style.md#5️⃣-emoji--bộ-chuẩn-nhất-quán)

Bộ emoji chuẩn cho section marker (🎯 mục tiêu, 📖 lý thuyết, 💡 pitfall, 🧠 self-check, ⚡ cheatsheet, 📚 glossary, 🔗 liên kết, ...) và inline (✅ ❌ ⚠️ 🟢🟡🔴 🚧 🆕 ...). Đầy đủ bảng + quy tắc dùng trong `03_writing-style.md`.

---

## 7️⃣ Quan hệ với hệ thống Skills của Mr.Rom

Blueprint này **kế thừa và mở rộng** các skill toàn cục đã có ở `~/Library/CloudStorage/OneDrive-Personal/Desktop/Dev/00_Skills/skills-for-me/`:

| Skill toàn cục | Blueprint áp dụng vào |
|---|---|
| `naming/files.md`, `naming/folders.md` | [`02_folder-structure.md`](./02_folder-structure.md) (Quy ước đặt tên nội bộ) |
| `naming/metadata-headers.md` | Header chuẩn của mọi bài học |
| `coding/revision-tracking.md` | Cách đánh dấu nội dung lỗi thời trong bài |
| `language/vietnamese.md` | Toàn bộ chuẩn ngôn ngữ |

> Blueprint **không lặp lại** những quy tắc đã có ở Skills toàn cục — chỉ **trỏ tới** và bổ sung phần riêng cho repo kiến thức này.

---

## 📌 Changelog

- **v1.0.0 (26/05/2026)** — **Tái cấu trúc lớn (Gộp file)**:
  - Gộp hoàn toàn file `00_blueprint-overview.md` vào `README.md` của Blueprint để tinh gọn, loại bỏ lặp lại vai trò.
  - Cập nhật danh mục file để phản ánh việc gộp `04_naming-convention.md` vào `02_folder-structure.md`.
  - Đồng bộ hóa quy ước Cheatsheet thành `_cheatsheet.md` xuyên suốt tài liệu.
- **v0.1.0 (15/05/2026)** — Bản đầu tiên.
