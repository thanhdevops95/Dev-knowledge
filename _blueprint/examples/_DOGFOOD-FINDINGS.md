# 🐕 Dogfood Findings — Test Blueprint v1.1 với bài mẫu

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.1.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 15/05/2026

> 🎯 *Ghi nhận gì OK / gì thiếu / gì gây vướng khi áp dụng Blueprint v1.1 thực tế. Bài thử: `sample_short-lesson_git-status.md` (short lesson pattern — chỉ REQUIRED + 1 OPTIONAL).*

---

## 1️⃣ Bài thử đã viết

- File: [`sample_short-lesson_git-status.md`](./sample_short-lesson_git-status.md)
- Topic: `git status` command
- Mục đích test: **short lesson pattern** — bài ngắn (<5 phút đọc), chỉ dùng phần REQUIRED + 1 OPTIONAL (cheatsheet)
- Khác sample `kubernetes-pod`: domain khác (Git vs K8s), độ dài khác (ngắn vs đầy đủ 8 phần)

## 2️⃣ Phần nào OK — Blueprint hoạt động tốt

| Phần | Đánh giá |
|---|---|
| ✅ **Khung 8 phần** | Linh hoạt — bỏ Pitfall, Self-check, Liên kết tự nhiên, không "chế cháo" |
| ✅ **Metadata header** | Đủ field, không thừa |
| ✅ **WHY → WHAT → HOW** | Áp dụng tốt cho command đơn giản — WHY hook người đọc, WHAT định nghĩa, HOW hands-on |
| ✅ **Câu dẫn** | "Câu dẫn đầu file" + "câu dẫn giữa section" làm bài liền mạch |
| ✅ **Tag `[MUST-KNOW]`** | Hợp lý cho git status — command thiết yếu |
| ✅ **Cheatsheet OPTIONAL** | Dùng được cho bài ngắn — không bắt buộc bài lớn |
| ✅ **Glossary** | Bảng EN↔VN đủ thông tin, không cần subsection thêm |
| ✅ **Mermaid diagram** | Render được trong VS Code / GitHub preview |

## 3️⃣ Phát hiện — Blueprint **cần chỉnh** 5 chỗ

### 🟡 #1: Câu dẫn đầu file vs câu dẫn ở metadata — chồng chéo

**Quan sát**: Khung hiện tại có:
- Metadata header có `> 🎯 *...*` câu dẫn ở dòng cuối block quote
- Section "Câu dẫn + Mục tiêu" cũng có `> 🎯 *...*` riêng

→ Khi viết, mình bị nhầm: 2 chỗ đều là "câu dẫn", có phải lặp không?

**Khuyến nghị**:
- **Câu dẫn 1 (sau metadata)** = positioning ngắn ("Bài này test pattern X" hoặc bỏ qua nếu không có meta-message)
- **Câu dẫn 2 (trước Mục tiêu)** = câu dẫn nội dung ("Sau bài này bạn làm được Z")

→ Cập nhật `03_writing-style.md` §2.2 làm rõ phân biệt 2 câu dẫn, hoặc gộp lại 1 chỗ.

### 🟡 #2: Heading H2 `## 🎯 Sau bài này bạn sẽ` chiếm số `1️⃣` nhưng nội dung WHY lại bắt đầu từ `## 1️⃣`

**Quan sát**: Trong bài thử mình đặt:
```
## 🎯 Sau bài này bạn sẽ     ← không có số
...
## 1️⃣ Vì sao cần git status (WHY)
## 2️⃣ Git status là gì (WHAT)
## 3️⃣ Cách dùng (HOW)
```

→ "Mục tiêu" không có số (vì nó là phần khung, không phải nội dung) còn nội dung chính bắt đầu từ 1️⃣. Có thể gây nhầm "Tại sao Mục tiêu không phải bài đầu tiên?"

**Khuyến nghị**:
- Convention rõ: "Mục tiêu" là **phần khung**, không đánh số. Chỉ "Nội dung chính" mới đánh số 1️⃣ 2️⃣ 3️⃣...
- Hoặc thử kiểu khác: "Mục tiêu" = `## 🎯 Mục tiêu` không số, "Nội dung" có phân heading nội bộ.

→ Cập nhật `03_writing-style.md` §1 hoặc thêm spec rõ vào template.

### 🟡 #3: Thiếu hướng dẫn **độ dài tối thiểu của câu dẫn**

**Quan sát**: Khi viết, mình phân vân: câu dẫn nên 1 dòng hay 1 đoạn? Hiện Blueprint chỉ nói "câu dẫn" chung chung.

**Khuyến nghị**:
- Câu dẫn đầu file: **1-2 câu**, không quá dài
- Câu dẫn giữa section: **1 câu** nối, in nghiêng trong block quote

→ Cập nhật `03_writing-style.md` §2.2 hoặc §3.3.

### 🟢 #4: Khi nào skip phần Liên kết — cần làm rõ

**Quan sát**: Bài thử mình bỏ phần "Liên kết & Tài nguyên" vì chưa có bài liên quan (kho chưa có content). Nhưng Blueprint nói "OPTIONAL khi không có bài liên quan".

→ Có thể hiểu lầm: "không có bài liên quan trong kho hiện tại" vs "topic không có bài liên quan ngoài đời".

**Khuyến nghị**:
- Làm rõ: bỏ "Liên kết" khi không có gì đáng link (cả internal lẫn external)
- Nếu có resource ngoài đáng giá → vẫn nên có section "Liên kết" dù chưa có bài internal

→ Cập nhật `03_writing-style.md` §2.8.

### 🟢 #5: Template lesson_template.md có comment `<!-- OPTIONAL -->` — clutter khi viết bài thật

**Quan sát**: Khi copy template để viết, các comment `<!-- OPTIONAL -->` hiển thị trong preview (mặc dù không render). Nhưng nhìn source thì rối.

**Khuyến nghị**:
- Giữ comment để biết section nào OPT — vẫn cần
- Nhưng nhắc trong template README: "Sau khi viết xong → xóa comment để file sạch"

→ Cập nhật `templates/README.md` thêm 1 dòng quy ước.

## 4️⃣ Đề xuất KHÔNG đổi — đã OK

- ✅ Cấu trúc folder 5 cấp (root → L1 → L2 → L3 → L4 → file)
- ✅ Menu 7 loại nội dung
- ✅ Naming convention (NN_, _, 99_, 00_)
- ✅ Glossary 3 cấp
- ✅ Cross-L2 pattern
- ✅ MASTER-CATALOG + CONTRIBUTING spec
- ✅ Bộ emoji nhất quán

## 5️⃣ Quyết định áp dụng

| # | Sửa gì | File canonical | Ưu tiên |
|---|---|---|---|
| 1 | Phân biệt 2 câu dẫn (metadata vs mục tiêu) | `03_writing-style.md` §2.2 | 🟡 TB |
| 2 | Quy ước đánh số H2 (chỉ nội dung chính có số, mục tiêu không) | `03_writing-style.md` §1 hoặc template | 🟡 TB |
| 3 | Độ dài tối thiểu câu dẫn | `03_writing-style.md` §3.3 | 🟢 Thấp |
| 4 | Làm rõ khi nào skip Liên kết | `03_writing-style.md` §2.8 | 🟢 Thấp |
| 5 | Nhắc xóa comment `<!-- OPT -->` khi viết xong | `templates/README.md` | 🟢 Thấp |

→ Tổng cộng: **5 chỉnh sửa nhỏ** trong `03_writing-style.md` và `templates/README.md`. Không có thay đổi cấu trúc lớn.

## 6️⃣ Tiếp theo

- [x] Áp dụng 5 chỉnh sửa nhỏ trên — DONE (v0.2.0)
- [x] Bump `03_writing-style.md` → v0.3.0 — DONE
- [x] Bump `templates/README.md` (thêm note) — DONE
- [x] Test thêm pattern: **exercise** + **recipe** — DONE

---

## 7️⃣ Dogfood vòng 2 — exercise + recipe pattern

### Bài thử thêm

| File | Pattern test |
|---|---|
| [`sample_exercise_create-first-pod.md`](./sample_exercise_create-first-pod.md) | Exercise pattern — đề bài, gợi ý ẩn, đáp án ẩn, verify, mở rộng |
| [`sample_recipe_pod-crashloopbackoff.md`](./sample_recipe_pod-crashloopbackoff.md) | Recipe pattern (troubleshooting) — Problem → Cause → Solution → Verify → Prevention |

### Template vừa tạo

- [`templates/exercise_template.md`](../templates/exercise_template.md) — chuẩn cho bài tập
- [`templates/recipe_template.md`](../templates/recipe_template.md) — chuẩn cho recipe troubleshooting/pattern/operation

### Phát hiện thêm

| # | Quan sát | Đánh giá |
|---|---|---|
| 6 | **Exercise có nhiều "ẩn" (`<details>`)** — gợi ý + đáp án | ✅ Hoạt động tốt, GitHub render OK |
| 7 | **Recipe có cấu trúc rõ rệt khác lesson** — không có Mục tiêu/WHY→WHAT→HOW, mà là Problem → Cause → Solution | ✅ Justified template riêng (không reuse lesson_template) |
| 8 | **Recipe có bảng "Nguyên nhân + Khả năng + Cách xác định"** — quan sát hay | ✅ Adopt vào template |
| 9 | **Exercise level: ⭐ ⭐⭐ ⭐⭐⭐** thay vì Basic/Inter/Advanced | 💡 Khác lesson — exercise dùng độ khó star, lesson dùng Level. Mỗi loại có metadata phù hợp |
| 10 | **Recipe có `Áp dụng cho: <version>`** | ✅ Quan trọng cho troubleshooting — bug đổi theo version |

### Đánh giá tổng kết

- ✅ Cả 2 pattern (exercise + recipe) **chạy tốt** với Blueprint hiện tại
- ✅ Không cần điều chỉnh thêm Blueprint config
- ✅ Template chuẩn — đủ chi tiết, không thừa
- ✅ Style guide §1 (8 phần) chỉ áp dụng cho `lessons/`. Exercise + recipe có cấu trúc khác (đã spec ở template riêng)

→ Đề xuất: thêm note ở `03_writing-style.md` §1 nói rõ "khung 8 phần áp dụng cho `lessons/`. Exercise và Recipe có template + cấu trúc riêng".

---

---

## 8️⃣ Dogfood vòng 3 — bài thật K8s Deployment (16/05/2026)

### Bài thử thêm

- File: [`sample_lesson_k8s-deployment.md`](./sample_lesson_k8s-deployment.md)
- Topic: K8s Deployment (chủ đề chưa có sample, MUST-KNOW)
- Goal: **dogfood Reference workflow mới** (v1.3 §15 quality-checklist) — viết draft solo trước, sau cherry-pick từ `_Ref/`

### Workflow đã thực hiện

| Phase | Việc | Thời gian |
|---|---|---|
| 1. Draft solo | Viết bài theo Blueprint + kiến thức riêng. KHÔNG mở `_Ref/` | ~25 phút |
| 2. Cherry-pick | Mở `_Ref/K8s-training/07_deployment/` skim 2 file (README + 08-strategies) | ~5 phút |
| 3. Adopt | Thêm §4 Recreate strategy + 3 use case cụ thể; cập nhật default %maxSurge | ~5 phút |
| 4. Quality | Đi qua checklist quick | ~5 phút |
| **Total** | | **~40 phút** |

→ **Time-box 15 phút tham khảo** (§15 quality-checklist) bị break — mất 10 phút (skim + adopt). Reasonable cho bài đầu tiên dogfood; sẽ nhanh hơn khi quen.

### Phát hiện

| # | Quan sát | Đánh giá |
|---|---|---|
| 11 | **Draft solo nhanh hơn dự kiến** — biết topic thì viết 25 phút có bài 600+ dòng | ✅ Workflow chạy |
| 12 | **Cherry-pick có giá trị thật** — bài thiếu Recreate strategy, _Ref/K8s-training bù được | ✅ Justified workflow |
| 13 | **Skim file _Ref/ rất nhanh** — chỉ cần đọc TOC + 1-2 H2 chính là biết có gì hay | ✅ Time-box realistic |
| 14 | **Không bị influence sai hướng** — vì draft trước, _Ref/ chỉ là "validation + add-on" | ✅ Mindset đúng |
| 15 | **Bài v1.0 → v1.1 sau cherry-pick** — version bump rõ ràng, changelog ghi nguồn | ✅ Version control work |

### Findings cần fix Blueprint?

**Không có fix mới.** Blueprint v1.3 chạy tốt cho workflow Reference. 1 chú ý nhỏ:

| Quan sát | Có cần update Blueprint? |
|---|---|
| Time-box 15 phút có thể hơi tight cho người mới | ❌ Để vậy — sẽ nhanh khi quen, ép sớm là tốt |
| Cherry-pick từ K8s-training rất "smooth" vì file đã có structure | ✅ Notes: `_Ref/K8s-training/` là gold mine — chọn ưu tiên skim khi tham khảo K8s |

### Tổng kết

- ✅ **Workflow Reference (Blueprint v1.3 §15) chạy đúng như design**
- ✅ Draft solo → cherry-pick → adopt là approach phù hợp
- ✅ `_Ref/` có giá trị THỰC nếu cherry-pick đúng — không phải toàn rác
- ✅ Mindset "Blueprint + ý riêng = chủ đạo, `_Ref/` = inspiration" cảm nhận tự nhiên khi viết

→ **Blueprint v1.3 final-ready cho production viết bài**.

---

## 📌 Changelog

- **v0.3.0 (16/05/2026)** — Dogfood vòng 3 với bài thật K8s Deployment. Workflow Reference (cherry-pick) chạy đúng. Không cần fix Blueprint thêm.
- **v0.2.0 (15/05/2026)** — Apply 5 fix xong + dogfood vòng 2 (exercise + recipe). Đề xuất 1 fix nhỏ thêm cho §1 writing-style.
- **v0.1.0 (15/05/2026)** — Bản đầu tiên. Ghi nhận 5 chỗ Blueprint cần chỉnh sau khi viết bài thử git status.
