# 📊 Master Catalog

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.1.0\
> **Tạo lúc:** DD/MM/YYYY\
> **Cập nhật:** 01/06/2026

> 🎯 *Tracking trạng thái mọi bài trong kho. Cập nhật khi tạo bài mới, đổi trạng thái, hoặc đổi tag.*

---

## 🔑 Ký hiệu

### Trạng thái

| Ký hiệu | Ý nghĩa |
|---|---|
| ✅ | **Done** — đã viết hoàn chỉnh, qua quality checklist |
| 🚧 | **WIP** — đang viết |
| ❌ | **Chưa có** — folder rỗng / placeholder |
| 🔄 | **Cần cập nhật** — outdated hoặc cần refactor |

### Tag bổ sung

| Ký hiệu | Ý nghĩa |
|---|---|
| 🌟 | **MUST-KNOW** — bài bắt buộc trong roadmap tương ứng |
| 🆕 | **New** — vừa thêm (< 7 ngày) |
| 🔥 | **Hot** — bài đang được sửa nhiều |

---

## 📊 Thống kê tổng

| Chỉ số | Giá trị |
|---|---|
| Tổng số bài | <X> |
| ✅ Done | <Y> (<Y/X%>) |
| 🚧 WIP | <Z> |
| ❌ Chưa có | <W> |
| 🌟 MUST-KNOW | <V> |

---

## 📚 Theo L1

### 00_roadmaps

#### career/
- ✅ `zero-to-coder_career-roadmap.md`
- 🚧 `backend-developer_career-roadmap.md`
- ❌ `frontend-developer_career-roadmap.md`

#### lab-series/
- ✅ `docker-to-k8s_lab-series.md`
- ❌ `full-stack-web-app_lab-series.md`

---

### 01_foundations

#### dsa/
- ✅ 🌟 `lessons/01_basic/00_big-o.md`
- 🚧 🌟 `lessons/01_basic/01_array.md`
- ❌ `lessons/01_basic/02_linked-list.md`
- ❌ `lessons/01_basic/03_stack.md`
- ❌ `lessons/01_basic/04_queue.md`

#### computer-architecture/
- ❌ `lessons/01_basic/00_cpu.md`
- ❌ `lessons/01_basic/01_memory.md`

#### (các L2 khác — bổ sung khi viết)

---

### 02_tools

#### git/
- ✅ 🌟 `lessons/01_basic/00_setup.md`
- ✅ 🌟 `lessons/01_basic/01_basic-commands.md`
- 🚧 `lessons/02_intermediate/00_branching.md`

#### shell/
- ❌ (chưa có content)

---

### 03_languages

#### python/
- ✅ 🌟 `lessons/01_basic/00_syntax.md`
- ✅ `lessons/01_basic/01_data-types.md`
- ✅ `lessons/01_basic/02_control-flow.md`

#### go/
- ❌ (chưa có content)

---

### 04_os

#### linux/
- ✅ 🌟 `lessons/01_basic/00_filesystem.md`
- 🚧 🌟 `lessons/01_basic/01_navigation.md`
- ❌ (~25 bài lý thuyết khác)

---

### 05_networking

(bổ sung khi có content)

---

### 06_databases

(bổ sung khi có content)

---

### 07_web

(bổ sung khi có content)

---

### 08_mobile

(bổ sung khi có content)

---

### 09_architecture

(bổ sung khi có content)

---

### 10_devops

#### docker/
- ✅ 🌟 `lessons/01_basic/00_what-is-docker.md`
- 🚧 `lessons/01_basic/01_image-and-container.md`
- ❌ `lessons/02_intermediate/00_compose.md`

#### kubernetes/
- ✅ 🌟 `lessons/01_basic/00_architecture.md`
- ✅ 🌟 `lessons/01_basic/01_pod.md`
- 🚧 `lessons/01_basic/02_replicaset.md`

#### ci-cd/
- ❌ (chưa có content)

---

### 11_cloud, 12_security, 13_ai-ml, 14_data-engineering, 15_specialized, 16_career-soft-skills

(bổ sung tương tự khi có content)

---

## 🔄 Bài cần cập nhật

| File | Lý do |
|---|---|
| `<path>` | <Lý do — vd: API version mới> |

---

## 🌟 Danh sách MUST-KNOW (toàn kho)

Bài MUST-KNOW xếp theo L1 để dễ xem cho từng roadmap:

- 🌟 ✅ `01_foundations/dsa/lessons/01_basic/00_big-o.md`
- 🌟 🚧 `01_foundations/dsa/lessons/01_basic/01_array.md`
- 🌟 ✅ `01_foundations/version-control/git/lessons/01_basic/00_setup.md`
- 🌟 ✅ `01_foundations/version-control/git/lessons/01_basic/01_basic-commands.md`
- 🌟 ✅ `03_languages/python/lessons/01_basic/00_syntax.md`
- 🌟 ✅ `04_os/linux/lessons/01_basic/00_filesystem.md`
- 🌟 🚧 `04_os/linux/lessons/01_basic/01_navigation.md`
- 🌟 ✅ `10_devops/docker/lessons/01_basic/00_what-is-docker.md`
- 🌟 ✅ `10_devops/kubernetes/lessons/01_basic/00_architecture.md`
- 🌟 ✅ `10_devops/kubernetes/lessons/01_basic/01_pod.md`

---

## 🛠️ Tự động hoá (OPT)

Khi kho lớn, có thể setup script tự gen catalog:

```bash
# _scripts/gen-catalog.sh
# Quét mọi *.md trong các L1, đọc metadata, output MASTER-CATALOG.md
```

Tích hợp pre-commit hook hoặc CI job để giữ catalog luôn fresh.

---

## 📌 Nhật ký thay đổi (Changelog)

- **v1.0.0 (DD/MM/YYYY)** — Bản đầu tiên.
- **v1.1.0 (01/06/2026)** — Dùng heading changelog chuẩn + tăng dần. Lý do: đồng bộ với 3 quyết định governance đã duyệt.
