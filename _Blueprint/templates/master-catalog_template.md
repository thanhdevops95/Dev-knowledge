# 📊 Master Catalog

> **Tác giả:** Mr.Rom\
> **Phiên bản:** v1.0.0\
> **Tạo lúc:** DD/MM/YYYY\
> **Cập nhật:** DD/MM/YYYY

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

### 00_Roadmaps

#### career/
- ✅ `zero-to-coder_career-roadmap.md`
- 🚧 `backend-developer_career-roadmap.md`
- ❌ `frontend-developer_career-roadmap.md`

#### lab-series/
- ✅ `docker-to-k8s_lab-series.md`
- ❌ `full-stack-web-app_lab-series.md`

---

### 01_Foundations

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

### 02_Tools

#### git/
- ✅ 🌟 `lessons/01_basic/00_setup.md`
- ✅ 🌟 `lessons/01_basic/01_basic-commands.md`
- 🚧 `lessons/02_intermediate/00_branching.md`

#### shell/
- ❌ (chưa có content)

---

### 03_Languages

#### python/
- ✅ 🌟 `lessons/01_basic/00_syntax.md`
- ✅ `lessons/01_basic/01_data-types.md`
- ✅ `lessons/01_basic/02_control-flow.md`

#### go/
- ❌ (chưa có content)

---

### 04_OS

#### linux/
- ✅ 🌟 `lessons/01_basic/00_filesystem.md`
- 🚧 🌟 `lessons/01_basic/01_navigation.md`
- ❌ (~25 bài lý thuyết khác)

---

### 05_Networking

(bổ sung khi có content)

---

### 06_Databases

(bổ sung khi có content)

---

### 07_Web

(bổ sung khi có content)

---

### 08_Mobile

(bổ sung khi có content)

---

### 09_Architecture

(bổ sung khi có content)

---

### 10_DevOps

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

### 11_Cloud, 12_Security, 13_AI-ML, 14_Data-Engineering, 15_Specialized, 16_Career-Soft-skills

(bổ sung tương tự khi có content)

---

## 🔄 Bài cần cập nhật

| File | Lý do |
|---|---|
| `<path>` | <Lý do — vd: API version mới> |

---

## 🌟 Danh sách MUST-KNOW (toàn kho)

Bài MUST-KNOW xếp theo L1 để dễ xem cho từng roadmap:

- 🌟 ✅ `01_Foundations/dsa/lessons/01_basic/00_big-o.md`
- 🌟 🚧 `01_Foundations/dsa/lessons/01_basic/01_array.md`
- 🌟 ✅ `01_Foundations/version-control/git/lessons/01_basic/00_setup.md`
- 🌟 ✅ `01_Foundations/version-control/git/lessons/01_basic/01_basic-commands.md`
- 🌟 ✅ `03_Languages/python/lessons/01_basic/00_syntax.md`
- 🌟 ✅ `04_OS/linux/lessons/01_basic/00_filesystem.md`
- 🌟 🚧 `04_OS/linux/lessons/01_basic/01_navigation.md`
- 🌟 ✅ `10_DevOps/docker/lessons/01_basic/00_what-is-docker.md`
- 🌟 ✅ `10_DevOps/kubernetes/lessons/01_basic/00_architecture.md`
- 🌟 ✅ `10_DevOps/kubernetes/lessons/01_basic/01_pod.md`

---

## 🛠️ Tự động hoá (OPT)

Khi kho lớn, có thể setup script tự gen catalog:

```bash
# _scripts/gen-catalog.sh
# Quét mọi *.md trong các L1, đọc metadata, output MASTER-CATALOG.md
```

Tích hợp pre-commit hook hoặc CI job để giữ catalog luôn fresh.

---

## 📌 Changelog

- **v1.0.0 (DD/MM/YYYY)** — Bản đầu tiên.
