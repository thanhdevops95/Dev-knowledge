# Bài #2 — Kubernetes là gì? K8s là gì?

---

## 📋 Metadata

- **Bài số:** #2
- **Module:** 01-core-concepts
- **Cấp độ:** `BEGINNER`
- **Thời lượng video gốc:** ~7 phút
- **Prerequisites:** [Bài #1 — Giới thiệu series](../00-introduction/01-gioi-thieu-series.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Hiểu **lịch sử tiến hóa** từ Server-based → VM → Container → Kubernetes
- [ ] Trả lời được **vì sao cần Kubernetes** (vấn đề mà K8s giải quyết)
- [ ] Phân biệt được **Container** vs **Pod** (khái niệm sơ bộ)
- [ ] Biết **Container Orchestrator** là gì và vì sao K8s là lựa chọn phổ biến nhất

---

## 📚 Nội Dung

### 1. Lịch Sử Tiến Hóa Triển Khai Phần Mềm

#### Giai đoạn 1: Server-based (Bare metal / VM)

```
┌─────────────────────────────────────┐
│              APP                     │  ← Ứng dụng
├─────────────────────────────────────┤
│            LIBRARY                   │  ← Thư viện phụ trợ
├─────────────────────────────────────┤
│       PLATFORM (runtime)             │  ← Nginx / Node.js / JVM
├─────────────────────────────────────┤
│       OS (Linux / Windows)           │  ← Hệ điều hành
└─────────────────────────────────────┘
```

Mỗi server (vật lý hoặc VM) chạy 1 stack độc lập — gọi là **Software Definition** thông qua **virtualization**.

**Ưu điểm:** ổn định, từng có thời kỳ là tiêu chuẩn.

**Nhược điểm sau thời gian dài:**

| Vấn đề                  | Mô tả                                                            |
| ----------------------- | ---------------------------------------------------------------- |
| **Lãng phí tài nguyên** | Server quá to so với app — tốn RAM/CPU không cần thiết           |
| **Khó scale độc lập**   | Nếu deploy monolith, không thể scale riêng từng dịch vụ con      |
| **Inconsistency**       | "Em chạy được trên máy em mà!" — môi trường dev ≠ staging ≠ prod |
| **Release chậm**        | Build & deploy 1 monolith có thể mất nửa ngày                    |

#### Giai đoạn 2: Container (Docker)

**Container giải quyết** tất cả các vấn đề trên bằng cách **đóng gói toàn bộ stack** (code + runtime + library + config) thành 1 đơn vị **portable**:

```
Container = code + runtime + library + config (ALL-IN-ONE)
```

> 💬 *"Container deploy vào ở đâu cũng vẫn là container đấy — nó không có sự khác biệt giữa máy dev với máy production."*

**Docker** là tổ chức/software phổ biến nhất hiện thực concept này (build, run, registry…).

#### Giai đoạn 3: Container Orchestration

Khi có **rất nhiều container** chạy trên **nhiều server**, ai sẽ:

- Quyết định container nào chạy ở server nào?
- Tự động restart khi crash?
- Scale up/down theo tải?
- Load balance giữa các replica?
- Update không downtime?

→ **Cần một "nhạc trưởng"** — gọi là **Container Orchestrator**.

```
┌──────────────────────────────────────────────────────────┐
│               🎼 ORCHESTRATOR (Nhạc Trưởng)               │
│                                                          │
│   "Container A → Server 1, scale lên 6 replicas"         │
│   "Container B crashed → restart trên Server 2"          │
│   "Đêm tải thấp → scale Container C xuống 2 replicas"    │
└──────────────────────────────────────────────────────────┘
       ↓ điều phối ↓ điều phối ↓ điều phối
   Server 1      Server 2      Server 3
```

### 2. Kubernetes — Orchestrator Phổ Biến Nhất

**Kubernetes** (viết tắt **K8s** — chữ "8" là 8 ký tự `ubernete` giữa K và s) là Orchestrator được phát triển bởi Google, hiện do **CNCF** maintain.

```
K[ubernete]s   ← 8 ký tự ⇒ "K8s"
```

**Vì sao K8s là lựa chọn #1?**

- ✅ Cộng đồng cực lớn (Google, AWS, Microsoft, IBM, Red Hat… đầu tư)
- ✅ Hệ sinh thái vệ tinh phong phú (CNCF Landscape có hàng trăm dự án)
- ✅ Tài liệu chính thức rất tốt
- ✅ Cơ hội việc làm cao
- ✅ Linh hoạt: chạy được on-premise lẫn cloud (AWS/GCP/Azure)
- ✅ Multi-tenant + Security tốt

**Đối thủ cạnh tranh:** Docker Swarm, HashiCorp Nomad, Amazon ECS — nhưng K8s vẫn là **de facto standard**.

### 3. Pod — Khái Niệm Cơ Bản Đầu Tiên

Trên K8s, **đơn vị nhỏ nhất** được triển khai **không phải container** mà là **Pod**.

```
┌──────────────────────────────────┐
│            POD                    │
│  ┌─────────┐  ┌─────────┐         │
│  │Container│  │Container│         │
│  │   #1    │  │   #2    │         │
│  └─────────┘  └─────────┘         │
└──────────────────────────────────┘
```

**Mỗi Pod có thể chứa 1 hoặc nhiều container** chia sẻ:
- Cùng IP
- Cùng storage volume
- Cùng network namespace

**Best practice:** 1 Pod = 1 container (trừ pattern sidecar đặc biệt — sẽ học sau).

> 💡 Chi tiết về Pod sẽ được học kỹ ở [Bài #8 — Pod là gì?](../03-pod-and-kubectl/01-pod-la-gi.md)

### 4. Ví Dụ Thực Tế: User Service & Payment Service

```
Trước Container:
┌─────────────────────┐  ┌─────────────────────┐
│   Server (4GB RAM)  │  │   Server (4GB RAM)  │
│   User App         │  │   Payment App       │
└─────────────────────┘  └─────────────────────┘
       ❌ Lãng phí RAM, scale khó


Sau Container + K8s:
   user-pod-1  user-pod-2  user-pod-3  user-pod-4  ← scale 4x vì traffic cao
   payment-pod-1  payment-pod-2                    ← chỉ cần 2x
        ↑                       ↑
    K8s tự động co giãn theo nhu cầu
```

K8s giúp bạn **co giãn độc lập** từng dịch vụ, **tận dụng tối đa** tài nguyên.

---

## 💻 Hands-On / Demo

Bài này là bài **lý thuyết**. Hands-on bắt đầu từ Bài #6 (cài đặt Minikube). Tuy nhiên, bạn có thể tham khảo trước:

```bash
# Xem CNCF Landscape để hình dung hệ sinh thái
open https://landscape.cncf.io/

# Xem Kubernetes documentation
open https://kubernetes.io/docs/concepts/overview/
```

---

## ⚠️ Lưu Ý

- ❌ **Đừng nhầm:** Container ≠ Pod. Pod là wrapper của 1+ container.
- ❌ **Đừng nhầm:** Kubernetes ≠ Docker. Docker là container runtime, K8s là orchestrator. K8s thậm chí có thể dùng container runtime khác (containerd, CRI-O).
- ✅ **Nhớ:** "K8s" và "Kubernetes" là **một**. "K8s" chỉ là viết tắt vì tên dài.
- ✅ **Nhớ:** K8s **không thay thế Docker** — chúng làm việc với nhau (Docker build image, K8s deploy & manage).

---

## ✅ Self-Check

1. **Vì sao K8s viết tắt là "K8s" mà không phải "K10s" hay "Ks"?**
   <details>
   <summary>Đáp án</summary>
   Vì giữa chữ K và s có **8 ký tự**: `K[ubernete]s` ⇒ K8s.
   </details>

2. **Container giải quyết vấn đề gì so với VM truyền thống?**
   <details>
   <summary>Đáp án</summary>
   - Đóng gói toàn bộ stack (code + runtime + library + config) → portable
   - Nhẹ hơn VM (không cần OS riêng)
   - Đảm bảo "chạy như nhau ở mọi môi trường" (dev = staging = prod)
   </details>

3. **Vì sao cần Container Orchestrator?**
   <details>
   <summary>Đáp án</summary>
   Khi có hàng chục/trăm container chạy trên nhiều server, không thể quản lý thủ công. Orchestrator tự động:
   - Lập lịch deploy container nào lên server nào
   - Restart khi crash
   - Scale up/down
   - Load balance
   - Rolling update không downtime
   </details>

4. **Tổ chức nào hiện đang maintain Kubernetes?**
   <details>
   <summary>Đáp án</summary>
   **CNCF** (Cloud Native Computing Foundation) — thuộc Linux Foundation. Ban đầu được Google phát triển và donate cho CNCF.
   </details>

5. **Pod chứa được bao nhiêu container?**
   <details>
   <summary>Đáp án</summary>
   1 hoặc nhiều container. Best practice là 1 Pod = 1 container, ngoại trừ pattern sidecar (vd: 1 main container + 1 logging/monitoring sidecar).
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #1 — Giới thiệu series](../00-introduction/01-gioi-thieu-series.md)
- ➡️ [Bài #3 — Lý do nên & không nên dùng K8s](02-khi-nao-nen-dung-k8s.md)
- 🏠 [Quay về index Module 01 — Core Concepts](README.md)

### Tài Nguyên

- 📖 [Kubernetes Overview (Official)](https://kubernetes.io/docs/concepts/overview/)
- 📖 [What is a Container? (Docker)](https://www.docker.com/resources/what-container/)
- 🌐 [CNCF Landscape](https://landscape.cncf.io/)
- 📺 Video gốc: `Decopy_✅ #2 _ Kubernetes là gì_ K8s là gì_..._captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Container nó sinh ra một cái ý niệm: 'cầm container deploy vào ở đâu nó vẫn là container đấy' — không có sự khác biệt giữa máy em với máy production. Đây là điều mà server-based truyền thống không làm được."*

> 💬 *"Nhạc trưởng — orchestrator — không làm vấn đề xử lý ứng dụng cho mình. Nó làm nhiệm vụ điều phối: lúc thì triển khai container ở Node này, lúc thì tắt nó, lúc thì co hẹp lại."*

> 💬 *"Cộng đồng sử dụng và phát triển K8s rất nhiều — Amazon, Google, Microsoft, IBM... Cho nên cơ hội việc làm cũng sẽ rất nhiều."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
