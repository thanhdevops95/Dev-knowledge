# Bài #3 — Lý Do NÊN & KHÔNG NÊN Sử Dụng Kubernetes

> ⚠️ **Đây là bài "nhạy cảm" theo lời giảng viên** — vì K8s không phải lúc nào cũng là lựa chọn đúng. Đọc kỹ trước khi quyết định đầu tư thời gian học.

---

## 📋 Metadata

- **Bài số:** #3
- **Module:** 01-core-concepts
- **Cấp độ:** `BEGINNER` (định hướng)
- **Thời lượng video gốc:** ~10 phút
- **Prerequisites:** [Bài #2 — Kubernetes là gì?](01-kubernetes-la-gi.md)
- **Last Updated:** 09/05/2026

---

## 🎯 Mục Tiêu Bài Học

Sau khi hoàn thành bài này, bạn sẽ:

- [ ] Liệt kê được **5 lý do NÊN** học và dùng K8s
- [ ] Liệt kê được **lý do KHÔNG NÊN** dùng K8s
- [ ] Biết các **alternative** thay thế K8s và khi nào dùng chúng
- [ ] Có quyết định đúng đắn: **K8s có phù hợp với mình/team/công ty không?**

---

## 📚 Nội Dung

### 1. ✅ 5 Lý Do NÊN Học & Dùng K8s

#### 1️⃣ K8s là Tiêu Chuẩn Ngành (De-facto Standard)

> 💬 *"Giống như đi đường nói xe máy thì người ta nghĩ ngay đến Honda — nói container orchestrator thì người ta nghĩ ngay đến K8s."*

Theo khảo sát **CNCF Annual Survey** (3,800 organization tham gia):

```
✅ 96% tổ chức đã hoặc đang đánh giá K8s
✅ 64% trong số đó đã chạy K8s trên PRODUCTION
   (không phải chỉ thử nghiệm/học tập)
```

→ **Số liệu này cực kỳ thuyết phục.**

#### 2️⃣ Tốc Độ Innovation Cực Nhanh

- Các công ty lớn (AWS/Google/Microsoft/IBM) đổ nguồn lực phát triển
- Release minor version **mỗi ~4 tháng** — bắt kịp nhu cầu thị trường
- Container hóa giúp release app **nhanh hơn 10x** so với monolith truyền thống
  - Hồi xưa: build & deploy 1 monolith = nửa ngày
  - Bây giờ: build & deploy = vài chục phút (thậm chí <10 phút)

#### 3️⃣ Tiết Kiệm Chi Phí Hạ Tầng

- **Auto-scaling** thông minh: tăng theo tải, giảm khi rảnh
- **Bin packing**: nhồi nhiều container/Pod vào cùng 1 Node
- Tận dụng được spot/preemptible instances trên cloud

→ **Cost optimization** tốt hơn server-based truyền thống.

#### 4️⃣ Lợi Thế Hiring & Career

| Cho công ty                                    | Cho cá nhân (DevOps/Developer)                |
| ---------------------------------------------- | --------------------------------------------- |
| Dễ tuyển người (skill phổ biến)                | Cơ hội việc làm cao (cả nội địa + nước ngoài) |
| Đầu tư long-term yên tâm (không sợ "hết thời") | Lương tốt hơn                                 |
| Cộng đồng hỗ trợ lớn                           | CV nổi bật hơn                                |

#### 5️⃣ Linh Hoạt + Security Tốt (yếu tố cá nhân giảng viên thích nhất)

> 💬 *"Mình cực kỳ thích cái Security của K8s. Công việc cụ thể của mình là làm Software Service — có pattern liên quan đến **isolation** (cô lập)."*

K8s xử lý **multi-tenant** rất tốt:
- Cô lập **vật lý** (different nodes)
- Cô lập **logic** (Namespace)
- Cấp phát/quản lý chi phí trên từng tenant
- Network Policy fine-grained

→ Phù hợp cho **SaaS** phục vụ nhiều khách hàng dùng chung hạ tầng.

---

### 2. ❌ Khi NÀO KHÔNG NÊN Dùng K8s?

#### ⚠️ Nhược Điểm Lớn Nhất: Learning Curve KHỦNG KHIẾP

> 💬 *"Dùng K8s thì các bạn phải xác định learning curve dài. Mình nghĩ phải tối thiểu **3-6 tháng** mới nói chuyện được với nhau."*

```
Tuần 1-4:   "Pod là gì? YAML lạ vậy?"  ← bối rối
Tháng 2-3:  "Deployment OK, Service OK..."  ← dần quen
Tháng 4-6:  "Networking + Storage + Security..."  ← bắt đầu sâu
Tháng 6+:   "Mình hiểu rồi!"  ← thật ra mới chỉ surface
```

**Đặc biệt:** chỉ cần **bỏ 1-2 tuần không dùng** là quên ngay → cần thực hành liên tục.

#### Khi NÀO Nên Dùng Alternative?

K8s **KHÔNG PHẢI** là lựa chọn đúng nếu:

| Tình huống                              | Khuyến nghị                                 |
| --------------------------------------- | ------------------------------------------- |
| Team nhỏ (1-3 dev), cần đơn giản        | **AWS ECS** hoặc **Docker Swarm**           |
| App cần scale quy mô vừa, chạy trên AWS | **Amazon ECS** (Fargate)                    |
| Học K8s để có việc làm                  | ✅ Vẫn nên học K8s                           |
| Cần multi-tenant + security cao         | ✅ K8s tốt nhất                              |
| App nhỏ, monolith, ít traffic           | **App Runner / Elastic Beanstalk / Heroku** |

#### Các Alternative Phổ Biến

| Tool                     | Bên cung cấp | Khi nào dùng                   |
| ------------------------ | ------------ | ------------------------------ |
| **Docker Swarm**         | Docker       | Đơn giản, nhỏ, học nhanh       |
| **HashiCorp Nomad**      | HashiCorp    | Linh hoạt, không chỉ container |
| **AWS ECS**              | AWS          | Đã ở trên AWS, muốn quản lý dễ |
| **AWS App Runner**       | AWS          | App rất đơn giản               |
| **Cloud Run**            | Google Cloud | Serverless containers          |
| **Azure Container Apps** | Microsoft    | App trên Azure                 |

#### Quan Điểm Cá Nhân Giảng Viên

> 💬 *"Cá nhân mình chỉ xoay quanh hai thứ: **ECS** hoặc **EKS**. Với dự án cá nhân, mình ưu tiên **ECS trước** vì học rất dễ, intuitive, gọn gàng. Còn ứng dụng cần security cao, multi-tenant thì mới dùng EKS."*

> 💬 *"Mình KHÔNG nên dùng 1 Tool cho tất cả mọi thứ. Mình đã làm việc với rất nhiều khách hàng dùng K8s cho everything — chi phí của họ không hề rẻ và phải mất rất nhiều thời gian để refactor."*

---

### 3. Bảng Quyết Định Nhanh

```
┌─────────────────────────────────────────────────────────────┐
│  CÂU HỎI                                  → CÔNG CỤ          │
├─────────────────────────────────────────────────────────────┤
│  Học để có việc làm?                      → ✅ K8s          │
│  CV nhiều dự án, làm SRE/DevOps?          → ✅ K8s          │
│  Multi-tenant SaaS, security quan trọng?   → ✅ K8s          │
│  Hệ thống quy mô lớn (hàng trăm services)?→ ✅ K8s          │
│                                                              │
│  Team nhỏ, cần ship nhanh?                → ❌ AWS ECS      │
│  App đơn giản, monolith?                  → ❌ App Runner   │
│  Đang ở AWS, ít resource DevOps?          → ❌ ECS Fargate  │
│  Cần serverless container?                → ❌ Cloud Run    │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Lưu Ý Quan Trọng

- 🚨 **Đừng học K8s chỉ vì "trendy"** — nếu công ty/dự án không thực sự cần, bạn sẽ over-engineering.
- 🚨 **Complexity ≠ Better.** Sự linh hoạt của K8s đi kèm độ phức tạp lớn.
- 🚨 **Đừng dùng K8s cho EVERYTHING** — luôn cân nhắc alternative trước.
- ✅ **Học K8s vẫn rất đáng** vì là kỹ năng phổ biến → có việc làm tốt.
- ✅ **Hiểu trade-offs** — không Tool nào hoàn hảo cho mọi case.

---

## ✅ Self-Check

1. **Theo CNCF Survey, bao nhiêu phần trăm tổ chức dùng K8s ở production?**
   <details>
   <summary>Đáp án</summary>
   64% trong số 96% tổ chức đã đánh giá/dùng K8s.
   </details>

2. **Nhược điểm lớn nhất của K8s là gì?**
   <details>
   <summary>Đáp án</summary>
   **Learning curve cực dốc** — cần 3-6 tháng để cảm thấy quen, dễ quên nếu không dùng thường xuyên.
   </details>

3. **Khi nào KHÔNG nên dùng K8s?**
   <details>
   <summary>Đáp án</summary>
   - Team nhỏ, cần ship nhanh
   - App đơn giản (monolith), ít traffic
   - Không có nguồn lực DevOps đủ mạnh
   - Có thể giải quyết tốt bằng managed service đơn giản hơn (ECS, App Runner...)
   </details>

4. **Liệt kê 3 alternative thay thế K8s phổ biến.**
   <details>
   <summary>Đáp án</summary>
   - **AWS ECS** (đặc biệt với Fargate)
   - **Docker Swarm**
   - **HashiCorp Nomad**
   - Khác: Cloud Run (GCP), Azure Container Apps, App Runner
   </details>

5. **Vì sao giảng viên ưu tiên ECS hơn EKS cho dự án cá nhân?**
   <details>
   <summary>Đáp án</summary>
   ECS đơn giản, intuitive, dễ học, gọn gàng. Chỉ khi cần multi-tenant + security cao mới chuyển qua EKS.
   </details>

---

## 🔗 Liên Kết

### Navigation

- ⬅️ [Bài #2 — Kubernetes là gì?](01-kubernetes-la-gi.md)
- ➡️ [Bài #4 — Cluster Architecture](03-cluster-architecture.md)
- 🏠 [Quay về index Module 01](README.md)

### Tài Nguyên

- 📊 [CNCF Annual Survey 2023](https://www.cncf.io/reports/cncf-annual-survey-2023/)
- 📖 [AWS ECS vs EKS Comparison](https://aws.amazon.com/ecs/faqs/)
- 📖 [When NOT to use Kubernetes](https://www.docker.com/blog/kubernetes-vs-docker/)
- 📺 Video gốc: `Decopy_✅ #3 _ Lý Do Nên & Không Nên Sử Dụng Kubernetes_captions.txt`

---

## 📝 Ghi Chú Từ Giảng Viên

> 💬 *"Cái việc này sẽ quyết định thời gian, thậm chí tiền bạc các bạn dồn vào. Mình can các bạn rằng các bạn cần phải biết chuyện này NGAY TỪ SỚM để cái nỗ lực các bạn đặt ra nó phải xứng đáng."*

> 💬 *"Có những lúc mình loay hoay 1 cái bug mà mất nửa ngày, thậm chí mất cả 1 ngày trời mình không làm được. Bị như thế là chuyện bình thường — đừng nản."*

> 💬 *"Người ta trên Tutorial làm rất nhanh, múa rất lẹ — vì người ta làm chuyện này rất nhiều lần rồi. Các bạn không thể so sánh với người ta được."*

> 💬 *"Mình KHÔNG nên dùng 1 Tool cho tất cả mọi thứ. K8s là công cụ rất tốt, nhưng nó không phải sự lựa chọn duy nhất."*

---

**Tác giả:** Mr.Rom 
**Phiên bản:** v1.0.0
**Ngày tạo:** 09/05/2026
