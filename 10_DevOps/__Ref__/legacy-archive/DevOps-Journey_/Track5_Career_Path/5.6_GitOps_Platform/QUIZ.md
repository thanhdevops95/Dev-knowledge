# ❓ Quiz: GitOps Platform

> **Knowledge Check for GitOps (5 Questions)**
>
> *Kiểm tra kiến thức GitOps (5 câu hỏi).*

---

### Q1: GitOps Definition

What is the core principle of GitOps?

*(Nguyên tắc cốt lõi của GitOps là gì?)*

- a) Manual deployments *(Triển khai thủ công)*
- b) Git as single source of truth *(Git là nguồn sự thật duy nhất)*
- c) No version control *(Không kiểm soát phiên bản)*
- d) Direct API calls *(Gọi API trực tiếp)*

---

### Q2: ArgoCD Architecture

What component syncs applications in ArgoCD?

*(Component nào đồng bộ applications trong ArgoCD?)*

- a) API Server
- b) Repo Server
- c) Application Controller
- d) Dex

---

### Q3: Sync Policy

What does `selfHeal: true` do in ArgoCD?

*(`selfHeal: true` làm gì trong ArgoCD?)*

- a) Delete application *(Xóa application)*
- b) Auto-sync when drift detected *(Tự động sync khi phát hiện drift)*
- c) Manual sync only *(Chỉ sync thủ công)*
- d) Ignore changes *(Bỏ qua thay đổi)*

---

### Q4: Flux Components

Which is NOT a Flux component?

*(Cái nào KHÔNG phải component của Flux?)*

- a) Source Controller
- b) Kustomize Controller
- c) Sync Controller *(Controller đồng bộ)*
- d) Helm Controller

---

### Q5: GitOps Tools

What is the relationship between Git and Kubernetes in GitOps?

*(Mối quan hệ giữa Git và Kubernetes trong GitOps là gì?)*

- a) Git pulls from Kubernetes *(Git pull từ Kubernetes)*
- b) Kubernetes state is synced from Git *(Trạng thái Kubernetes được sync từ Git)*
- c) No relationship *(Không có quan hệ)*
- d) Bidirectional sync *(Sync hai chiều)*

---

## 📝 Answers

<details>
<summary>Click to view answers / Nhấn để xem đáp án</summary>

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | b | Git repository is the source of truth |
| 2 | c | Application Controller monitors and syncs |
| 3 | b | Self-heal reverts manual changes |
| 4 | c | Flux has Source, Kustomize, Helm, Notification controllers |
| 5 | b | Kubernetes desired state comes from Git |

</details>

---

**[← Back to README](./README.md)**
