# Bài #1 — Giới Thiệu Series Học Kubernetes (K8s) & Amazon EKS

---

## 📋 Metadata

- **Bài số:** #1
- **Module:** 00-introduction
- **Cấp độ:** `BEGINNER`
- **Thời lượng video gốc:** ~5 phút
- **Prerequisites:** Không yêu cầu
- **Last Updated:** 09/05/2026
- **Author:** Mr.Rom 

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Nắm được **lộ trình tổng thể** của series 3 phần (Fundamentals → EKS → Production)
- [ ] Biết **những chủ đề chính** sẽ được học trong toàn bộ khóa
- [ ] Hiểu **cách tiếp cận học hiệu quả** (skip phần đã biết, tăng tốc độ video, hands-on)
- [ ] Biết **các công cụ phụ trợ** sẽ dùng (Minikube, kubectl, Docker, Terraform, AWS CDK, ArgoCD, Karpenter…)

---

## 📚 Nội Dung

### 1. Lộ Trình Series 3 Phần

Toàn bộ series được chia thành **3 phần chính**, đi từ nền tảng đến triển khai chuyên nghiệp:

```
┌─────────────────────────────────────────────────────────────┐
│ PHẦN 1: KUBERNETES FUNDAMENTALS                              │
│  • Pod, ReplicaSet, Deployment, Service, Namespace           │
│  • ConfigMap, Secret, Volume                                 │
│  • Ingress, RBAC, Resource Quota                             │
│  → Nền tảng cốt lõi, BẮT BUỘC nắm chắc                       │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ PHẦN 2: AMAZON EKS (K8s trên AWS)                            │
│  • Vì sao cần EKS thay vì tự host K8s                        │
│  • EKS giải quyết những khó khăn nào của K8s self-managed    │
│  • Cách triển khai cùng một workload trên EKS so với K8s     │
│  • Tích hợp với AWS services: S3, RDS, Secrets Manager…      │
│  → Hiểu khi nào nên/không nên dùng EKS                       │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ PHẦN 3: PRODUCTION DEPLOYMENT                                │
│  • Infrastructure as Code: AWS CDK & Terraform               │
│  • CI/CD tự động hóa với ArgoCD, GitOps                      │
│  • Cost optimization với Karpenter                           │
│  • Kinh nghiệm thực tế từ AWS với khách hàng lớn             │
│  → Vận hành K8s ở quy mô doanh nghiệp                        │
└─────────────────────────────────────────────────────────────┘
```

### 2. Phần 1 – Kubernetes Fundamentals

**Mục tiêu:** Nắm thật chắc kiến trúc, các khái niệm cốt lõi của K8s, và cách thao tác bằng `kubectl` ở mức hands-on.

**Lý do quan trọng:** K8s có hệ sinh thái vệ tinh **rất lớn** (CNCF có hàng trăm dự án). Nếu không nắm chắc fundamentals, bạn sẽ dễ bị "mù lung" khi đứng trước quá nhiều lựa chọn.

> 💬 *"Quá nhiều sự lựa chọn khiến các bạn rất bị mù lung. Phần này các bạn cần phải nắm thật chắc thì các bạn mới qua phần tiếp theo nó vững được."* — thầy Việt

### 3. Phần 2 – Amazon EKS

Sau khi hiểu K8s vanilla, ta sẽ thấy nó có nhiều **pain points** khi self-host (quản lý control plane, cập nhật version, HA, security…). EKS là **managed service** của AWS giải quyết các vấn đề đó.

Nội dung Phần 2 sẽ:

- So sánh **K8s self-managed** vs **EKS** ở các tình huống thực tế (ConfigMap, Node Affinity, Network…).
- Triển khai **chính cùng một workload** trên cả 2 môi trường để thấy điểm khác/giống.
- Tích hợp EKS với các AWS services xung quanh:
  - **Amazon S3**: lưu static files
  - **RDS / DynamoDB**: cơ sở dữ liệu
  - **AWS Secrets Manager**: tách sensitive info ra khỏi cluster

### 4. Phần 3 – Production Deployment

Phần này phân biệt **"chạy được"** (Phần 2) với **"chạy professional"** (Phần 3). Tập trung vào:

| Chủ đề                           | Công cụ                                                  |
| -------------------------------- | -------------------------------------------------------- |
| Infrastructure as Code           | **AWS CDK** (cho dev) hoặc **Terraform** (cho non-coder) |
| CI/CD & GitOps                   | **ArgoCD**                                               |
| Auto-scaling & Cost Optimization | **Karpenter**                                            |
| Production checklist             | Best practices từ kinh nghiệm thực tế                    |

---

## 💡 Cách Học Hiệu Quả Nhất

Lời khuyên trực tiếp từ giảng viên:

| Vấn đề                | Giải pháp                                      |
| --------------------- | ---------------------------------------------- |
| Đã biết một topic rồi | **Skip** bài đó, không cần xem lại             |
| Cần review nhanh      | **Tăng tốc độ phát** trên YouTube (1.25x – 2x) |
| Cần xem code chi tiết | Pause, zoom vào, hands-on theo                 |
| Có ý kiến/thắc mắc    | **Comment** để giảng viên điều chỉnh nội dung  |

> 💬 *"Đây không phải là content chết. Content này dựa trên các bạn — các bạn bình luận tích cực để chúng ta cùng học, cùng làm, cùng chia sẻ."*

---

## 💻 Hands-On / Demo

Bài này là bài **giới thiệu**, không có demo. Các công cụ sẽ dùng xuyên suốt series:

```bash
# Phần 1 – cài đặt môi trường local (sẽ có ở Bài #6)
brew install --cask docker
brew install kubectl
brew install minikube

# Phần 2 – tài khoản AWS
aws configure

# Phần 3 – IaC tools
brew install terraform
npm install -g aws-cdk
```

> Chi tiết cài đặt: xem [Bài #6 – Cài đặt Minikube, kubectl, Docker](../02-environment-setup/01-cai-dat-minikube-kubectl-docker.md).

---

## ⚠️ Lưu Ý

- ✅ **Học theo thứ tự** — nhất là Phần 1, vì các bài sau dựa trên kiến thức bài trước.
- ✅ **Đừng bỏ qua hands-on** — K8s là công cụ thực hành, không phải lý thuyết.
- ❌ **Đừng cố nhớ hết** ngay từ đầu — hệ sinh thái rất lớn, bạn sẽ học dần qua từng bài.
- ❌ **Đừng so sánh sớm** với các tool khác (Docker Swarm, Nomad…) — hãy tập trung học K8s trước.

---

## ✅ Self-Check

1. **Series này có bao nhiêu phần chính?**
   <details>
   <summary>Đáp án</summary>
   3 phần: Fundamentals → EKS → Production Deployment
   </details>

2. **Vì sao cần Phần 2 (EKS) sau khi đã có Phần 1 (K8s Fundamentals)?**
   <details>
   <summary>Đáp án</summary>
   Vì K8s self-managed có nhiều pain points (quản lý control plane, HA, security update…). EKS là managed service của AWS giúp giải quyết các pain points này.
   </details>

3. **Trong Phần 3, hai công cụ Infrastructure as Code nào sẽ được giới thiệu?**
   <details>
   <summary>Đáp án</summary>
   AWS CDK (cho người biết lập trình) và Terraform (cho người không rành ngôn ngữ lập trình).
   </details>

4. **Ngoài K8s/EKS, cần học thêm những công cụ ecosystem nào?**
   <details>
   <summary>Đáp án</summary>
   ArgoCD (GitOps), Karpenter (auto-scaling), AWS S3/RDS/Secrets Manager (services xung quanh).
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ Đây là bài **đầu tiên**
- ➡️ [Bài #2 — Kubernetes là gì? K8s là gì?](../01-core-concepts/01-kubernetes-la-gi.md)
- 🏠 [Quay về index Module 00 – Introduction](README.md)
- 🏠 [Quay về index Series K8s Training](../README.md)

### Tài Nguyên

- 📺 [Video gốc: #1 Giới Thiệu](../../K8s/Decopy_✅%20%231%20_%20Gi%E1%BB%9Bi%20Thi%E1%BB%87u%20_%20H%E1%BB%8Dc%20Kubernetes%20%28K8s%29%20v%C3%A0%20Amazon%20EKS%20Ti%E1%BA%BFng%20Vi%E1%BB%87t%20Full_captions.txt)
- 📖 [Kubernetes Official Docs](https://kubernetes.io/docs/home/)
- 📖 [Amazon EKS User Guide](https://docs.aws.amazon.com/eks/)
- 📖 [CNCF Landscape](https://landscape.cncf.io/) — bản đồ hệ sinh thái Cloud Native

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Mình sẽ đẩy tốc độ nhanh ở Phần 1 để các bạn qua được Phần 2 thật là sớm. Khi các bạn làm xong Phần 2, các bạn hoàn toàn có thể tự tin build cho ứng dụng của các bạn ở những quy mô phổ biến của doanh nghiệp."*

> 💬 *"Một cái Tool không thể dùng cho tất cả mọi thứ được. Chúng ta cũng sẽ thảo luận một số trường hợp NÊN và KHÔNG NÊN sử dụng EKS / K8s cho ứng dụng của mình."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
**Cập nhật lần cuối:** 09/05/2026
