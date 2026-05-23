# Kế Hoạch Biên Soạn Bộ Đào Tạo K8s từ Phụ Đề Video

> **Nguồn:** 40 file phụ đề tiếng Việt từ series "Học Kubernetes (K8s) và Amazon EKS"
> **Vị trí nguồn:** `04-Knowledge/K8s/`
> **Vị trí đích:** `04-Knowledge/K8s-Training/`
> **Tác giả gốc (giảng viên):** Việt
> **Người biên soạn lại:** Mr.Rom (với hỗ trợ AI)
> **Ngày tạo:** 09/05/2026

---

## 🎯 Mục Tiêu

Biến **40 file phụ đề thô** (speech-to-text tự động, nhiều lỗi chính tả) thành **bộ tài liệu đào tạo K8s có cấu trúc**, có thể đọc/học/ôn tập được, **giữ nguyên mạch giảng dạy của giảng viên** nhưng được:

- Làm sạch thuật ngữ ("ctic" → "K8s", "co tan" → "container", "noteb" → "NodePort"...)
- Cấu trúc lại thành các phần rõ ràng (lý thuyết, ẩn dụ, hands-on, lưu ý)
- Bổ sung code block YAML/kubectl đúng cú pháp
- Có metadata, mục tiêu học tập, self-check questions

---

## 📁 Cấu Trúc Thư Mục Đề Xuất

```
04-Knowledge/K8s-Training/
├── README.md                          # Index tổng – lộ trình học
├── REBUILD-PLAN.md                    # File này
│
├── 00-introduction/                   # Module 0: Khởi đầu
│   ├── README.md                      # Tổng quan module
│   ├── 01-gioi-thieu-series.md        # ← Bài #1
│   └── 02-he-thong-chung-chi-cncf.md  # ← Bài #5
│
├── 01-core-concepts/                  # Module 1: Khái niệm cốt lõi
│   ├── README.md
│   ├── 01-kubernetes-la-gi.md         # ← Bài #2
│   ├── 02-khi-nao-nen-dung-k8s.md     # ← Bài #3
│   └── 03-cluster-architecture.md     # ← Bài #4
│
├── 02-environment-setup/              # Module 2: Cài đặt môi trường
│   ├── README.md
│   ├── 01-cai-dat-minikube-kubectl-docker.md  # ← Bài #6
│   └── 02-kubernetes-version.md       # ← Bài #7
│
├── 03-pod-and-kubectl/                # Module 3: Pod & kubectl cơ bản
│   ├── README.md
│   ├── 01-pod-la-gi.md                # ← Bài #8
│   ├── 02-kubectl-logs.md             # ← Bài #11
│   ├── 03-kubectl-exec.md             # ← Bài #12
│   └── 04-curl-pod.md                 # ← Bài #33
│
├── 04-expose-pod-nodeport/            # Module 4: Expose Pod với NodePort
│   ├── README.md
│   ├── 01-nodeport-co-che-hoat-dong.md       # ← Bài #9
│   └── 02-nodeport-service-expose-pod.md     # ← Bài #10
│
├── 05-imperative-vs-declarative/      # Module 5: Imperative vs Declarative & YAML
│   ├── README.md
│   ├── 01-imperative-vs-declarative.md       # ← Bài #13
│   └── 02-yaml-manifest-101.md               # ← Bài #14
│
├── 06-replicaset/                     # Module 6: ReplicaSet
│   ├── README.md
│   ├── 01-gioi-thieu-replicaset.md           # ← Bài #15
│   ├── 02-replicaset-labels-vs-selector.md   # ← Bài #16
│   ├── 03-expose-replicaset-imperative.md    # ← Bài #17
│   ├── 04-expose-replicaset-declarative.md   # ← Bài #18
│   └── 05-edit-replicaset-va-deployment.md   # ← Bài #19
│
├── 07-deployment/                     # Module 7: Deployment
│   ├── README.md
│   ├── 01-create-deployment.md               # ← Bài #20
│   ├── 02-scale-expose-deployment.md         # ← Bài #21
│   ├── 03-set-container-image.md             # ← Bài #22
│   ├── 04-rollout-deployment.md              # ← Bài #23
│   ├── 05-rollback-deployment.md             # ← Bài #24
│   ├── 06-pause-resume-deployment.md         # ← Bài #25
│   ├── 07-change-cause-revision.md           # ← Bài #26
│   ├── 08-recreate-vs-rollingupdate.md       # ← Bài #27
│   ├── 09-progress-deadline-seconds.md       # ← Bài #28
│   └── 10-restart-deployment.md              # ← Bài #29
│
├── 08-services/                       # Module 8: Services
│   ├── README.md
│   ├── 01-services-types-ly-thuyet.md        # ← Bài #30
│   └── 02-services-types-demo.md             # ← Bài #31
│
├── 09-namespace/                      # Module 9: Namespace
│   ├── README.md
│   ├── 01-namespace.md                       # ← Bài #32
│   └── 02-namespace-vs-cluster.md            # ← Bài #34
│
└── 10-resource-management/            # Module 10: Resource Management
    ├── README.md
    ├── 01-requests-and-limits.md             # ← Bài #35
    ├── 02-khuyen-nghi-cau-hinh-cpu-memory.md # ← Bài #36
    ├── 03-command-and-args.md                # ← Bài #37
    ├── 04-enable-metrics-server.md           # ← Bài #38
    ├── 05-resource-quotas.md                 # ← Bài #39
    └── 06-limit-ranges.md                    # ← Bài #40
```

**Tổng:** 11 module + 40 file bài học + 1 README chính + 11 README module = **52 file markdown**

---

## 📝 Bố Cục Mỗi File Bài Học

Mỗi file bài học sẽ có cấu trúc thống nhất gồm các phần:

```markdown
# [Tên Bài]

## 📋 Metadata
- Bài số (#X), Module, Cấp độ, Thời lượng video, Prerequisites, Last Updated

## 🎯 Mục Tiêu Bài Học
- Liệt kê 3-5 điều học viên sẽ làm được sau bài

## 📚 Nội Dung
### 1. [Phần lý thuyết 1]
   - Khái niệm
   - Ẩn dụ/ví dụ đời thường (giữ từ giảng viên)
   - Sơ đồ ASCII nếu cần
### 2. [Phần lý thuyết 2]
   ...

## 💻 Hands-On / Demo
### Setup
### Commands
### YAML manifest (nếu có)
### Expected Output

## ⚠️ Lưu Ý & Common Pitfalls
- Bullet các điểm dễ nhầm

## ✅ Self-Check
- 3-5 câu hỏi tự kiểm tra

## 🔗 Liên Kết
- ← Bài trước
- → Bài tiếp theo
- 📺 Video gốc

## 📝 Ghi Chú Từ Giảng Viên
- Quote những lời khuyên/insight quan trọng từ bài giảng gốc
```

---

## 🛠️ Quy Trình Biên Soạn Mỗi Bài

1. **Đọc file phụ đề thô** từ `04-Knowledge/K8s/Decopy_✅ #X _ ...txt`
2. **Hiểu nội dung** giảng viên muốn truyền tải
3. **Làm sạch thuật ngữ** kỹ thuật (giữ glossary thống nhất - xem dưới)
4. **Cấu trúc lại** thành các phần theo template
5. **Bổ sung code/YAML/sơ đồ** đúng cú pháp K8s
6. **Giữ phong cách** thân thiện của giảng viên (xưng hô "bạn", "mình"...)

### Glossary thuật ngữ thống nhất

| Phụ đề thô | Đúng |
|------------|------|
| ctic, catet, k8s, K38s | K8s / Kubernetes |
| co tan, container | container |
| noteb, Note p, notb | NodePort |
| iks, exs, x | EKS |
| ws, adds, aws, abe | AWS |
| q ctl, k ctl, kctl, kết | kubectl |
| port (Pod) | Pod |
| Note (Node) | Node |
| service | Service |
| diệt vụ, dị vụ | dịch vụ |
| Q proxy | kube-proxy |
| Core DNS | CoreDNS |
| O json, OB | Orchestrator / Orchestration |
| min, mini | Minikube |
| Kai | Kind |
| s c, s car | sidecar |

---

## ✅ Tiến Độ — HOÀN THÀNH 100%

- [x] Phân tích 40 file phụ đề
- [x] Đề xuất bố cục thư mục
- [x] Đề xuất template bài học
- [x] **File mẫu Bài #1** ([xem tại đây](00-introduction/01-gioi-thieu-series.md))
- [x] Module 0: Introduction (2 bài) ✅
- [x] Module 1: Core concepts (3 bài) ✅
- [x] Module 2: Environment setup (2 bài) ✅
- [x] Module 3: Pod & kubectl (4 bài) ✅
- [x] Module 4: NodePort (2 bài) ✅
- [x] Module 5: Imperative vs Declarative (2 bài) ✅
- [x] Module 6: ReplicaSet (5 bài) ✅
- [x] Module 7: Deployment (10 bài) ✅
- [x] Module 8: Services (2 bài) ✅
- [x] Module 9: Namespace (2 bài) ✅
- [x] Module 10: Resource Management (6 bài) ✅
- [x] README.md chính + 11 README module ✅

**TỔNG:** 40 bài + 11 module README + 1 README chính + 1 REBUILD-PLAN = **53 files** Markdown.

---

## 📊 Thống Kê Cuối

| Module | Số bài | File |
|--------|--------|------|
| 00-introduction | 2 | 3 (gồm README) |
| 01-core-concepts | 3 | 4 |
| 02-environment-setup | 2 | 3 |
| 03-pod-and-kubectl | 4 | 5 |
| 04-expose-pod-nodeport | 2 | 3 |
| 05-imperative-vs-declarative | 2 | 3 |
| 06-replicaset | 5 | 6 |
| 07-deployment | 10 | 11 |
| 08-services | 2 | 3 |
| 09-namespace | 2 | 3 |
| 10-resource-management | 6 | 7 |
| **TỔNG** | **40 bài** | **51 + 2 root files** |

🎉 **Bộ tài liệu sẵn sàng sử dụng!** Bắt đầu từ [`README.md`](README.md).
