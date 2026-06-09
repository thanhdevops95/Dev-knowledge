# ✅ Checklist Kiểm Tra & Hoàn Thiện Bài (Lesson QA)

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** 01/06/2026\
> **Cập nhật:** 01/06/2026

> 🎯 *Quy trình kiểm tra + hoàn thiện 1 bài, đúc kết từ đợt làm cụm Docker. Dùng cho: (1) hoàn thiện bộ Docker, (2) review lại từng bài đã làm, (3) làm cơ sở góp ý cho `_blueprint/07_quality-checklist.md`. Bài mẫu văn phong chuẩn: `10_devops/docker/lessons/01_basic/00_what-is-docker.md` (KHÔNG dùng `00_intermediate-overview.md` làm mẫu — file đó còn lỗi).*

---

## 🔁 Quy trình review 1 bài (theo thứ tự)

1. **Đọc nguyên bài** bằng lăng kính người mới khó tính: chỗ nào vập, nhảy cóc, thuật ngữ chưa giải thích?
2. Soát theo **10 nhóm A–J** bên dưới (đánh dấu từng mục).
3. **Chạy verify tự động** (mục K) — code, link, fence, bullet, residue/meta.
4. **Cross-file**: số liệu/tên/marker/link-text có khớp các bài khác không.
5. Sửa tại chỗ → **bump version + 1 dòng changelog** (tăng dần).
6. Ghi lại **lỗi loại mới phát hiện** vào cuối file này (mục "Nhật ký lỗi mới") để bổ sung checklist + góp ý blueprint.

---

## 🅰️ Văn phong (style)

- [ ] Mở bài/section bằng **tình huống thật** hoặc câu hỏi gợi suy nghĩ — KHÔNG định nghĩa khô, KHÔNG liệt kê khô.
- [ ] **Lời dẫn 2–3 câu trước** mỗi code block / bảng / list lớn (vì sao có, làm gì, expect gì); **1–2 câu phân tích sau** (kết quả nói gì, dẫn sang ý kế).
- [ ] **Ẩn dụ đời thường** ở khái niệm khó — mỗi ẩn dụ dùng 1 lần, không lạm dụng; concept đã có ẩn dụ tốt thì giữ.
- [ ] **Câu bắc cầu** giữa các section (không nhảy ngang).
- [ ] Việt hoá đoạn **"điện tín"** (chuỗi thuật ngữ EN liên tiếp) → câu tiếng Việt mượt; thuật ngữ EN **giải thích trong ngoặc lần đầu**.
- [ ] Xưng hô: người đọc = "bạn", tác giả = "mình"/"Mr.Rom". KHÔNG chèn "Mr.Rom" vào thân bài/code/output/tiêu đề.
- [ ] KHÔNG độn chữ, KHÔNG sáo rỗng ("như đã biết", "hy vọng hữu ích").

## 🅱️ Header / Metadata

- [ ] Dùng **block-quote** (KHÔNG YAML frontmatter `---` cho lessons): Tác giả, Phiên bản, Tạo lúc, Cập nhật, Level, Tags, Yêu cầu trước. **KHÔNG dùng field "Thời lượng đọc"** (đã bỏ toàn kho 01/06 — ước tính không chuẩn, chỉ thêm lỗi).
- [ ] H1 = emoji + tiêu đề mô tả; **KHÔNG đóng khung con số cứng** ("8 lệnh") — gom theo logic/vòng đời.
- [ ] Ngày `DD/MM/YYYY`; Phiên bản SemVer; line-break dùng `\` (2-space cũng được nếu cả file đồng nhất).

## 🅲 Cấu trúc & Heading chuẩn

- [ ] Khung lessons bám 8 phần: Metadata · Câu dẫn+Mục tiêu · Nội dung (WHY→WHAT→HOW) · Pitfall · Self-check · Cheatsheet · Glossary · Liên kết (phần OPTIONAL bỏ khi không cần).
- [ ] Heading chuẩn, đồng nhất toàn cụm (**Việt hoá + EN trong ngoặc** — chốt 01/06):
  - `## 📚 Từ Điển Thuật Ngữ (Glossary)` (header bảng: `| EN | VN | Giải thích |` hoặc `| Thuật ngữ | Tiếng Việt | Giải thích |`)
  - `## 🧠 Tự kiểm tra (Self-check)` · `## ⚡ Tra cứu nhanh (Cheatsheet)` · `## 💡 Cạm bẫy thường gặp & Best practice` (`### ❌ Cạm bẫy:` / `### ✅ Best practice:`)
  - `## 📌 Nhật ký thay đổi (Changelog)` · "Step N" → "Bước N"
  - `## 🔗 Liên kết & Tài nguyên` + 3 sub: `### 🧭 Định hướng lộ trình học` · `### 🧩 Các chủ đề có thể bạn quan tâm` · `### 🌐 Tài nguyên tham khảo khác`
- [ ] Heading KHÔNG có dấu `:` cuối; có **dòng trống** trước/sau heading, list, fence.

## 🅳 Changelog

- [ ] Thứ tự **TĂNG DẦN** (cũ → mới, v1.0.0 trên cùng).
- [ ] Mỗi lần sửa → bump SemVer + 1 dòng mô tả **theo nội dung**, trung tính (KHÔNG "Premium/chuẩn 5 sao/Apply Blueprint §/Narrative Master").
- [ ] Mọi bài đều **có** changelog.

## 🅴 Markdown / Bullet

- [ ] Bullet `-` (dash, 1 space) — KHÔNG `*`.
- [ ] Code fence cân bằng (số ``` chẵn), có ngôn ngữ (` ```bash`/`python`/`yaml`...).
- [ ] Bảng: số cột header = separator = data; không lệch.
- [ ] KHÔNG tag rác lọt vào (`<parameter…>`, HTML thừa); KHÔNG smart-quote `“ ”`; KHÔNG trailing space.
- [ ] Bullet thiếu space sau `-` (`-design-patterns`); fence/heading thiếu dòng trống → fix.

## 🅵 Code chạy được

- [ ] Python: `python3 -m py_compile` / `-c`; Bash: `bash -n`; YAML: `yaml.safe_load`; Dockerfile/compose: lệnh thật hợp lệ.
- [ ] Output mẫu **khớp lệnh**; có giải thích dòng trạng thái quan trọng. KHÔNG bỏ bước, KHÔNG `...`.
- [ ] Lệnh/flag/version **hiện hành**, không deprecated. Ví dụ đã gặp: `npm ci --omit=dev` (≠ `--only=production`), cosign `attest` (≠ `attach sbom`), trivy `--scanners` (≠ `--security-checks`), `brew --cask docker-desktop`.
- [ ] Placeholder data đúng quy ước (`Nguyen Van A`...), KHÔNG để residue `"bạn"` trong code/JSON/SQL.

## 🅶 Link

- [ ] Mọi link nội bộ **resolve** (`ls` xác nhận). KHÔNG link rỗng `[text]()`.
- [ ] KHÔNG nhãn `(sắp viết)/(chưa có)` cho bài **đã tồn tại**.
- [ ] KHÔNG link `_blueprint/`, `01_sitemap-detail.md`, `templates/` trong file học (thuộc CONTRIBUTING).
- [ ] **Link text/description khớp tiêu đề thực** của bài đích.

## 🅷 "Sao nhãng" (de-meta) — vùng cấm trong file học

- [ ] KHÔNG nhắc: "viết bằng tiếng Việt / cho người Việt / 4 nhóm đối tượng / Narrative-driven / triết lý / 5 nguyên tắc sinh mệnh / 4 tầng đọc".
- [ ] KHÔNG tham chiếu nội bộ: `__Ref__`, "sprint complete", "Apply Blueprint §X", "Dogfood".

## 🅸 Nội dung / Factual

- [ ] Số liệu/version/hành vi kỹ thuật **đúng** và **nhất quán cross-file** (vd dung lượng image phải giống nhau ở mọi bài tham chiếu).
- [ ] Level đúng: `01_basic` KHÔNG nhồi nội dung advanced (security hardening sâu, internals, HA…).
- [ ] Không khung cứng số lượng; gom theo logic (vòng đời, nhóm chức năng).
- [ ] Thuật ngữ dùng **trước khi** giải thích → bổ sung giải thích/đưa lên Glossary.
- [ ] Mục tiêu (checklist đầu bài) **khớp** nội dung thực dạy trong bài.

## 🅹 Cross-file consistency (toàn cụm)

- [ ] Heading Glossary/Changelog/Liên kết đồng nhất mọi bài.
- [ ] Marker trạng thái (✅/🚧) trong README/catalog khớp file thực.
- [ ] Link "Bài trước/Bài tiếp" + description khớp H1 bài đích.
- [ ] Số liệu/ẩn dụ/placeholder dùng nhất quán giữa các bài liên quan.

---

## 🅺 Lệnh verify tự động (chạy từ gốc kho)

```bash
# Link gãy (bỏ false-positive trong code: =~, **kwargs, 'es'...)
python3 _workspace/check-broken-links.py 2>&1 | grep -A3 '📂 File: <path>'

# Bullet asterisk còn sót + fence lệch (script trong _workspace khi cần)
# Residue / meta
grep -rnE 'Mr\.Rom' <path> | grep -viE 'Tác giả|changelog'
grep -rnE '__Ref__|Apply Blueprint|sắp viết|Narrative' <path>
grep -rnE '"bạn"|=bạn|: bạn' <path>          # residue trong code/data

# Code: trích từng block ra chạy py_compile / bash -n / yaml.safe_load
# Cross-file số liệu: grep con số ở nhiều file rồi đối chiếu
```

---

## 📓 Nhật ký lỗi mới phát hiện (bổ sung dần → góp ý blueprint)

> Mỗi khi review gặp **loại lỗi chưa có trong checklist**, ghi vào đây để (a) thêm vào checklist, (b) cân nhắc đưa vào `_blueprint/`.

- (01/06/2026) Tuyên bố dung lượng/số liệu lệch giữa bài chính và bài tham chiếu chéo (vd 30 MB vs 85 MB) → thêm mục J "cross-file số liệu".
- (01/06/2026) Tag rác `<parameter…>` (artifact của lần sửa trước) lọt vào nội dung → thêm vào mục E.
- (01/06/2026) Khung cứng con số ("8 lệnh") gây bất nhất giữa tiêu đề/bảng/hands-on/sơ đồ → mục I.
- (01/06/2026) **Flag/lệnh deprecated** theo version mới: `npm ci --only=production`/`--production` → `--omit=dev`; `cosign attach sbom` → `cosign attest`; `trivy --security-checks` → `--scanners`; `brew --cask docker` → `docker-desktop`; `docker system prune -a` chú thích sai (xoá MỌI unused, không chỉ dangling) → bổ sung mục F: luôn đối chiếu lệnh/flag với bản hiện hành.
- (01/06/2026) **Field metadata lẫn EN**: `**Prerequisites:**` thay vì `**Yêu cầu trước:**` → mục B: tên field phải tiếng Việt, đồng nhất toàn cụm.
- (01/06/2026) **Nav không nhất quán cross-file**: cụm dùng marker riêng (`↶/→/↑` + link text = tên file) khác gold standard basic (`⬅️/➡️` + tiêu đề thật) → mục J: nav phải đồng bộ kiểu + link text = tiêu đề thực.
- (01/06/2026) **Fence thiếu ngôn ngữ** (MD040) cho block output/log → mục E: mọi fence có ngôn ngữ (`text` cho output).
- (01/06/2026) **Reading-time lệch** giữa README và header bài (12p vs 18p) → **ĐÃ XỬ LÝ TRIỆT ĐỂ**: bỏ hẳn field "Thời lượng đọc" khỏi metadata toàn kho + bảng README/overview + blueprint spec/template (theo chỉ đạo chủ kho: ước tính không chuẩn → loại bỏ).
- (01/06/2026) **Heading/Glossary-header lẫn EN trong cụm** ("Pitfall & Best practice", "Term | Vietnamese / Explanation", "Step 1..5", "Base image showdown") — nhất quán nội cụm nhưng khác gold standard → **CẦN QUYẾT Ở BLUEPRINT** (Việt hoá đồng loạt hay chấp nhận EN cho heading kỹ thuật?).
- _(thêm khi gặp...)_

---

## 📌 Changelog

- **v1.0.0 (01/06/2026)** — Bản đầu: đúc kết checklist 10 nhóm A–J + verify K từ đợt làm cụm Docker.
