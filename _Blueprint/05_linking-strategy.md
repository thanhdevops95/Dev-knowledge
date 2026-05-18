# 🔗 Linking Strategy — Quy ước liên kết & glossary

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v0.1.0\
> **Tạo lúc:** 15/05/2026\
> **Cập nhật:** 15/05/2026

> 🎯 *File này định nghĩa cách tạo liên kết giữa các bài, anchor, glossary, và pattern xử lý cross-L2 reference. Mục tiêu: kho có **mạng lưới navigation 2 chiều** — đọc 1 bài có thể nhảy ngang/dọc nhanh chóng.*

---

## 1️⃣ Triết lý link trong kho

| Nguyên tắc | Diễn giải |
|---|---|
| **DRY** | Nội dung chỉ ở 1 nơi — các nơi khác link tới |
| **Navigation 2 chiều** | Mỗi bài có "Bài tiếp" và "Bài trước"; nhiều bài có cả "Bài liên quan" |
| **Local trước, external sau** | Ưu tiên link nội kho. External chỉ thêm khi cần đào sâu |
| **Description-rich link text** | Link text mô tả đích, không "click here" / "ở đây" |
| **Relative path** | Internal link dùng relative — di chuyển folder không vỡ |
| **Stable anchor** | Anchor đến heading ổn định — đừng đổi heading lặt vặt |

---

## 2️⃣ Loại link

### 2.1 Internal — link nội kho

**Format**: relative path từ file hiện tại.

```markdown
[Pod](../01_pod.md)                           ← cùng L4 lessons/01_basic/
[Deployment](./03_deployment.md)              ← cùng cấp
[K8s overview](../../00_overview.md)          ← lên 2 cấp
[Linux setup](../../../04_OS/linux/setup/)    ← cross-L1
```

**Quy tắc**:
- Bắt đầu bằng `./` hoặc `../` cho rõ
- Không dùng absolute path (`/04_Knowledge/...`)
- Trailing slash nếu link tới folder (`linux/`), bỏ slash nếu link tới file (`pod.md`)

### 2.2 Anchor — link trong cùng file

```markdown
[Section "Pitfall"](#-pitfall--best-practice)
```

**Quy tắc**:
- Anchor sinh tự động từ heading text
- Emoji + space ở đầu heading → bỏ trong anchor
- Tiếng Việt có dấu **GitHub render đúng** — vẫn dùng được

### 2.3 Anchor cross-file

```markdown
[Pod section "Networking"](../01_pod.md#networking)
```

→ Path file + `#` + anchor.

### 2.4 External — link ngoài

```markdown
[Official K8s docs — Pod](https://kubernetes.io/docs/concepts/workloads/pods/)
```

**Quy tắc**:
- Link text phải mô tả đích (không "ở đây", "click here")
- Có thể thêm note ngắn sau dấu `—`: `[K8s docs — Pod spec](url) — chi tiết YAML schema`
- Markdown thường tự mở tab mới cho external link

### 2.5 Wiki-link `[[...]]` (cho metadata frontmatter và _Blueprint)

Trong **Blueprint files** và **metadata frontmatter** dùng `[[name]]` để link mềm:

```markdown
xem [[blueprint-overview]] để hiểu vai trò
```

Trong **content files** (bài học) → KHÔNG dùng `[[...]]`, dùng markdown link thường để compatibility.

---

## 3️⃣ Pattern cross-L2 reference

Khi 1 bài cần content từ L2 khác (vd: K8s project cần image từ Docker project), dùng **pattern 3 bước**:

```markdown
> ⚠️ **Prerequisite — Lấy source từ Docker:**
>
> Project này cần image `myapp:6.0` đã build ở Docker. Có 3 cách:
>
> 1. **Đi qua từ Docker series**: hoàn thành [`../../docker/projects/03_compose-multi-tier/`](../../docker/projects/03_compose-multi-tier/) Bài 24, đã có image
> 2. **Clone repo mẫu**: `git clone https://github.com/your-username/myapp-source`
> 3. **Build app mới**: làm theo [`../../docker/lessons/01_basic/`](../../docker/lessons/01_basic/) trong ~30 phút
>
> Sau khi có image, quay lại file này tiếp tục.
```

**Format**:
- Dùng `> ⚠️` block để nổi bật
- Liệt kê 2-3 cách lấy source (đi từ stage trước / clone / tự build)
- Link tới L2 khác bằng relative path đầy đủ
- Câu kết: "quay lại tiếp tục"

---

## 4️⃣ Navigation block cuối bài

Mỗi bài lessons (và project step) nên có **navigation footer**:

```markdown
---

## 🔗 Liên kết & Tài nguyên

### Bài liên quan trong kho

| Hướng | Bài |
|---|---|
| ⬅️ Bài trước | [Container và Image](./00_architecture.md) |
| ➡️ Bài tiếp | [ReplicaSet](./02_replicaset.md) |
| 🔗 Liên quan | [Deployment](./03_deployment.md), [Service](./04_service.md) |
| ⬆️ Index L2 | [K8s overview](../../00_overview.md) |

### Tài nguyên ngoài

- [Official K8s docs — Pod](https://kubernetes.io/docs/concepts/workloads/pods/) — spec đầy đủ
- [Kubernetes the Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) — build cluster from scratch
```

→ Đảm bảo người đọc luôn biết "đi đâu tiếp", không bị dead-end.

---

## 5️⃣ Glossary — chiến lược 3 cấp

Có 3 cấp glossary, mỗi cấp phục vụ scope khác nhau:

### 5.1 Cấp 1: `_glossary.md` ở từng bài (OPT)

Trong bài học có nhiều thuật ngữ EN, thêm section ở cuối:

```markdown
## 📚 Glossary

| EN | VN | Giải thích |
|---|---|---|
| Pod | Pod | Đơn vị deploy nhỏ nhất K8s |
| Manifest | File khai báo | YAML/JSON mô tả desired state |
```

→ Glossary local cho bài đó. Người đọc tra ngay tại bài.

### 5.2 Cấp 2: `<L2>/_glossary.md` (cho L2)

Tổng hợp thuật ngữ của cả L2 (vd: `kubernetes/_glossary.md` gồm tất cả thuật ngữ K8s).

```markdown
# Glossary — Kubernetes

| EN | VN | Giải thích | Bài chính |
|---|---|---|---|
| Pod | Pod | Đơn vị deploy | [lessons/01_basic/01_pod.md](./lessons/01_basic/01_pod.md) |
| Node | Node | Máy worker | [lessons/01_basic/00_architecture.md](./lessons/01_basic/00_architecture.md) |
| ConfigMap | Config | Lưu cấu hình | [lessons/02_intermediate/00_configmap-and-secret.md](...) |
```

→ Cột "Bài chính" link ngược tới bài giảng thuật ngữ đó.

### 5.3 Cấp 3: `<L1>/_glossary.md` (cho L1)

Thuật ngữ chung của L1, áp dụng nhiều L2 (vd: `10_DevOps/_glossary.md` gồm DevOps, GitOps, IaC, ...).

```markdown
# Glossary — DevOps

| EN | VN | Giải thích | L2 chính |
|---|---|---|---|
| GitOps | GitOps | Quản lý infra qua Git | [_concepts/gitops.md](./_concepts/gitops.md) |
| IaC | Hạ tầng dạng code | Quản lý infra qua code | [iac/](./iac/) |
```

### 5.4 Quy ước viết entry glossary

| Cột | Quy tắc |
|---|---|
| **EN** | Tên gốc — không Việt hóa |
| **VN** | Bản dịch (nếu có) hoặc *"giữ nguyên"* nếu không có VN tương đương phổ biến |
| **Giải thích** | 1 câu ngắn, ≤25 từ |
| **Bài chính** (OPT) | Link tới bài giảng kỹ thuật ngữ đó |

---

## 6️⃣ Pattern link giữa các cấp

### 6.1 Lesson → Lesson cùng L2

Nên có sequential link rõ ràng:

```markdown
[⬅️ Pod](./01_pod.md) | [📋 Index](../README.md) | [➡️ Deployment](./03_deployment.md)
```

### 6.2 Lesson → Exercise tương ứng

Trong bài lessons, ở cuối phần Hands-on:

```markdown
> 🧪 **Luyện thêm**: làm bài tập [01 — Tạo Pod đầu tiên](../../exercises/01_create-first-pod.md)
```

### 6.3 Lesson → Recipe khi bài đề cập tình huống

```markdown
> 💡 Khi Pod bị `CrashLoopBackOff`, xem cách debug ở [recipes/troubleshooting/pod-crashloopbackoff.md](../../recipes/troubleshooting/pod-crashloopbackoff.md)
```

### 6.4 Project → Lesson cần làm trước

Project README có section Prerequisites:

```markdown
## 📋 Prerequisites

- [x] Đã làm [Pod basic](../../lessons/01_basic/01_pod.md)
- [x] Đã làm [Deployment basic](../../lessons/01_basic/03_deployment.md)
- [ ] Đã có cluster local (xem [setup/minikube.md](../../setup/minikube.md))
```

### 6.5 Roadmap → Lessons/Projects

Roadmap chỉ chứa link, không lặp nội dung:

```markdown
## Bước 3 — K8s basics (1 tuần)

📚 **Đọc tuần tự**:
- [ ] [Pod](../../10_DevOps/kubernetes/lessons/01_basic/01_pod.md)
- [ ] [Deployment](../../10_DevOps/kubernetes/lessons/01_basic/03_deployment.md)
- [ ] [Service](../../10_DevOps/kubernetes/lessons/01_basic/04_service.md)

🧪 **Hoàn thành project**:
- [ ] [01_first-pod](../../10_DevOps/kubernetes/projects/01_first-pod/)
```

---

## 7️⃣ Link checker — tự động phát hiện link vỡ

Khi rename file, link cũ vỡ. Để phát hiện sớm:

### 7.1 Script đơn giản (đặt ở `_scripts/check-links.sh`)

```bash
#!/usr/bin/env bash
# Tìm tất cả markdown link nội bộ
find . -name "*.md" -exec grep -Hn '\[.*\](\..*\.md)' {} \;
```

### 7.2 Tooling (OPT, nâng cao)

- `markdown-link-check` (npm package) — kiểm tra tự động
- `lychee` (Rust binary) — fast, kiểm tra cả internal + external

Tích hợp vào CI/pre-commit nếu kho mở public.

---

## 8️⃣ Anchor link — quy ước heading để anchor đẹp

### 8.1 Heading tiếng Việt — anchor giữ dấu

```markdown
## 🎯 Sau bài này bạn sẽ làm gì
```

→ Anchor: `#-sau-bài-này-bạn-sẽ-làm-gì`

GitHub render hỗ trợ. Khi link:

```markdown
[Sau bài học gì](./pod.md#-sau-bài-này-bạn-sẽ-làm-gì)
```

### 8.2 Heading có numbering ️⃣

```markdown
## 1️⃣ Pod là gì
```

→ Anchor: `#1️⃣-pod-là-gì`

→ Hoạt động trong GitHub. Khi link bên ngoài → test.

### 8.3 Heading thay đổi — cần update link

Khi sửa heading text, anchor đổi. Tìm và sửa:

```bash
grep -rn "#cũ-anchor" .
```

→ Best practice: heading nên ổn định, không thêm prefix linh tinh.

---

## 9️⃣ Link metadata (cho tooling AI / static-site)

Một số tooling đọc frontmatter để build index:

```yaml
---
title: Pod — Đơn vị deploy K8s
related:
  - ./00_architecture.md
  - ./03_deployment.md
prerequisites:
  - ../../docker/lessons/01_basic/01_image-and-container.md
glossary: ../../_glossary.md
---
```

→ OPTIONAL. Chỉ thêm khi có tooling sử dụng.

---

## 🔟 Tóm tắt — bảng quyết định link

| Tình huống | Loại link |
|---|---|
| Bài trước/sau trong cùng level | Sequential: `[⬅️] [📋] [➡️]` |
| Bài liên quan ngoài level | Block "Liên quan" trong navigation footer |
| Bài tiên quyết | Block "Prerequisites" ở đầu (project) hoặc trong câu dẫn (lesson) |
| Tài nguyên ngoài | Section "Tài nguyên ngoài" cuối |
| Cross-L2 source | Block ⚠️ Prerequisite với 2-3 cách lấy source |
| Thuật ngữ kỹ thuật | Glossary cấp 1 (bài) → cấp 2 (L2) → cấp 3 (L1) |
| Roadmap → bài cụ thể | Checklist với relative path |

---

## 📌 Changelog

- **v0.1.0 (15/05/2026)** — Bản đầu tiên. Spec 5 loại link (internal, anchor, anchor cross-file, external, wiki-link). Pattern cross-L2 reference. Navigation footer chuẩn. Glossary 3 cấp (bài → L2 → L1). Link checker. Anchor quy ước.
