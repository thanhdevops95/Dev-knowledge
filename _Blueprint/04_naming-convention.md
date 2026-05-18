# 🏷️ Naming Convention — Quy ước đặt tên trong kho

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.1.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 15/05/2026

> 🎯 *File này định nghĩa quy tắc đặt tên cho mọi thứ trong kho: folder, file, anchor, code block label, image path. Kế thừa từ skills toàn cục (`naming/files.md`, `naming/folders.md`, `naming/numbering.md`) và bổ sung phần riêng cho kho tri thức CNTT.*

---

## 0️⃣ Nguyên tắc chung

| Nguyên tắc | Mô tả |
|---|---|
| **English-first cho định danh** | Tên folder/file dùng EN. Nội dung file dùng VN. |
| **Lowercase mặc định** | Trừ folder L1 và proper nouns |
| **Hyphen `-` giữa từ trong 1 segment** | `multi-tier-app` không phải `multi_tier_app` |
| **Underscore `_` giữa các segment** | `NN_<name>_<type>.<ext>` |
| **Không khoảng trắng** | `pod-lifecycle.md` không phải `pod lifecycle.md` |
| **Không dấu tiếng Việt** | `gioi-thieu` không phải `giới-thiệu` |
| **Không emoji trong tên file/folder** | Emoji chỉ trong nội dung |

---

## 1️⃣ Tên folder

### 1.1 Folder L1 (chủ đề lớn)

Format: `NN_<Name>` — đánh số 2 chữ số + sentence case.

| ✅ Đúng | ❌ Sai | Lý do |
|---|---|---|
| `10_DevOps/` | `10-DevOps/` | Sai separator (`-` thay `_`) |
| `10_DevOps/` | `10_devops/` | L1 dùng sentence case |
| `16_Career-Soft-skills/` | `16_career_soft_skills/` | Multi-word dùng `-` trong name |
| `00_Roadmaps/` | `0_Roadmaps/` | Phải 2 chữ số |

**Proper noun giữ nguyên**: `K8s-training/`, `MacOS/`, `iOS/`, `AWS-Architect/`.

### 1.2 Folder L2 (chủ đề con)

Format: `<name>` — lowercase, không số thứ tự, multi-word dùng `-`.

| ✅ Đúng | ❌ Sai |
|---|---|
| `kubernetes/` | `Kubernetes/` |
| `data-engineering/` | `data_engineering/` |
| `react-native/` | `React-Native/` |

> Lý do không đánh số L2: thứ tự học các L2 *không cố định*. User có thể học K8s trước Docker (hoặc ngược lại) — phụ thuộc roadmap đang chọn.

### 1.3 Folder L3 (loại nội dung)

Tên cố định theo menu 7 loại + extension (xem `02_folder-structure.md`):

- `lessons/`, `setup/`, `exercises/`, `projects/`, `recipes/`
- `references/`, `interview-questions/`, `case-studies/`, `migration-guides/`, `tools-comparison/` (mở rộng)

Tên này **không đổi** — giữ nhất quán toàn kho để dễ navigate.

### 1.4 Folder L4 (level trong lessons hoặc subfolder)

Trong `lessons/`: bắt buộc 3 level đánh số:
- `01_basic/`, `02_intermediate/`, `03_advanced/`

Trong các L3 khác (vd subfolder `recipes/`):
- `troubleshooting/`, `patterns/`, `operations/` — lowercase, không số

### 1.5 Folder meta (L1-level)

Prefix `_` để phân biệt với L2:

- `_notes/`
- `_concepts/`
- `_capstone-projects/`
- `_assets/` (cho ảnh/diagram)

### 1.6 Folder Blueprint / build / archive

Theo convention toàn cục:

- `_Blueprint/` — thiết kế repo (đang đọc)
- `_archive/` — nội dung cũ giữ tham khảo
- `_scripts/` — tooling

---

## 2️⃣ Tên file

### 2.1 File trong `lessons/<level>/`

Format: `NN_<topic-name>.md`

| ✅ Đúng | ❌ Sai |
|---|---|
| `00_overview.md` | `0_overview.md` (thiếu số 0) |
| `01_pod.md` | `01-pod.md` (sai separator) |
| `08_imperative-vs-declarative.md` | `08_imperative_vs_declarative.md` (sai separator trong name) |

### 2.2 File trong `setup/`, `recipes/`

Không đánh số (mỗi file độc lập). Tên = function/problem (kebab-case):

| ✅ Đúng |
|---|
| `minikube.md` |
| `pod-crashloopbackoff.md` |
| `backup-and-restore.md` |

### 2.3 File trong `exercises/`

Đánh số theo độ khó: `NN_<verb-phrase>.md`

| ✅ Đúng |
|---|
| `01_create-first-pod.md` |
| `02_scale-deployment.md` |
| `05_grep-awk-log-analysis.md` |

### 2.4 File trong `projects/<NN>_<project>/`

| Vị trí | Format |
|---|---|
| README chính của project | `README.md` |
| Step files | `NN_<step-name>.md` (vd `01_setup.md`, `02_deploy-frontend.md`) |

### 2.5 File README, overview, cheatsheet, glossary

Tên cố định (không tùy biến):

| File | Vị trí |
|---|---|
| `README.md` | Mọi folder cần index |
| `00_overview.md` | L1, L2, một số L3 (lessons, setup, projects) |
| `99_cheatsheet.md` | Cuối L2 (nếu áp dụng) |
| `_glossary.md` | Cuối L1 và/hoặc L2 |

### 2.6 File metadata / config

| File | Mục đích |
|---|---|
| `_meta.yml` (OPT) | Metadata bổ sung cho folder (nếu cần tooling đọc) |
| `_redirects.md` (OPT) | Mapping URL cũ → mới khi rename |

---

## 3️⃣ Tên anchor (heading trong file)

Heading sinh anchor tự động trong markdown. Quy tắc viết heading để anchor đẹp:

### 3.1 Heading H2/H3

- Bắt đầu bằng emoji + space
- Sentence case (chỉ chữ cái đầu hoa)
- Anchor sinh ra sẽ lowercase + thay space bằng `-` + bỏ emoji

Ví dụ:

```markdown
## 🎯 Sau bài này bạn sẽ làm được gì
```

→ Anchor: `#sau-bài-này-bạn-sẽ-làm-được-gì`

> ⚠️ **Lưu ý**: anchor tiếng Việt **CÓ DẤU** vẫn hợp lệ trong GitHub render, nhưng có engine không hỗ trợ. Khi link tới heading tiếng Việt → test nếu cần.

### 3.2 Heading có ký tự đặc biệt

Tránh: `&`, `(`, `)`, `/`, `:`. Nếu có, anchor sẽ bỏ.

❌ "Pod (chi tiết) & lifecycle" → anchor rối\
✅ "Pod — chi tiết và lifecycle" → anchor sạch hơn

---

## 4️⃣ Tên trong code (variable, function, file path)

| Loại | Convention |
|---|---|
| Variable / function name | Theo ngôn ngữ (Python: `snake_case`, JS: `camelCase`, Go: `mixedCase`) — không Việt hóa |
| File path trong code | Tuyệt đối / tương đối — không Việt hóa |
| String literal cho UI/user | Có thể tiếng Việt (vì hiển thị cho người dùng) |

Ví dụ:

```python
# Đúng
visit_count = redis.incr('visit_count')
greeting = "Xin chào bạn!"   # ← string user-facing tiếng Việt OK

# Sai
soluot_truycap = redis.incr('soluot_truycap')   # ← biến tiếng Việt
```

---

## 5️⃣ Tên image / asset

### 5.1 Quy tắc đặt tên

Format: `<topic>-<aspect>_<format>.<ext>`

| ✅ Đúng | ❌ Sai |
|---|---|
| `pod-lifecycle_diagram.png` | `pod lifecycle diagram.png` (có space) |
| `k8s-architecture_full.svg` | `K8sArchitectureFull.svg` (PascalCase) |
| `kubectl-cheatsheet_v2.png` | `cheatsheet.png` (không rõ topic) |

### 5.2 Vị trí lưu

| Phạm vi dùng | Lưu ở |
|---|---|
| Dùng riêng cho 1 bài | `<folder của bài>/_assets/` |
| Dùng chung trong 1 L2 | `<L2>/_assets/` |
| Dùng chung trong 1 L1 | `<L1>/_assets/` |
| Dùng chung toàn kho | `_assets/` ở gốc |

### 5.3 Tham chiếu trong markdown

```markdown
![Mô tả ngắn](./_assets/pod-lifecycle_diagram.png)
```

→ **Alt text bắt buộc** (không để rỗng `[]`).

---

## 6️⃣ Tên trong YAML frontmatter (nếu dùng)

Một số file (đặc biệt trong `_Blueprint/`) có frontmatter:

```yaml
---
name: blueprint-overview
description: <one-liner>
metadata:
  layer: L1-core
---
```

| Field | Convention |
|---|---|
| `name` | kebab-case, unique trong toàn kho |
| `description` | Tiếng Anh hoặc Việt, 1 dòng, mô tả mục đích |
| `layer` | Enum: `L1-core`, `L2-mode`, `L3-skill`, `L4-template` |

---

## 7️⃣ Tên link / URL

### 7.1 Internal link

Dùng relative path từ file hiện tại:

```markdown
[Pod](../01_pod.md)               ← lên 1 cấp
[Deployment](./03_deployment.md)  ← cùng cấp
[Cheatsheet](../../99_cheatsheet.md)  ← lên 2 cấp
```

### 7.2 Anchor link

```markdown
[Section "Pitfall"](#-pitfall-thường-gặp--best-practice)
```

→ Test render thử nếu anchor có dấu tiếng Việt.

### 7.3 External URL

```markdown
[Official K8s docs](https://kubernetes.io/docs/)
```

→ Link text phải mô tả đích, không dùng "click here", "ở đây".

---

## 8️⃣ Tên trong table of contents (TOC)

Nếu file dài > 500 dòng → có TOC ở đầu:

```markdown
## 📋 Mục lục

1. [Pod là gì](#1️⃣-pod-là-gì)
2. [Diagram cấu trúc](#2️⃣-diagram-cấu-trúc)
3. [Hands-on](#3️⃣-hands-on)
4. [Pitfall](#4️⃣-pitfall)
```

→ Mỗi heading H2 ở dạng `<số>️⃣ <tên>` để vừa có numbering vừa có emoji.

---

## 9️⃣ Tên branch / commit (khi dùng Git)

| Loại | Format | Ví dụ |
|---|---|---|
| Feature branch | `feature/<L1>-<L2>-<topic>` | `feature/devops-k8s-pod-lesson` |
| Fix branch | `fix/<area>-<short-desc>` | `fix/k8s-pod-typo` |
| Commit message | `<type>: <description>` | `feat: add Pod lesson basic`, `fix: typo in deployment.md` |

Commit `type`: `feat`, `fix`, `docs`, `refactor`, `chore`.

---

## 🔟 Tên không được dùng (forbidden)

| ❌ Không dùng | Vì sao |
|---|---|
| `final_v2_FINAL_ok.md` | Lộn xộn — dùng version SemVer trong metadata |
| `untitled.md`, `new-file.md` | Không mô tả nội dung |
| `Doc1.md`, `Doc2.md` | Không có ý nghĩa |
| `temp.md`, `test.md` | Để trong `_archive/` hoặc xóa |
| `MyDocument.md` | PascalCase không hợp file |
| `tài-liệu.md` | Tiếng Việt có dấu |
| `Tài liệu.md` | Tiếng Việt + space |
| `2024-01-15-meeting.md` | Date prefix → chỉ dùng cho `_notes/` nếu cần |

---

## 1️⃣1️⃣ Tóm tắt prefix-by-cấp

| Cấp | Folder pattern | File pattern | Ví dụ |
|---|---|---|---|
| Root | `NN_<Name>/`, `_<Name>/` | `README.md` | `10_DevOps/`, `_Blueprint/` |
| L1 | `_<name>/` (meta), `<name>/` (L2) | `README.md`, `00_overview.md`, `_glossary.md` | `_notes/`, `docker/` |
| L2 | `<name>/` (L3 types) | `README.md`, `00_overview.md`, `99_cheatsheet.md`, `_glossary.md` | `lessons/`, `setup/` |
| L3 lessons | `NN_<level>/` | — | `01_basic/` |
| L3 setup | — | `<tool>.md` | `minikube.md` |
| L3 exercises | — | `NN_<verb-phrase>.md` | `01_create-pod.md` |
| L3 projects | `NN_<project>/` | `README.md`, `NN_<step>.md` | `01_first-pod/`, `01_setup.md` |
| L3 recipes | `<category>/` | `<problem-name>.md` | `troubleshooting/pod-crashloopbackoff.md` |
| L4 lessons | — | `NN_<topic>.md` | `01_pod.md` |

---

## 1️⃣2️⃣ Quy trình rename — khi cần đổi tên

Khi đổi tên 1 file/folder đã có content:

1. ✏️ **Rename** file/folder
2. 🔍 **Grep** mọi link trỏ tới tên cũ: `grep -rn "<old-name>" .`
3. 🔧 **Fix link** trong các file phụ thuộc
4. 📝 **Note** trong `_redirects.md` (nếu rename đáng kể): `<old> → <new> (lý do, ngày)`
5. 📌 **Bump version** của file đã rename

> ⚠️ Avoid rename quá thường xuyên — tốn công và dễ vỡ link.

---

## 📌 Changelog

- **v0.1.0 (15/05/2026)** — Bản đầu tiên. Quy ước đặt tên folder/file ở từng cấp (root → L1 → L2 → L3 → L4). Prefix `NN_`, `_`, `00_`, `99_` và khi nào dùng. Anchor, image path, link, branch/commit. Danh sách forbidden names. Quy trình rename.
