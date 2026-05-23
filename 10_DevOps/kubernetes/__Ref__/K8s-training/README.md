# 🎓 K8s Training — Học Kubernetes Tiếng Việt

> Bộ tài liệu **40 bài** về Kubernetes (K8s) cơ bản, biên soạn từ video tiếng Việt của thầy Việt.

---

## 📋 Tổng Quan

- **Tổng số bài:** 40
- **Tổng module:** 11
- **Tổng thời lượng:** ~6-7 giờ video gốc + thực hành
- **Ngôn ngữ:** Tiếng Việt
- **Đối tượng:** Developer/DevOps mới học K8s
- **Prerequisites:** Biết Docker cơ bản

---

## 🗺️ Lộ Trình Học (Modules)

| Module | Tên | Số bài | Thời lượng | Cấp độ |
|--------|-----|--------|------------|--------|
| **00** | [Introduction](00-introduction/README.md) | 2 | ~15' | BEGINNER |
| **01** | [Core Concepts](01-core-concepts/README.md) | 3 | ~30' | BEGINNER |
| **02** | [Environment Setup](02-environment-setup/README.md) | 2 | ~25' | BEGINNER |
| **03** | [Pod & kubectl](03-pod-and-kubectl/README.md) | 4 | ~30' | BEGINNER |
| **04** | [Expose Pod (NodePort)](04-expose-pod-nodeport/README.md) | 2 | ~20' | INTERMEDIATE |
| **05** | [Imperative vs Declarative](05-imperative-vs-declarative/README.md) | 2 | ~20' | INTERMEDIATE |
| **06** | [ReplicaSet](06-replicaset/README.md) | 5 | ~35' | INTERMEDIATE |
| **07** | [Deployment](07-deployment/README.md) | 10 | ~57' | INTERMEDIATE |
| **08** | [Services](08-services/README.md) | 2 | ~27' | INTERMEDIATE |
| **09** | [Namespace](09-namespace/README.md) | 2 | ~18' | INTERMEDIATE |
| **10** | [Resource Management](10-resource-management/README.md) | 6 | ~55' | ADVANCED |

**TỔNG:** **40 bài** • **~5.5 giờ** content

---

## 🎯 Học Theo Cấp Độ

### 🟢 BEGINNER (Module 00 → 03)

Mục tiêu: Hiểu K8s là gì, cài đặt được môi trường, chạy Pod đầu tiên.

```
00 → 01 → 02 → 03
```

✅ **Thành quả:** Chạy được `kubectl run`, `kubectl logs`, `kubectl exec`.

---

### 🟡 INTERMEDIATE (Module 04 → 09)

Mục tiêu: Triển khai ứng dụng production-ready với Deployment + Service + Namespace.

```
04 → 05 → 06 → 07 → 08 → 09
```

✅ **Thành quả:** Deploy app với rolling update, rollback, expose qua NodePort/LoadBalancer.

---

### 🔴 ADVANCED (Module 10)

Mục tiêu: Quản lý tài nguyên trong môi trường multi-tenant.

```
10
```

✅ **Thành quả:** Cấu hình ResourceQuota + LimitRange + best practices CPU/Memory.

---

## 📐 Cấu Trúc Một Bài Học

```markdown
# Tên Bài
## 📋 Metadata          (Bài số, module, cấp độ, thời lượng)
## 🎯 Mục Tiêu Bài Học  (Checklist kiến thức)
## 📚 Nội Dung          (Lý thuyết + diagrams)
## 💻 Hands-On / Demo   (Code + lệnh thực hành)
## ⚠️ Lưu Ý             (Common pitfalls)
## ✅ Self-Check        (Câu hỏi ôn tập có đáp án)
## 🔗 Liên Kết          (Navigation, tài nguyên)
## 📝 Ghi Chú Từ Giảng Viên (Quote)
```

---

## 🛠️ Công Cụ Cần Có

### Bắt buộc

- 🐳 [Docker Desktop](https://www.docker.com/products/docker-desktop)
- 🅺 [Minikube](https://minikube.sigs.k8s.io/docs/start/) (local K8s cluster)
- ⌨️ [kubectl](https://kubernetes.io/docs/tasks/tools/) (CLI)
- 📝 [VS Code](https://code.visualstudio.com/) hoặc IDE có hỗ trợ YAML

### Khuyến nghị

- 📊 [Lens](https://k8slens.dev/) — K8s IDE GUI
- 💻 [k9s](https://k9scli.io/) — Terminal UI cho K8s
- 🔀 [k3d](https://k3d.io/) — Lightweight K8s thay Minikube

---

## 📚 Glossary (Thuật Ngữ Cốt Lõi)

| Thuật ngữ | Giải thích ngắn |
|-----------|-----------------|
| **Pod** | Đơn vị triển khai nhỏ nhất, chứa 1+ container |
| **ReplicaSet** | Đảm bảo N Pod chạy song song |
| **Deployment** | Quản lý ReplicaSet + rolling update + rollback |
| **Service** | Cung cấp địa chỉ IP/DNS ổn định cho Pod |
| **Namespace** | Phân vùng logic trong cluster |
| **Node** | Server vật lý/ảo trong cluster |
| **Cluster** | Tập hợp Node + Control Plane |
| **kubectl** | CLI tương tác với K8s |
| **Manifest** | File YAML mô tả resource |
| **Selector / Label** | Cơ chế gắn kết Service ↔ Pod |

---

## 🔗 Tài Nguyên Bổ Sung

### Tài liệu chính thức

- 📖 [Kubernetes Docs](https://kubernetes.io/docs/)
- 📖 [kubectl Cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- 🎓 [Kubernetes Tutorials](https://kubernetes.io/docs/tutorials/)

### Chứng chỉ (CNCF)

- 🏆 **CKA** (Certified Kubernetes Administrator) — Vận hành cluster
- 🏆 **CKAD** (Certified Kubernetes Application Developer) — Dev triển khai app
- 🏆 **CKS** (Certified Kubernetes Security Specialist) — Bảo mật

> 💡 Module 00, Bài #5 có chi tiết về CNCF certifications.

### Community VN

- 💬 Vietnam DevOps Group on Facebook/Telegram
- 🎥 Channel YouTube của thầy Việt (video gốc)

---

## 📁 Cấu Trúc Thư Mục

```
04-Knowledge/K8s-Training/
├── README.md                          ← BẠN ĐANG Ở ĐÂY
├── REBUILD-PLAN.md                    ← Kế hoạch tổng thể
│
├── 00-introduction/
│   ├── README.md
│   ├── 01-gioi-thieu-series.md       (Bài #1)
│   └── 02-he-thong-chung-chi-cncf.md (Bài #5)
│
├── 01-core-concepts/                  (3 bài: #2, #3, #4)
├── 02-environment-setup/              (2 bài: #6, #7)
├── 03-pod-and-kubectl/                (4 bài: #8, #11, #12, #33)
├── 04-expose-pod-nodeport/            (2 bài: #9, #10)
├── 05-imperative-vs-declarative/      (2 bài: #13, #14)
├── 06-replicaset/                     (5 bài: #15, #16, #17, #18, #19)
├── 07-deployment/                     (10 bài: #20-#29)
├── 08-services/                       (2 bài: #30, #31)
├── 09-namespace/                      (2 bài: #32, #34)
└── 10-resource-management/            (6 bài: #35-#40)
```

---

## ✍️ Cách Sử Dụng Bộ Tài Liệu

### Cách 1: Đọc theo lộ trình (recommended)

```
00 → 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 → 10
```

### Cách 2: Tra cứu theo chủ đề

- Cần triển khai app? → **Module 07 (Deployment)**
- Network lỗi? → **Module 08 (Services)**
- Tài nguyên không đủ? → **Module 10 (Resources)**

### Cách 3: Theo bài cụ thể

Mỗi bài đều có thể đọc độc lập. Chỉ cần xem **Prerequisites** trong Metadata.

---

## 🚀 Bắt Đầu Ngay

👉 **[Module 00 — Bài #1: Giới Thiệu Series](00-introduction/01-gioi-thieu-series.md)**

---

## 📝 Ghi Chú

- 📌 **Tác giả gốc (video):** Thầy Việt — Channel "Học Kubernetes & Amazon EKS Tiếng Việt"
- 📌 **Biên soạn lại (text):** Mr.Rom — biến lời nói (transcript) thành tài liệu có cấu trúc
- 📌 **Phiên bản:** v1.0.0
- 📌 **Ngày tạo:** 09/05/2026
- 📌 **License:** Cá nhân học tập

---

## 🤝 Đóng Góp

Nếu phát hiện lỗi đánh máy, sai kỹ thuật, hoặc muốn thêm ví dụ:

1. Sửa file Markdown
2. Cập nhật phiên bản trong file
3. Cập nhật `Last Updated` trong Metadata

---

**Chúc bạn học tốt và sớm trở thành K8s Engineer chuyên nghiệp! 🚀**
